import MetaTrader5 as mt5
import pandas as pd
import os, time, logging
from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QProgressBar
)
from PyQt5.QtCore import (
    Qt,
    QThread,
    pyqtSignal,
    QRectF
)
from PyQt5.QtGui import (
    QPainterPath,
    QRegion
)

from modules.bot.data_preparation import get_historical_data, prepare_data
from modules.bot.indicators import calculate_indicators
from modules.bot.model_training import train_xgboost_model
from threading import Thread as tds

class TradingBot:
    def __init__(self, userData, lot_ = None, risk_ = None):
        
        print(userData, "#################")
        
        self.ORDER_BUY = 0
        self.ORDER_SELL = 1
        self.ACCOUNT_ID, self.PASSWORD, self.SERVER = userData

        self.EMA_FAST_PERIOD = 5
        self.EMA_SLOW_PERIOD = 20
        self.RSI_PERIOD = 14
        self.STOCHASTIC_K_PERIOD = 14
        self.STOCHASTIC_D_PERIOD = 3
        self.MACD_FAST_PERIOD = 12
        self.MACD_SLOW_PERIOD = 26
        self.MACD_SIGNAL_PERIOD = 9
        self.LOT_SIZE = 0.01
        self.STOP_LOSS = 15
        self.TAKE_PROFIT = 30
        self.RISK_PERCENTAGE = 0.1  # Riesgo del 2% por operación

        self.model = None
        self.df = None
        self.symbol = 'EURUSD'
        self.timeframe = mt5.TIMEFRAME_M5
        
        # Iniciar el hilo del proceso de trading
        self.thread = TradingThread(self)
        self.thread.progress_update.connect(self.update_progress)
        self.thread.finished.connect(self.close_progress_window)
        self.thread.start()
        
        # Ventana de progreso
        self.progress_window = ProgressWindow()
        self.progress_window.show()

    def update_progress(self, message, progress):
        self.progress_window.update_message(message)
        self.progress_window.update_progress(progress)

    def close_progress_window(self):
        self.progress_window.close()

    def initialize_mt5(self):
        logging.info("Conectando a MetaTrader 5...")
        if not mt5.initialize(
            login=self.ACCOUNT_ID,
            password=self.PASSWORD,
            server=self.SERVER
        ):
            logging.error("Error al inicializar MetaTrader 5")
            raise RuntimeError("Error al inicializar MetaTrader 5")
        if not mt5.login(
            login=self.ACCOUNT_ID,
            password=self.PASSWORD,
            server=self.SERVER
        ):
            mt5.shutdown()
            logging.error("Error de autenticación en MetaTrader 5")
            raise RuntimeError("Error de autenticación en MetaTrader 5")
        logging.info("Conexión exitosa con MetaTrader 5")

        if symbol_info := mt5.symbol_info(self.symbol):
            logging.info(f"Atributos disponibles para {self.symbol}: {symbol_info._asdict()}")
        else:
            logging.error(f"Símbolo {self.symbol} no encontrado")

    def prepare_data(self):
        logging.info("Preparando los datos para el modelo...")
        self.df = get_historical_data(self.symbol, self.timeframe, 1000)
        logging.debug(f"Datos obtenidos: {self.df.head()}")
        self.df = calculate_indicators(self.df)
        logging.debug(f"Datos con indicadores: {self.df.head()}")
        self.df = prepare_data(self.df)
        logging.debug(f"Datos preparados: {self.df.head()}")

    def train_model(self):
        logging.info("Entrenando el modelo...")
        try:
            self.model = train_xgboost_model(self.df)
            logging.info("Modelo entrenado exitosamente")
        except Exception as e:
            logging.error(f"Error entrenando el modelo: {e}")

    def make_prediction(self):
        logging.info("Realizando predicción...")
        start_time = time.time()
        last_row = self.df.iloc[-1]
        features = pd.DataFrame([[last_row['ema_fast'], last_row['ema_slow'], last_row['bb_upper'], last_row['bb_lower'], last_row['atr'], 
                                last_row['rsi'], last_row['macd'], last_row['macd_signal'], last_row['macd_histogram'], 
                                last_row['plus_di'], last_row['minus_di'], last_row['adx'], last_row['stochastic_k'], 
                                last_row['stochastic_d'], last_row['vol_change']]], 
                                columns=['ema_fast', 'ema_slow', 'bb_upper', 'bb_lower', 'atr', 'rsi', 'macd', 
                                        'macd_signal', 'macd_histogram', 'plus_di', 'minus_di', 'adx', 
                                        'stochastic_k', 'stochastic_d', 'vol_change'])
        prediction = self.model.predict(features)[0]
        elapsed_time = time.time() - start_time
        logging.info(f"Predicción: {prediction} (Tiempo de predicción: {elapsed_time:.2f} segundos)")
        return prediction

    def open_trade(self, signal):
        lot_size = self.calculate_lot_size()
        symbol_info = mt5.symbol_info(self.symbol)
        
        if not symbol_info:
            logging.error(f"Símbolo {self.symbol} no encontrado")
            return

        account_info = mt5.account_info()
        if not account_info:
            logging.error("Error al obtener la información de la cuenta")
            return
        
        available_balance = account_info.balance
        margin_required = self.calculate_margin_required(lot_size)
        
        if margin_required > available_balance:
            logging.error(f"Saldo insuficiente. Se requiere {margin_required} pero solo hay {available_balance}")
            return

        if signal == 1:  # Buy signal
            price = mt5.symbol_info_tick(self.symbol).ask
            stop_loss = price - self.STOP_LOSS * symbol_info.point
            take_profit = price + self.TAKE_PROFIT * symbol_info.point
            order = {
                'action': mt5.TRADE_ACTION_DEAL,
                'symbol': self.symbol,
                'volume': lot_size,
                'price': price,
                'sl': stop_loss,
                'tp': take_profit,
                'deviation': 20,
                'type': self.ORDER_BUY,
                'magic': 0,
                'comment': "Buy order",
                'type_filling': mt5.ORDER_FILLING_IOC
            }
        elif signal == 0:  # Sell signal
            price = mt5.symbol_info_tick(self.symbol).bid
            stop_loss = price + self.STOP_LOSS * symbol_info.point
            take_profit = price - self.TAKE_PROFIT * symbol_info.point
            order = {
                'action': mt5.TRADE_ACTION_DEAL,
                'symbol': self.symbol,
                'volume': lot_size,
                'price': price,
                'sl': stop_loss,
                'tp': take_profit,
                'deviation': 20,
                'type': self.ORDER_SELL,
                'magic': 0,
                'comment': "Sell order",
                'type_filling': mt5.ORDER_FILLING_IOC
            }
        else:
            logging.info("No hay señales claras para operar")
            return

        result = mt5.order_send(order)
        progressBar = ProgressWindow()
        if result.retcode == mt5.TRADE_RETCODE_DONE:
            logging.info(f"{'BUY' if signal == 1 else 'SELL'} {self.symbol} {price:.4f}| SL={stop_loss:.4f} |TP={take_profit:.4f}")
            if signal == 1:
                progressBar.setlabel("color: blue;")
            else:
                progressBar.setlabel("color: red;")
                self.thread.progress_update.emit(
                f"{'BUY' if signal == 1 else 'SELL'} {self.symbol} {price:.4f}| SL={stop_loss:.4f} |TP={take_profit:.4f}",
                100
            )
        else:
            self.thread.progress_update.emit("ERROR REQUOTE", 0)
            logging.error(f"Error al enviar la orden: {result.retcode} ({result.comment})")

    def calculate_lot_size(self):
        import math
        symbol_info = mt5.symbol_info(self.symbol)
        if not symbol_info:
            logging.error(f"Símbolo {self.symbol} no encontrado")
            return 0

        account_balance = self.get_account_balance()
        risk_amount = self.RISK_PERCENTAGE * account_balance
        stop_loss_amount = self.STOP_LOSS * symbol_info.point
        lot_converted = str(math.floor(risk_amount / stop_loss_amount))[:2]
        lot_final = float(lot_converted[0] + "." + lot_converted[1])
        lot_size = lot_final

        lot_step = getattr(symbol_info, 'volume_step', 0.01)
        lot_size = round(lot_size / lot_step) * lot_step
        logging.info(f"Tamaño del lote calculado: {lot_size}")
        return lot_size

    def calculate_margin_required(self, lot_size):
        return mt5.order_calc_margin(mt5.ORDER_TYPE_BUY, self.symbol, lot_size, mt5.symbol_info_tick(self.symbol).ask)

    def get_account_balance(self):
        account_info = mt5.account_info()
        if not account_info:
            logging.error("Error al obtener la información de la cuenta")
            return 0
        return account_info.balance

class ProgressWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setFixedSize(300, 100)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setObjectName("MainFrame")
        self.setStyleSheet(self.styles())
        layout = QVBoxLayout()

        self.label = QLabel("Iniciando...", self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMaximum(100)
        
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)
        self.round_corners(15)
        
    def round_corners(self, radius):
        rect = QRectF(self.rect())

        path = QPainterPath()
        path.addRoundedRect(rect, radius, radius)

        region = QRegion(path.toFillPolygon().toPolygon())

        self.setMask(region)

    def setlabel(self, style):
        self.label.setStyleSheet(style)
    def update_message(self, message):
        self.label.setText(message)

    def update_progress(self, progress):
        self.progress_bar.setValue(progress)
    
    def styles(self) -> str:
        return """
            #MainFrame {
                background-color: #000;
            }
            QLabel {
                color: #fff;
                font-size: 18;
                font-family: monospace;
            }
            QProgressBar {
                background-color: #00000000;
                color: #000;
                text-align: center;
                border-radius: 10px;
                font-size: 18px;
                font-family: monospace;
            }
            QProgressBar::chunk {
                background-color: #d2053d;
                border-radius: 10px;
            }
        """

class TradingThread(QThread):
    progress_update = pyqtSignal(str, int)

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    def run(self):
        self.progress_update.emit("Conectando a MetaTrader 5...", 10)
        self.bot.initialize_mt5()
        
        self.progress_update.emit("Preparando datos...", 30)
        self.bot.prepare_data()
        
        self.progress_update.emit("Entrenando el modelo...", 50)
        self.bot.train_model()
        
        self.progress_update.emit("Comenzando a operar...", 70)
        try:
            self.progress_update.emit("Realizando predicción...", 80)
            prediction = self.bot.make_prediction()
            
            self.progress_update.emit("Enviando orden...", 90)
            self.bot.open_trade(prediction)
            
            time.sleep(60)
        except Exception as e:
            logging.error(f"Error durante la ejecución del bot: {e}")
        
        self.progress_update.emit("Proceso completado", 100)
        self.quit()

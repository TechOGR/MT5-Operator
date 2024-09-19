import MetaTrader5 as mt5
import pandas as pd
import numpy as np

def get_historical_data(symbol, timeframe, n=1000):
    """Obtiene los datos históricos del símbolo"""
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, n)
    if rates is None:
        raise RuntimeError(f"No se pudieron obtener los datos para {symbol}")
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.set_index('time', inplace=True)
    return df

def prepare_data(df):
    """Prepara los datos para el modelo"""
    df['label'] = np.where(df['close'].shift(-1) > df['close'], 1, 0)
    df.dropna(inplace=True)  # Elimina filas con valores NaN
    return df

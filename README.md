# MT5 Operator

Herramienta de trading con interfaz gráfica en PyQt5 que se integra con MetaTrader 5 para conectar tu cuenta, preparar datos, entrenar un modelo de predicción (XGBoost) y ejecutar operaciones de forma asistida.

- Entrada principal: [main.py](file:///d:/Programacion/Python/MT5-Operator/main.py)
- Interfaz gráfica: [interface.py](file:///d:/Programacion/Python/MT5-Operator/gui/interface.py)
- Conexión MT5: [connect_mt5.py](file:///d:/Programacion/Python/MT5-Operator/modules/connect_mt5.py)
- Bot de trading: [predict_bot.py](file:///d:/Programacion/Python/MT5-Operator/modules/bot/predict_bot.py)

## Tabla de Contenidos
- [Características](#características)
- [Arquitectura](#arquitectura)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Ejecución](#ejecución)
- [Configuración](#configuración)
- [Compilación a .exe](#compilación-a-exe)
- [Estructura de Carpetas](#estructura-de-carpetas)
- [Licencia](#licencia)
- [Contacto](#contacto)

## Características
- Interfaz moderna sin bordes, con estilos personalizados y atajos de teclado.
- Conexión a MetaTrader 5 con usuario, password y servidor.
- Preparación de datos e indicadores técnicos (EMA, Bollinger, ATR, RSI, MACD, DMI/ADX, Estocástico).
- Entrenamiento de modelo XGBoost y predicciones para orientación operativa.
- Ventana de progreso durante conexión, preparación y entrenamiento.
- Gestión de credenciales y configuración en archivos locales.
- Empaquetado a ejecutable Windows con PyInstaller y hook para XGBoost.

## Arquitectura
- Aplicación GUI: [interface.py](file:///d:/Programacion/Python/MT5-Operator/gui/interface.py#L1-L40) define la ventana principal (clase Window) y elementos de UI.
- Conexión MT5: [connect_mt5.py](file:///d:/Programacion/Python/MT5-Operator/modules/connect_mt5.py#L1-L19) inicializa y valida credenciales contra MT5.
- Bot de Trading:
  - Flujo general: [predict_bot.py](file:///d:/Programacion/Python/MT5-Operator/modules/bot/predict_bot.py#L1-L120)
  - Preparación de datos: [data_preparation.py](file:///d:/Programacion/Python/MT5-Operator/modules/bot/data_preparation.py#L1-L19)
  - Indicadores técnicos: [indicators.py](file:///d:/Programacion/Python/MT5-Operator/modules/bot/indicators.py#L4-L58)
  - Entrenamiento XGBoost: [model_training.py](file:///d:/Programacion/Python/MT5-Operator/modules/bot/model_training.py#L7-L36)
- Estilos de UI: [styles.py](file:///d:/Programacion/Python/MT5-Operator/modules/styles.py)
- Configuración y almacenamiento local: [ctrl_data.py](file:///d:/Programacion/Python/MT5-Operator/modules/ctrl_data.py)
- Entrada de la app: [main.py](file:///d:/Programacion/Python/MT5-Operator/main.py#L7-L11) crea QApplication y muestra la ventana.

## Requisitos
- Windows con [MetaTrader 5](https://www.metatrader5.com/es/download) instalado.
- Python 3.x
- Paquetes de Python:
  - PyQt5
  - MetaTrader5
  - pandas
  - numpy
  - scikit-learn
  - xgboost

## Instalación
1. Clona el repositorio:

   ```bash
   git clone https://github.com/TechOGR/MT5-Operator.git
   cd MT5-Operator
   ```

2. (Opcional) Crea y activa un entorno virtual:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Instala dependencias:

   ```bash
   pip install PyQt5 MetaTrader5 pandas numpy scikit-learn xgboost
   ```

## Ejecución
- Ejecuta la aplicación:

  ```bash
  python main.py
  ```

- En la interfaz:
  - Ingresa Usuario (login), Password y Servidor de tu cuenta MT5.
  - Conecta y guarda tus datos si lo deseas.
  - Usa el botón “PredictorBot” para lanzar el proceso de:
    - Conexión a MT5, carga de históricos y cálculo de indicadores.
    - Entrenamiento del modelo XGBoost.
    - Predicción y ejecución de una orden según la señal.

Referencias:
- Entrada: [main.py](file:///d:/Programacion/Python/MT5-Operator/main.py)
- Ventana principal: [interface.py](file:///d:/Programacion/Python/MT5-Operator/gui/interface.py#L80-L120)
- Bot y progreso: [predict_bot.py](file:///d:/Programacion/Python/MT5-Operator/modules/bot/predict_bot.py#L60-L120)

## Configuración
- Credenciales:
  - Se guardan en [userData.json](file:///d:/Programacion/Python/MT5-Operator/config/userData.json) vía [ctrl_data.py](file:///d:/Programacion/Python/MT5-Operator/modules/ctrl_data.py#L39-L83).
  - Si no existe la carpeta, se crea automáticamente al guardar.
- Pares de divisas disponibles:
  - [currencyPair.json](file:///d:/Programacion/Python/MT5-Operator/config/currencyPair.json)
- Servidor:
  - Campo con sugerencias en la UI: [customEditServer.py](file:///d:/Programacion/Python/MT5-Operator/modules/components/customEditServer.py)

## Compilación a .exe
- Script de build: [build.bat](file:///d:/Programacion/Python/MT5-Operator/build.bat)
- Hook para incluir recursos de XGBoost en el exe:
  - [hook-xgboost.py](file:///d:/Programacion/Python/MT5-Operator/hooks/hook-xgboost.py)
- Compilar:

  ```bash
  build.bat
  ```

Genera un ejecutable “MT-Operator.exe” en la carpeta de distribución (PyInstaller).

## Estructura de Carpetas
- Código principal: [gui](file:///d:/Programacion/Python/MT5-Operator/gui), [modules](file:///d:/Programacion/Python/MT5-Operator/modules)
- Recursos: [img](file:///d:/Programacion/Python/MT5-Operator/img), [fonts](file:///d:/Programacion/Python/MT5-Operator/fonts)
- Config: [config](file:///d:/Programacion/Python/MT5-Operator/config)
- Build: [build.bat](file:///d:/Programacion/Python/MT5-Operator/build.bat), [hooks](file:///d:/Programacion/Python/MT5-Operator/hooks)

## Licencia
- No se ha definido una licencia formal en este repositorio.
- El uso del software está sujeto a la autorización del autor.

## Contacto
- YouTube: https://www.youtube.com/@OnelCrack

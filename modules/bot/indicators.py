import pandas as pd
import numpy as np

def calculate_indicators(df):
    """Calcula todos los indicadores técnicos relevantes"""
    # EMA
    df['ema_fast'] = df['close'].ewm(span=5, adjust=False).mean()
    df['ema_slow'] = df['close'].ewm(span=20, adjust=False).mean()
    
    # Bollinger Bands
    df['bb_middle'] = df['close'].rolling(window=20).mean()
    df['bb_std'] = df['close'].rolling(window=20).std()
    df['bb_upper'] = df['bb_middle'] + (df['bb_std'] * 2)
    df['bb_lower'] = df['bb_middle'] - (df['bb_std'] * 2)
    
    # ATR
    df['tr'] = np.maximum(df['high'] - df['low'], 
                          abs(df['high'] - df['close'].shift(1)), 
                          abs(df['low'] - df['close'].shift(1)))
    df['atr'] = df['tr'].rolling(window=14).mean()

    # RSI
    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    df['rsi'] = 100 - (100 / (1 + rs))

    # MACD
    df['macd'] = df['close'].ewm(span=12, adjust=False).mean() - df['close'].ewm(span=26, adjust=False).mean()
    df['macd_signal'] = df['macd'].ewm(span=9, adjust=False).mean()
    df['macd_histogram'] = df['macd'] - df['macd_signal']

    # DMI
    df['tr'] = np.maximum(df['high'] - df['low'], 
                          abs(df['high'] - df['close'].shift(1)), 
                          abs(df['low'] - df['close'].shift(1)))
    df['plus_dm'] = df['high'].diff().clip(lower=0)
    df['minus_dm'] = -df['low'].diff().clip(upper=0)
    df['tr14'] = df['tr'].rolling(window=14).sum()
    df['plus_dm14'] = df['plus_dm'].rolling(window=14).sum()
    df['minus_dm14'] = df['minus_dm'].rolling(window=14).sum()
    df['plus_di'] = 100 * (df['plus_dm14'] / df['tr14'])
    df['minus_di'] = 100 * (df['minus_dm14'] / df['tr14'])
    df['adx'] = 100 * (abs(df['plus_di'] - df['minus_di']) / (df['plus_di'] + df['minus_di'])).rolling(window=14).mean()

    # Estocástico
    df['stochastic_k'] = 100 * ((df['close'] - df['low'].rolling(window=14).min()) /
                                (df['high'].rolling(window=14).max() - df['low'].rolling(window=14).min()))
    df['stochastic_d'] = df['stochastic_k'].rolling(window=3).mean()

    # Volumen
    if 'volume' in df.columns:
        df['vol_change'] = df['volume'].pct_change()
    else:
        df['vol_change'] = 0

    return df

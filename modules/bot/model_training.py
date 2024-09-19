from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score, GridSearchCV
from xgboost import XGBClassifier

def train_xgboost_model(df):
    """Entrena el modelo XGBoost con optimización de hiperparámetros"""
    features = df[['ema_fast', 'ema_slow', 'bb_upper', 'bb_lower', 'atr', 'rsi', 'macd', 'macd_signal', 
                'macd_histogram', 'plus_di', 'minus_di', 'adx', 'stochastic_k', 'stochastic_d', 'vol_change']]
    labels = df['label']

    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.3, random_state=42)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [3, 5, 7],
        'learning_rate': [0.01, 0.1, 0.2],
        'subsample': [0.8, 1.0],
        'colsample_bytree': [0.8, 1.0]
    }

    xgb = XGBClassifier()
    grid_search = GridSearchCV(xgb, param_grid, scoring='accuracy', cv=3, n_jobs=-1)
    try:
        grid_search.fit(X_train_scaled, y_train)
        best_model = grid_search.best_estimator_
        y_pred = best_model.predict(X_test_scaled)
        print(f"Precisión del mejor modelo: {accuracy_score(y_test, y_pred):.2f}")
    except Exception as e:
        print(f"Error durante la búsqueda de hiperparámetros: {e}")
    
    return best_model

def train_xgboost_model_v2(df):
    """Entrena el modelo XGBoost con parámetros fijos"""
    features = df[['ema_fast', 'ema_slow', 'bb_upper', 'bb_lower', 'atr', 'rsi', 'macd', 'macd_signal', 
                'macd_histogram', 'plus_di', 'minus_di', 'adx', 'stochastic_k', 'stochastic_d', 'vol_change']]
    labels = df['label']

    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.3, random_state=42)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = XGBClassifier(n_estimators=100, max_depth=5, learning_rate=0.1)
    model.fit(X_train_scaled, y_train)

    y_pred = model.predict(X_test_scaled)
    print(f"Precisión del modelo: {accuracy_score(y_test, y_pred):.2f}")
    return model

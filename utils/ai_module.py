import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from datetime import datetime


def preprocess_solar_data(df):
    """Preprocess solar generation data"""
    # Convert timestamp and extract features
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    df['is_daylight'] = df['hour'].between(6, 18).astype(int)

    # Scale the numerical features
    scaler = StandardScaler()
    features = ['generation_kw', 'hour', 'day_of_week']
    X_scaled = scaler.fit_transform(df[features])

    return X_scaled, scaler, df


def train_isolation_forest(X_scaled, contamination=0.05):
    """Train an isolation forest model"""
    model = IsolationForest(contamination=contamination,
                            random_state=42,
                            n_estimators=100)
    model.fit(X_scaled)
    return model


def detect_anomalies(model, X_scaled, df):
    """Detect anomalies and return labeled data"""
    preds = model.predict(X_scaled)
    df['is_anomaly'] = (preds == -1).astype(int)
    return df


def generate_solar_summary(df):
    """Generate summary of solar anomalies"""
    anomalies = df[df['is_anomaly'] == 1]

    if anomalies.empty:
        return "No solar generation anomalies detected"

    summary = f"Detected {len(anomalies)} solar generation anomalies:\n"
    for _, row in anomalies.iterrows():
        summary += f"- {row['timestamp']}: Generation {row['generation_kw']:.2f} kW\n"

    return summary
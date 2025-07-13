import pandas as pd
from utils.ai_module import preprocess_solar_data, train_isolation_forest, detect_anomalies
from utils.db import get_db_connection


def update_solar_data():
    try:
        # Load and process data
        solar_data = pd.read_csv("utils/cleaned_solar_data_reduced.csv")
        X_scaled, scaler, processed_data = preprocess_solar_data(solar_data)
        model = train_isolation_forest(X_scaled)
        results = detect_anomalies(model, X_scaled, processed_data)

        # Save to database
        conn = get_db_connection()
        results.to_sql('solar_data', conn, if_exists='replace', index=False)
        conn.commit()
        conn.close()

        return True
    except Exception as e:
        print(f"Error updating solar data: {str(e)}")
        return False


if __name__ == "__main__":
    update_solar_data()
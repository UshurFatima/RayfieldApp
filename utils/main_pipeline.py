import pandas as pd
import matplotlib.pyplot as plt
from ai_module import preprocess_solar_data, train_isolation_forest, detect_anomalies, generate_solar_summary

try:
    df = pd.read_csv("cleaned_solar_data_reduced.csv", parse_dates = ["date"])
except FileNotFoundError:
    import numpy as np
    dates = pd.date_range(start = "2025-01-01", period = 100, freq = 'D')
    np.random.seed(42)
    output_kw = np.random.normal(loc = 5000, scale = 300, size = 100)
    output_kw[10] = 2000
    output_kw[50] = 8000

    df = pd.DataFrame({
        "data": dates,
        "output_kw": output_kw
    })

print("Data sample:")
print(df.head())

#preprocess data
X_scaled, scaler = preprocess_solar_data(df, ["output_kw"])

#train model
model = train_isolation_forest(X_scaled, contamination = 0.05)

#predict anomalies
df["anomaly"] = detect_anomalies(model, X_scaled)
print(df.head())

#save final csv
df.to_csv("final_output_with_anomalies.csv", index = False)
print("Saved final_output_with_anomalies.csv")

#visualize data
anomalies = df[df["anomaly"] == True]

plt.figure(figsize = (12, 6))
plt.plot(df["date"], df["output_kw"], label = "Normal Data")
plt.scatter(anomalies["date"], anomalies["output_kw"],
            color = 'red', label = 'Anomaly')
plt.title("Energy Output with Anomalies Highlighted")
plt.xlabel("Date")
plt.ylabel("Output (kW)")
plt.legend()
plt.show()

#generate summary
summary = generate_solar_summary(df)
print(summary)

#save summary
with open("weekly_summary.txt", "w") as f:
    f.write(summary)
print("Saved weekly_summary.txt")
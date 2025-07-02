# use conda python 3.12
# Header der .csv: timedate, temp, hum
# ggf zeit anpassen von wetterdaten

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error

# ==== 1. Simulationsdaten laden ====
T_in_df = pd.read_csv("earthship_model/simulierte_temperatur.csv", parse_dates=["timedate"])

# ==== 2. Echte Messdaten laden ====
real_df = pd.read_csv("earthship_model/data/logger3_wohnraum.csv", parse_dates=["timedate"])

# Messzeitbereich ermitteln und Simulationsdaten passend beschränken
start = real_df["timedate"].min()
end = real_df["timedate"].max()
T_in_df = T_in_df[(T_in_df["timedate"] >= start) & (T_in_df["timedate"] <= end)]

# ==== 3. Messzeitpunkte zu nächstem Simulationszeitpunkt matchen ====
real_df["matched_time"] = real_df["timedate"].apply(
    lambda t: T_in_df.iloc[(T_in_df["timedate"] - t).abs().argmin()]["timedate"]
)

# ==== 4. Merge beider Tabellen anhand matched_time ====
merged = real_df.merge(T_in_df, left_on="matched_time", right_on="timedate", how="inner")

# ==== 5. Fehlerberechnung ====
temp_mae = mean_absolute_error(merged["temp"], merged["T_in"])

print(f"Temperatur MAE (Messung vs. Simulation): {temp_mae:.2f} °C")

# ==== 6. Plot: Vergleich Messung vs. Simulation ====
plt.figure(figsize=(12, 5))
plt.plot(merged["matched_time"], merged["temp"], label="Gemessen", marker='o')
plt.plot(merged["matched_time"], merged["T_in"], label="Simulation", linestyle='--')
plt.title("Temperatur: Messung vs. Simulation")
plt.ylabel("Temperatur (°C)")
plt.xlabel("Zeit")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# use conda python 3.12
# header of .csv: timedate, temp, hum, voltage, radiation intensity
# zeitstempel von wetterdaten evtl anders?
# ERA5 hourly data on single levels from 1940 to present



import pandas as pd
import numpy as np
import xarray as xr
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt

# 1. Wetterdaten laden
weather_data_t2m_nc = "earthship_model/data_db_val/temp.nc"
weather_data_ssrd_nc= "earthship_model/data_db_val/ssrd.nc"
weather_data_t2m = xr.open_dataset(weather_data_t2m_nc)
weather_data_ssrd = xr.open_dataset(weather_data_ssrd_nc)
time_data = pd.to_datetime(weather_data_t2m["valid_time"].values)

# Identify the closest grid point
lat = 49.126513                                  # Tempelhof: 49.126513, # north-south
lon = 10.206333                                 # Tempelhof: 10.206333 # east-west 

# wetterdaten auswählen
latitudes = weather_data_t2m.variables["latitude"][:]
longitudes = weather_data_t2m.variables["longitude"][:]
lat_idx = np.argmin(np.abs(latitudes.data - lat))
lon_idx = np.argmin(np.abs(longitudes.data - lon))
outdoor_temp = weather_data_t2m.variables["t2m"][:, lat_idx, lon_idx] - 273.15
solar_radiation = weather_data_ssrd.variables["ssrd"][:, lat_idx, lon_idx] / 3600

# Wetter-Datenframe erstellen
weather_df = pd.DataFrame({
    "datetime": time_data,
    "sim_temp": outdoor_temp,
    "sim_radiation": solar_radiation
})

# 2. CSV laden
real_df = pd.read_csv("earthship_model/data_db_val/logger2_dach.csv", parse_dates=["timedate"])

# Nur Wetterdaten im Bereich der Messdaten verwenden
start = real_df["timedate"].min()
end = real_df["timedate"].max()
weather_df = weather_df[(weather_df["datetime"] >= start) & (weather_df["datetime"] <= end)]

# 3. Zuordnung: Nächster Wetter-Zeitpunkt für jede Messung
real_df["matched_time"] = real_df["timedate"].apply(
    lambda t: weather_df.iloc[(weather_df["datetime"] - t).abs().argmin()]["datetime"]
)

# 4. Merge: Wetter- und Echtdaten
merged = real_df.merge(weather_df, left_on="matched_time", right_on="datetime", how="inner")

# 5. Fehler berechnen
temp_mae = mean_absolute_error(merged["temp"], merged["sim_temp"])

rad_mae = mean_absolute_error(merged["radiation intensity"], merged["sim_radiation"])

print(f"Temperatur MAE: {temp_mae:.2f} °C")
print(f"Strahlung MAE: {rad_mae:.2f} W/m²")

# === 6. Plotten ===

# Temperaturplot
plt.figure(figsize=(12, 5))
plt.plot(merged["timedate"], merged["temp"], label="Gemessen", marker='o', linestyle='--')  # Nur Punkte
plt.plot(merged["timedate"], merged["sim_temp"], label="Datenbank", marker='x', linestyle='--')  # Linie mit Punkten
plt.title("Temperaturvergleich")
plt.ylabel("Temperatur (°C)")
plt.xlabel("Zeit")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


# Strahlungsplot
plt.figure(figsize=(12, 5))
plt.plot(merged["timedate"], merged["radiation intensity"], label="Gemessen", marker='o', linestyle='--')  # Punkte
plt.plot(merged["timedate"], merged["sim_radiation"], label="Datenbank", marker='x', linestyle='--')  # Linie mit Marker
plt.title("Strahlungsintensität Vergleich")
plt.ylabel("Strahlung (W/m²)")
plt.xlabel("Zeit")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


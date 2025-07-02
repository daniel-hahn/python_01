import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import pandas as pd
from config import *  # Import all constants and variables
import pvlib

# Load weather data
weather_data_t2m = xr.open_dataset(weather_data_t2m_nc)
weather_data_ssrd = xr.open_dataset(weather_data_ssrd_nc)
weather_data_wind_u10 = xr.open_dataset(weather_data_wind_u_nc)
weather_data_wind_v10 = xr.open_dataset(weather_data_wind_v_nc)

# Identify the closest grid point
latitudes = weather_data_t2m.variables["latitude"][:]
longitudes = weather_data_t2m.variables["longitude"][:]
lat_idx = np.argmin(np.abs(latitudes.data - lat))
lon_idx = np.argmin(np.abs(longitudes.data - lon))

# Extract temperature, radiation and wind
outdoor_temp = weather_data_t2m.variables["t2m"][:, lat_idx, lon_idx] - 273.15
solar_radiation = weather_data_ssrd.variables["ssrd"][:, lat_idx, lon_idx] / 3600
wind_speed_u10 = weather_data_wind_u10.variables["u10"][:, lat_idx, lon_idx]  # m/s 
wind_speed_v10 = weather_data_wind_v10.variables["v10"][:, lat_idx, lon_idx]  # m/s 

# calc real wind, horizontal wind speed, 2m (log wind profile equation, commonly used in building physics and meteorology)
min_len = min(len(wind_speed_u10), len(wind_speed_v10))
wind_speed_10 = np.sqrt(wind_speed_u10[:min_len]**2 + wind_speed_v10[:min_len]**2)
z = 2                   # height of Earthship
z_ref = 10              # height of ERA5 wind measurement
z0 = 0.3                # e.g. for suburban/vegetated area (Wind speed reduction (10 m → 3 m): 58%)
wind_speed_2m = wind_speed_10 * (np.log(z / z0) / np.log(z_ref / z0))
wind_speed_green_wall = wind_speed_2m * green_wall_factor

# Extract time data
time_data = pd.to_datetime(weather_data_t2m["valid_time"].values)

# solar angle calc
location = pvlib.location.Location(latitude=lat, longitude=lon)
solar_position = location.get_solarposition(time_data[:total_steps])
solar_elevation = solar_position['elevation'].values # Extract solar elevation angle

# Initialize arrays for simulation
Q_solar_mass_stored = np.zeros(total_steps)
T_in = np.zeros(total_steps)
T_in[0] = starttemp
Q_solar_total_plot = np.zeros(total_steps)
transmission_heat_loss_plot = np.zeros(total_steps)
Q_vent_loss_plot = np.zeros(total_steps)
Q_thermal_mass_released_plot = np.zeros(total_steps)
internal_heat_plot = np.zeros(total_steps)
Q_solar_direct_useful_plot = np.zeros(total_steps)

# Sums for H_T' calc
w_U_ges_sum = 0
d_U_ges_sum = 0
b_U_ges_sum = 0 

# Sum for H_T calc
H_T_total = 0

# TAI^2, quadratischer Temperaturabweichungsindex
comf_t_min = 18
comf_t_max = 24
TAI2 = 0

# Sum for SAKZ, stunden außerhalb der komfortzone
SAKZ = 0

# Simulation loop
for t in range(1, total_steps):

    # Update mean temperature of surface and environment
    T_m_i = T_in[t-1] + 273.15          # Convert to Kelvin
    T_m_e = outdoor_temp[t] + 273.15    # Convert to Kelvin

    # Update convective and radiative coefficients, inside and outside
    h_re_green_wall = eps_e_green_wall * 4 * boltz_const * (T_m_e ** 3)  # W/(m²K)
    h_ri = eps_i * 4 * boltz_const * (T_m_i ** 3)  # W/(m²K)
    h_ce_green_wall = 4 + 4 * wind_speed_green_wall[t]  # W/(m²K)
    # v_wind_windows = wind_speed_2m[t]
    # h_ce_window = 4 + 4 * v_wind_windows  # W/(m²K)
    # h_re_window = eps_e_window * 4 * boltz_const * (T_m_e ** 3)  # W/(m²K)

    # Update Rs and U values
    w_Rs_i = 1 / (h_ri + h_ci)                                          # wall
    w_Rs_e = 1 / (h_re_green_wall + h_ce_green_wall)                    # wall
    w_U_ges = 1 / (w_Rs_i + w_s1_R + w_s2_R + w_s3_R + w_s4_R + w_Rs_e) # wall
    w_U_ges_sum += w_U_ges_sum

    d_Rs_i = 1 / (h_ri + h_ci)                                          # roof
    d_Rs_e = 1 / (h_re_green_wall + h_ce_green_wall)                    # roof
    d_U_ges = 1 / (d_Rs_i + d_s1_R + d_s2_R + d_s3_R + d_s4_R + d_Rs_e) # roof 
    d_U_ges_sum += d_U_ges_sum

    b_Rs_i = 1 / (h_ri + h_ci)                                          # floor
    b_Rs_e = 1 / (h_re_green_wall + h_ce_green_wall)                    # floor
    b_U_ges = 1 / (b_Rs_i + b_s1_R + b_s2_R + b_s3_R + b_Rs_e)          # floor
    b_U_ges_sum += b_U_ges_sum

    #H_T = w_U_ges * (w_A_n * w_F_n + w_A_o * w_F_o + w_A_w * w_F_w) + b_U_ges * b_A * b_F + d_U_ges * d_A + f_U_ges * f_A_s + delta_U_WB * A_huell
    #H_T_spezif = H_T / A_huell
    #print("H_T_spezif: ")
    #print(H_T_spezif)

    # Solar heat gain, Determine solar gain factor based on sun elevation angle
    Q_solar_direct = solar_radiation[t] * f_A_s * solar_transmittance * F_F * F_S * F_C # F_W is redundant
    if solar_elevation[t] <= sun_threshold_deg_min:
        solar_gain_factor = 1.0
    elif solar_elevation[t] >= sun_threshold_deg_max:
        solar_gain_factor = 0.0
    else:
        solar_gain_factor = (sun_threshold_deg_max - solar_elevation[t]) / (sun_threshold_deg_max - sun_threshold_deg_min) # Linear interpolation between min and max gain angle
    # Apply solar gain factor to direct solar radiation
    Q_solar_direct_useful = Q_solar_direct * (1 - thermal_mass_absorption) * solar_gain_factor
    Q_solar_mass_stored[t] = Q_solar_mass_stored[t-1] * (1 - thermal_mass_release_factor) + Q_solar_direct * thermal_mass_absorption * solar_gain_factor
    Q_solar_mass_released = Q_solar_mass_stored[t-1] * thermal_mass_release_factor

    # Internal heat gains
    internal_heat = internal_gains_day if solar_radiation[t] > 0 else internal_gains_night
    
    # Ventilation heat loss
    ventilation_rate = ventilation_rate_day if solar_radiation[t] > 0 else ventilation_rate_night
    if T_in[t-1] > 24:
        ventilation_rate = 1.5  # increase to remove heat
    elif T_in[t-1] < 16:
        ventilation_rate = 0.1  # reduce to retain heat
    air_mass_flow = ventilation_rate * room_volume * air_density /3600
    Q_vent = air_mass_flow * specific_heat_air * (T_in[t-1] - outdoor_temp[t]) # or use ground_temp for air pipes

    # Heat loss through walls, floor, roof, windows (through transmission, convection, radiation)
    Q_wall_loss = w_U_ges * w_A_ges * w_F * (T_in[t-1] - outdoor_temp[t]) 
    Q_floor_loss = b_U_ges * b_A * b_F * (T_in[t-1] - ground_temperature)
    Q_roof_loss = d_U_ges * d_A * d_F * (T_in[t-1] - outdoor_temp[t])
    Q_window_loss = f_U_ges * f_A_s * f_F * (T_in[t-1] - outdoor_temp[t]) * (1 - wintergarden_effect)
    Q_HB_loss = delta_U_WB * A_huell * (T_in[t-1] - outdoor_temp[t])
    transmission_heat_loss = Q_wall_loss + Q_floor_loss + Q_roof_loss + Q_window_loss + Q_HB_loss

    # Net heat flow and temperature change
    dT = (Q_solar_direct_useful + Q_solar_mass_released + internal_heat - Q_vent - transmission_heat_loss) *3600/ thermal_mass # *3600
    T_in[t] = T_in[t-1] + dT
    
    net_heat_flow = Q_solar_direct_useful + Q_solar_mass_released + internal_heat - Q_vent - transmission_heat_loss # Watt
    if (net_heat_flow < 0):
        H_T_total = H_T_total + net_heat_flow # Wh

    # store variables for plots
    Q_solar_direct_useful_plot[t] = Q_solar_direct_useful
    transmission_heat_loss_plot[t] = transmission_heat_loss
    Q_vent_loss_plot[t] = Q_vent
    Q_thermal_mass_released_plot[t] = Q_solar_mass_released
    internal_heat_plot[t] = internal_heat

    # TAI^2 and SAKZ calc
    if (T_in[t] > comf_t_max):
        TAI2 += T_in[t] - comf_t_max
        SAKZ += 1
    if (T_in[t] < comf_t_min):
        TAI2 += comf_t_min - T_in[t]
        SAKZ += 1


# H_T' calc
w_U_ges_average = w_U_ges_sum/ total_steps 
d_U_ges_average = d_U_ges_sum/ total_steps
b_U_ges_average = b_U_ges_sum/ total_steps
A_bez = laenge_wohnflaeche * breite_wohnflaeche
H_T_spec = ((w_U_ges_average * w_A_ges + d_U_ges_average * d_A + b_U_ges_average * b_A + f_U_ges * f_A_s)/ A_bez) + delta_U_WB
print ("H_T' (W/(m^2*K)):" + str(H_T_spec))

# H_T calc
print ("H_T (kWh):" + str(float(H_T_total/1000)))

# TAI^2 and SAKZ result
print("TAI^2: " + str(TAI2))
print("SAKZ: " + str(SAKZ))

# create .csv for validation of T_in
df_out = pd.DataFrame({
    "timedate": time_data[:total_steps],
    "T_in": T_in[:total_steps]  # falls T_in länger ist als total_steps
})
df_out.to_csv("simulierte_temperatur.csv", index=False)

# Plot results
# Indoor vs Outdoor Temperature
plt.figure(figsize=(10, 5))
plt.plot(time_data[:total_steps], T_in, label="Indoor Temperature (°C)", color="red")
plt.plot(time_data[:total_steps], outdoor_temp[:total_steps], label="Outdoor Temperature (°C)", color="blue", linestyle="dashed")
plt.axhspan(18, 23, color='green', alpha=0.2, label="Comfort Zone (18-23°C)")
plt.xlabel("Time")
plt.ylabel("Temperature (°C)")
plt.title("Earthship Indoor vs Outdoor Temperature")
plt.legend()
plt.grid()
plt.xticks(rotation=45)
plt.show(block=False)

# Solar Gains vs Heat Losses
plt.figure(figsize=(10, 5))
plt.plot(time_data[:total_steps], (Q_solar_direct_useful_plot + Q_thermal_mass_released_plot + internal_heat_plot), label="Total Gains (Direct Solar + Thermal Mass + Internal) (W)", color="orange")
plt.plot(time_data[:total_steps], Q_vent_loss_plot, label="Total Heat Losses (Transmission + Ventilation) (W)", color="blue", linestyle="dashed")
plt.xlabel("Time")
plt.ylabel("Heat (W)")
plt.title("Total Gains vs Total Losses")
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.show(block=False)

# Thermal Mass Stored/Released
plt.figure(figsize=(10, 5))
plt.plot(time_data[:total_steps], Q_solar_mass_stored, label="Thermal Mass Stored (J)", color="red")
plt.plot(time_data[:total_steps], Q_thermal_mass_released_plot, label="Thermal Mass Released (J)", color="green", linestyle="dashed")
plt.xlabel("Time")
plt.ylabel("Heat (J)")
plt.title("Thermal Mass Stored vs Released Heat")
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.show(block=False)

# Ventilation Loss vs Gains
plt.figure(figsize=(10, 5))
plt.plot(time_data[:total_steps], Q_vent_loss_plot, label="Ventilation Loss (W)", color="blue")
plt.plot(time_data[:total_steps], internal_heat_plot + Q_solar_direct_useful_plot, label="Internal & Solar Gains (W)", color="red", linestyle="dashed")
plt.xlabel("Time")
plt.ylabel("Heat (W)")
plt.title("Ventilation Loss vs Internal & Solar Gains")
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.show(block=False)

plt.show()
import numpy as np

# --- Weather, Position & Simulation Settings ---
weather_data_t2m_nc = "data_23-25_t2m.nc"
weather_data_ssrd_nc= "data_23-25_ssrd_accum.nc"
weather_data_wind_u_nc= "data_23-25_wind_u10.nc"
weather_data_wind_v_nc= "data_23-25_wind_v10.nc"

lat = 49.5                                  # Tempelhof: 49.126513, # north-south
lon = 11.5                                  # Tempelhof: 10.206333 # east-west 
#time_step = 3600                           # Time step in seconds (1 hour)
days = 365                                  # Simulation duration (days)
total_steps = days * 24                     # Total time steps
ground_temperature = 5                      # °C
starttemp = 15                              # °C

# --- Earthship Construction Properties ---
roh_earthwall = 2000                        # kg/m^3
c_earthwall = 900                           # kg/m^3
laenge_wohnflaeche = 10                     # m
breite_wohnflaeche = 5                      # m
breite_oben_wintergarten = 1                # m
breite_unten_wintergarten = 1.5             # m
hoehe_wohnflaeche = 2.5                     # m
d_earthwall = 1                             # m

# winkel_fenster =  np.arctan(hoehe_wohnflaeche/(breite_unten_wintergarten-breite_oben_wintergarten)) # °
# V_earthwall = 2 * (breite_wohnflaeche * d_earthwall * hoehe_wohnflaeche) + 1 * (laenge_wohnflaeche * d_earthwall * hoehe_wohnflaeche) + 1 * (breite_wohnflaeche * d_earthwall * laenge_wohnflaeche) + 2 * (d_earthwall**2 * breite_wohnflaeche) + 2 * (d_earthwall**2 * (hoehe_wohnflaeche + d_earthwall)) + 1 * (d_earthwall**2 * laenge_wohnflaeche) + 1 * ((breite_wohnflaeche +1*d_earthwall) * d_earthwall * (laenge_wohnflaeche+2*d_earthwall)) #140 #m^3 # boden: 1m dick??
aktive_wandtiefe = 1                        # m, wirken thermisch aktiv (je nach Zeitkonstante)
aktive_wandflaeche = 2 * (hoehe_wohnflaeche*laenge_wohnflaeche) + 2 * (hoehe_wohnflaeche*breite_wohnflaeche) + 2 * (breite_wohnflaeche*laenge_wohnflaeche)  # alle Innenwände inkl. Boden
V_aktiv = aktive_wandflaeche * aktive_wandtiefe
thermal_mass = roh_earthwall * c_earthwall * V_aktiv                                            # 100000  # J/K
room_volume = laenge_wohnflaeche*breite_wohnflaeche*hoehe_wohnflaeche                           # m³, ohne wintergarten

# --- Heat Loss Properties ---
boltz_const = 5.67e-8                       # Stefan-Boltzmann Constant (W/m²K⁴)

# --- Indoor Surface Properties ---
eps_i = 0.9                                 # --
h_ci = 2.5                                  # W/(m²K) , standard value for horizonal wind flow

# --- Outdoor Surface Properties ---
eps_e_window = 0.9                          # --
eps_e_green_wall = 0.85                     # --

# --- Wall Construction ---
w_A_n, w_A_o, w_A_w = hoehe_wohnflaeche*laenge_wohnflaeche, hoehe_wohnflaeche*breite_wohnflaeche, hoehe_wohnflaeche*breite_wohnflaeche  # inside Wall areas (m²)
w_A_ges = w_A_n + w_A_o + w_A_w             # m^2, Total inside wall area, without wintergarden
w_F_n, w_F_o, w_F_w, w_F = 1, 1, 1, 1               # Correction factors

w_s1_lambda, w_s1_d = 0.5, 0.1              # (W/mK, m) vegetation
w_s2_lambda, w_s2_d = 1.8, d_earthwall      # (W/mK, m) Compacted earth
w_s3_lambda, w_s3_d = 0.25, 0.005           # (W/mK, m) Tire wall
w_s4_lambda, w_s4_d = 0.04, 0.15            # (W/mK, m) Insulation

w_s1_R = w_s1_d / w_s1_lambda               # (m^2*K)/W
w_s2_R = w_s2_d / w_s2_lambda               # (m^2*K)/W
w_s3_R = w_s3_d / w_s3_lambda               # (m^2*K)/W
w_s4_R = w_s4_d / w_s4_lambda               # (m^2*K)/W

# --- Roof ---
d_A = hoehe_wohnflaeche * breite_wohnflaeche# m²
d_F = 1

d_s1_lambda, d_s1_d = 0.5, 0.1              # (W/mK, m) vegetation
d_s2_lambda, d_s2_d = 1.8, d_earthwall      # (W/mK, m) Compacted earth
d_s3_lambda, d_s3_d = 0.15, 0.3             # (W/mK, m) studs
d_s4_lambda, d_s4_d = 0.04, 0.15            # (W/mK, m) Insulation

d_s1_R = d_s1_d / d_s1_lambda               # (m^2*K)/W
d_s2_R = d_s2_d / d_s2_lambda               # (m^2*K)/W
d_s3_R = d_s3_d / d_s3_lambda               # (m^2*K)/W
d_s4_R = d_s4_d / d_s4_lambda               # (m^2*K)/W

# --- Floor ---
b_A = hoehe_wohnflaeche * breite_wohnflaeche# m²
b_F = 0.6

b_s1_lambda, b_s1_d = 1.8, d_earthwall      # (W/mK, m) Compacted earth
b_s2_lambda, b_s2_d = 0.04, 0.15            # (W/mK, m) Insulation
b_s3_lambda, b_s3_d = 0.15, 0.02            # (W/mK, m) wooden floor

b_s1_R = b_s1_d / b_s1_lambda               # (m^2*K)/W
b_s2_R = b_s2_d / b_s2_lambda               # (m^2*K)/W
b_s3_R = b_s3_d / b_s3_lambda               # (m^2*K)/W

# --- Windows ---
f_A_s = laenge_wohnflaeche                  # m²
f_F = 1

f_U_ges = 3                                 # W/(m²K)
solar_transmittance = 0.6                   # = g_senkrecht
#F_W = 0.9                                   # 0.9, Abminderung nicht senkrechter Einfall
F_C = 1                                     # Abminderung Sonnenschutz
F_S = 0.9                                   # Abminderung Verschattung
F_F = 0.7                                   # Abminderung Rahmen

# --- Heat Bridges and Total Area ---
delta_U_WB = 0.05                           # W/(m^2*K)
A_huell = w_A_ges + f_A_s + b_A + d_A       # m^2, inside/outside?

# --- Wintergarden Effect ---
wintergarden_effect = 0.3                   # --, 30% Minderung des Wärmeverlusts an Fensterfront

# --- Internal Gains ---
internal_gains_day = 500                    # W
internal_gains_night = 200                  # W

# --- Ventilation Properties ---
ventilation_rate_day = 0.3                  # Air Changes per Hour (ACH)
ventilation_rate_night = 1.0                # ACH
air_density = 1.225                         # kg/m³
specific_heat_air = 1005                    # J/(kg.K)

# --- Solar Properties ---
thermal_mass_absorption = 0.7               # --, 70% der Solarenergie geht ins Speichermaterial
thermal_mass_release_factor = 0.1           #0.1           # --, 10% wird pro Zeitschritt (Stunde) wieder abgegeben
sun_threshold_deg_min = 10                  # below= full gain, adjust based on building geometry
sun_threshold_deg_max = 60                  # above = no gain, adjust based on building geometry




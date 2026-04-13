import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plot_debug = False
remove_wafer_background = True

sample_data_path = "field_cooling_sample.dat"
wafer_data_path = "field_cooling_wafer.dat"

def read_csv_to_json(csv_file_path):
    df = pd.read_csv(csv_file_path, keep_default_na=False)      # keep_default_na = True: return NaN if empty; keep_default_na = False: return '' if empty
    return df.to_dict(orient='records')


""" read data """
wafer_data = read_csv_to_json(wafer_data_path)
sample_data = read_csv_to_json(sample_data_path)

""" field cooling ============================================ """
""" wafer """
# filter data
wafer_data_field = [d for d in wafer_data if d["Magnetic Field (Oe)"] > 4900]
wafer_data_temp_field = np.array([d["Temperature (K)"] for d in wafer_data_field])
wafer_data_moment_field = np.array([d["Moment (emu)"] for d in wafer_data_field])

# trendline
wafer_field_degree = 9
coeffs = np.polyfit(wafer_data_temp_field, wafer_data_moment_field, wafer_field_degree)
x_range = np.linspace(wafer_data_temp_field.min(), wafer_data_temp_field.max(), 400)
print(f"Polynomial coefficients: {coeffs}")

# get trend functions
wafer_field_cooling_trend_func = np.poly1d(coeffs)

# plot graph
if plot_debug:
    plt.plot(x_range, wafer_field_cooling_trend_func(x_range), color='red', label=f'Degree {wafer_field_degree} Trend')
    plt.scatter(wafer_data_temp_field, wafer_data_moment_field, label="Wafer Field Cooling")
    plt.xlabel('Temperature (K)')
    plt.ylabel('Moment (emu)')
    plt.legend()
    plt.show()

""" sample """
# filter data
sample_data_field = [d for d in sample_data if d["Magnetic Field (Oe)"] > 4900]
sample_data_temp_field = np.array([d["Temperature (K)"] for d in sample_data_field])
sample_data_moment_field = np.array([d["Moment (emu)"] for d in sample_data_field])

# plot graph
if remove_wafer_background:
    sample_data_moment_field -= wafer_field_cooling_trend_func(sample_data_temp_field)

if plot_debug:
    plt.scatter(sample_data_temp_field, sample_data_moment_field, label="NiO Sample Field Cooling")
    plt.xlabel('Temperature (K)')
    plt.ylabel('Moment (emu)')
    plt.show()

""" 0 field cooling ============================================ """
""" wafer """
# filter data
wafer_data_0_field = wafer_data[0:1139]
wafer_data_temp_0_field = np.array([d["Temperature (K)"] for d in wafer_data_0_field])
wafer_data_moment_0_field = np.array([d["Moment (emu)"] for d in wafer_data_0_field])

# trendline
wafer_0_field_degree = 5
coeffs = np.polyfit(wafer_data_temp_0_field, wafer_data_moment_0_field, wafer_0_field_degree)
x_range = np.linspace(wafer_data_temp_0_field.min(), wafer_data_temp_0_field.max(), 400)
print(f"Polynomial coefficients: {coeffs}")

# get trend functions
wafer_0_field_cooling_trend_func = np.poly1d(coeffs)

# plot graph
if plot_debug:
    plt.plot(x_range, wafer_0_field_cooling_trend_func(x_range), color='red', label=f'Degree {wafer_0_field_degree} Trend')
    plt.scatter(wafer_data_temp_0_field, wafer_data_moment_0_field, label="Wafer 0 Field Cooling")
    plt.xlabel('Temperature (K)')
    plt.ylabel('Moment (emu)')
    plt.legend()
    plt.show()

""" sample """
# filter data
sample_data_0_field = sample_data[1791:2928]
sample_data_temp_0_field = np.array([d["Temperature (K)"] for d in sample_data_0_field])
sample_data_moment_0_field = np.array([d["Moment (emu)"] for d in sample_data_0_field])

# plot graph
if remove_wafer_background:
    sample_data_moment_0_field -= wafer_0_field_cooling_trend_func(sample_data_temp_0_field)

if plot_debug:
    plt.scatter(sample_data_temp_0_field, sample_data_moment_0_field, label="NiO Sample 0 Field Cooling")
    plt.xlabel('Temperature (K)')
    plt.ylabel('Moment (emu)')
    plt.show()

""" field cooling nad 0 field cooling in one graph """
plt.scatter(sample_data_temp_field, sample_data_moment_field, label="NiO Sample Field Cooling")
plt.scatter(sample_data_temp_0_field, sample_data_moment_0_field, label="NiO Sample 0 Field Cooling")
plt.xlabel('Temperature (K)')
plt.ylabel('Moment (emu)')
plt.grid()
plt.legend()
plt.show()

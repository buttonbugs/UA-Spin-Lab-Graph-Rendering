import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data_path = "10K_hysteresis.csv"
output_path = "10K_hysteresis.png"

def read_csv_to_json(csv_file_path):
    df = pd.read_csv(csv_file_path, keep_default_na=False)      # keep_default_na = True: return NaN if empty; keep_default_na = False: return '' if empty
    return df.to_dict(orient='records')


data = read_csv_to_json(data_path)

data_low_temp = data[3732:10694]
data_low_temp = [d for d in data_low_temp if d["Magnetic Field (Oe)"] > -2000 and d["Magnetic Field (Oe)"] < 2000]

H = np.array([d["Magnetic Field (Oe)"] for d in data_low_temp])
M = np.array([d["Moment (emu)"] for d in data_low_temp])

plt.scatter(H, M)
plt.xlabel('Magnetic Field (Oe)')
plt.ylabel('Moment (emu)')
plt.grid()
plt.savefig(output_path, dpi=300, transparent=False, bbox_inches='tight')
plt.show()
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

hysteresis_data_path = "10K_hysteresis.csv"
save_graph_file_path = "10K_hysteresis_with_inset.png"
separator = "\t"

# Data points

def read_data(data_file_path):
    with open(data_file_path, "r") as data_file:
        data_str = data_file.read()

    xpoints = []
    ypoints = []

    for data_row_str in data_str.split("\n")[1:]:
        data_row = data_row_str.split(separator)
        xpoints.append(float(data_row[2][:-1]))     # [:-1] to remove 'K'
        ypoints.append((float(data_row[0]) + float(data_row[1])) / 2)    # take the absolute value of the exchange bias

    return np.array(xpoints), np.array(ypoints)


def read_csv_to_json(csv_file_path):
    df = pd.read_csv(csv_file_path, keep_default_na=False)      # keep_default_na = True: return NaN if empty; keep_default_na = False: return '' if empty
    return df.to_dict(orient='records')


if __name__ == "__main__":
    """ 10K Hysteresis """
    fig, ax = plt.subplots(figsize=(6, 4))

    hysteresis_data = read_csv_to_json(hysteresis_data_path)

    hysteresis_data_low_temp = hysteresis_data[3732:10694]
    hysteresis_data_low_temp = [d for d in hysteresis_data_low_temp if d["Magnetic Field (Oe)"] > -2000 and d["Magnetic Field (Oe)"] < 1000]

    H = np.array([d["Magnetic Field (Oe)"] for d in hysteresis_data_low_temp])
    M = np.array([d["Moment (emu)"] for d in hysteresis_data_low_temp])

    ax.scatter(H, M)
    ax.set_xlabel('Magnetic Field (Oe)')
    ax.set_ylabel('Moment (emu)')
    ax.grid(linewidth = 0.3)

    """ Inset """
    ax_inset = ax.inset_axes([0.16, 0.58, 0.4, 0.4])
    xpoints, ypoints = read_data("Hc_Temp_1.txt")
    ax_inset.plot(xpoints, ypoints, color = "red", marker='s', markersize=3, linewidth = 1)

    xpoints, ypoints = read_data("Hc_Temp_2.txt")
    ax_inset.plot(xpoints, ypoints, color = "blue", marker='s', markersize=3, linewidth = 1)
    # plt.legend()      # Show legend
    ax_inset.set_xlabel("Temperature (K)")
    ax_inset.set_ylabel("Exchange bias (Oe)")
    ax_inset.set_ylim(-400, 400)
    ax_inset.grid(linewidth = 0.2)
    plt.savefig(save_graph_file_path, dpi=300, transparent=False, bbox_inches='tight')
    # plt.show()

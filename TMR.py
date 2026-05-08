import matplotlib.pyplot as plt
import numpy as np
import math
import pandas as pd

TMR_data_file_path = "TMR.txt"
hysteresis_10K_data_path = "TMR_inset_10K.txt"
hysteresis_300K_data_path = "TMR_inset_300K.txt"

sample_volume = 0.000000148152

TMR_data_separator = "\t"

# Data points

def read_data():
    with open(TMR_data_file_path, "r") as data_file:
        data_str = data_file.read()

    xpoints = []
    ypoints = []

    for data_row_str in data_str.split("\n")[1:]:
        data_row = data_row_str.split(TMR_data_separator)
        if len(data_row) == 3:
            xpoints.append(float(data_row[0]))
            ypoints.append(abs(float(data_row[1])))

    return np.array(xpoints), np.array(ypoints)

def read_csv_to_json(csv_file_path):
    df = pd.read_csv(csv_file_path, sep='\t', keep_default_na=False)      # keep_default_na = True: return NaN if empty; keep_default_na = False: return '' if empty
    return df.to_dict(orient='records')

def plot_R(xpoints, ypoints):

    # Plot the points and connect with a line
    plt.plot(xpoints, ypoints, color= "black", marker='s')
    plt.grid(True)

    # Add labels and a title
    plt.xlabel("Applied Field (Oe)")
    plt.ylabel("Resistance (Ω)")
    # plt.yscale('log') # Set the y-axis to logarithmic scale
    # plt.title("Resistance - Applied Field")

    plt.savefig("TMR_R.png", dpi=300, transparent=False, bbox_inches='tight')

    # Display the plot
    # plt.show()

def plot_TMR(xpoints, ypoints, axis: plt.Axes):

    # Plot the points and connect with a line
    axis.plot(xpoints, ypoints, color= "black", marker='s')
    axis.grid(linewidth = 0.3)

    # Add labels and a title
    axis.set_xlabel("Applied Field (Oe)")
    axis.set_ylabel("TMR (%)")
    axis.set_xlim(-500, 600)
    # plt.yscale('log') # Set the y-axis to logarithmic scale
    # plt.title("TMR")


def plot_RA(xpoints, ypoints):

    # Plot the points and connect with a line
    plt.plot(xpoints, ypoints, color= "black", marker='s')
    plt.grid()

    # Add labels and a title
    plt.xlabel("Applied Field (Oe)")
    plt.ylabel("RA (MΩ μm$^2$)")

    plt.savefig("TMR_RA.png", dpi=300, transparent=False, bbox_inches='tight')
    # plt.show()

def plot_hysteresis(axis: plt.Axes):
    """ 10K """
    hysteresis_10K_data = read_csv_to_json(hysteresis_10K_data_path)

    H_10K = np.array([d["Magnetic Field (Oe)"] for d in hysteresis_10K_data])
    Moment_10K = np.array([d["Moment (emu)"] for d in hysteresis_10K_data])

    Magnetization_10K = Moment_10K / sample_volume
    axis.plot(H_10K, Magnetization_10K / 1000, color="blue", marker='s', markersize=3, label="10K")

    """ 300K """
    hysteresis_300K_data = read_csv_to_json(hysteresis_300K_data_path)

    H_300K = np.array([d["Magnetic Field (Oe)"] for d in hysteresis_300K_data])
    Moment_300K = np.array([d["Moment (emu)"] for d in hysteresis_300K_data])

    Magnetization_300K = Moment_300K / sample_volume
    axis.plot(H_300K, Magnetization_300K / 1000, color="red", marker='s', markersize=3, label="300K")

    """ General """
    axis.legend()
    axis.set_xlabel('Magnetic Field (Oe)')
    axis.set_ylabel('Magnetization ($10^3$ emu/cm$^3$)')
    axis.set_xlim(-350, 350)
    axis.grid(linewidth = 0.2)

if __name__ == "__main__":
    field, resistance = read_data()
    field -= 40.0       # An artifact that comes from the measurement
    # plot_R(field, resistance)
    R_p = np.min(resistance)
    # plot_RA(field, resistance / 1000 * math.pi * 100**2)

    """ TMR """
    fig, ax = plt.subplots(figsize=(6, 4))

    plot_TMR(field, (resistance-R_p)/R_p*100, ax)

    ax_inset = ax.inset_axes([0.65, 0.38, 0.35, 0.4])
    plot_hysteresis(ax_inset)

    # Save the plot
    plt.savefig("TMR_TMR.png", dpi=300, transparent=False, bbox_inches='tight')

    # Display the plot
    plt.show()
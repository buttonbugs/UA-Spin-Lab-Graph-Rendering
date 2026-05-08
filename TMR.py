import matplotlib.pyplot as plt
import numpy as np
import math

data_file_path = "TMR.txt"
separator = "\t"

# Data points

def read_data():
    with open(data_file_path, "r") as data_file:
        data_str = data_file.read()

    xpoints = []
    ypoints = []

    for data_row_str in data_str.split("\n")[1:]:
        data_row = data_row_str.split(separator)
        if len(data_row) == 3:
            xpoints.append(float(data_row[0]))
            ypoints.append(abs(float(data_row[1])))

    return np.array(xpoints), np.array(ypoints)


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
    plt.show()

def plot_TMR(xpoints, ypoints):

    # Plot the points and connect with a line
    plt.plot(xpoints, ypoints, color= "black", marker='s')
    plt.grid(True)

    # Add labels and a title
    plt.xlabel("Applied Field (Oe)")
    plt.ylabel("TMR (%)")
    # plt.yscale('log') # Set the y-axis to logarithmic scale
    # plt.title("TMR")

    plt.savefig("TMR_TMR.png", dpi=300, transparent=False, bbox_inches='tight')

    # Display the plot
    plt.show()

def plot_RA(xpoints, ypoints):

    # Plot the points and connect with a line
    plt.plot(xpoints, ypoints, color= "black", marker='s')
    plt.grid(True)

    # Add labels and a title
    plt.xlabel("Applied Field (Oe)")
    plt.ylabel("RA (MΩ μm$^2$)")
    # plt.yscale('log') # Set the y-axis to logarithmic scale
    # plt.title("RA")

    plt.savefig("TMR_RA.png", dpi=300, transparent=False, bbox_inches='tight')

    # Display the plot
    plt.show()

if __name__ == "__main__":
    field, resistance = read_data()
    field -= 40.0       # An artifact that comes from the measurement
    plot_R(field, resistance)
    R_p = np.min(resistance)
    plot_TMR(field, (resistance-R_p)/R_p*100)
    plot_RA(field, resistance / 1000 * math.pi * 100**2)

import matplotlib.pyplot as plt
import numpy as np

save_graph_file_path = "Hc_Temp.png"
data_file_path = "Hc_Temp.txt"
separator = "\t"

# Data points

def read_data():
    with open(data_file_path, "r") as data_file:
        data_str = data_file.read()

    xpoints = []
    ypoints = []

    for data_row_str in data_str.split("\n")[1:]:
        data_row = data_row_str.split(separator)
        xpoints.append(float(data_row[2][:-1]))     # [:-1] to remove 'K'
        ypoints.append((float(data_row[0]) + float(data_row[1])) / 2)    # take the absolute value of the exchange bias

    return np.array(xpoints), np.array(ypoints)


def plot_data(xpoints, ypoints):

    # Plot the points and connect with a line
    plt.plot(xpoints, ypoints, color= "black", marker='s')
    plt.grid(True)

    # Add labels and a title
    plt.xlabel("Temperature (K)")
    plt.ylabel("Exchange bias (Oe)")
    # plt.yscale('log') # Set the y-axis to logarithmic scale
    # plt.title("Exchange bias - temperature")

    plt.savefig(save_graph_file_path, dpi=300, transparent=False, bbox_inches='tight')

    # Display the plot
    plt.show()

if __name__ == "__main__":
    xpoints, ypoints = read_data()
    plot_data(xpoints, ypoints)

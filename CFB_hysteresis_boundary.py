import numpy as np
import pandas as pd
from sklearn.mixture import GaussianMixture

'''
Installation Requirement:
pip install scikit-learn

'''

sample_volume = 1.334e-7

CFB_hysteresis_data_path = "CFB_hysteresis.txt"

def read_csv_to_json(csv_file_path):
    df = pd.read_csv(csv_file_path, sep='\t', keep_default_na=False)      # keep_default_na = True: return NaN if empty; keep_default_na = False: return '' if empty
    return df.to_dict(orient='records')

def calculate_charateristic(x_values: np.ndarray, y_values: np.ndarray):

    center_y = np.average(get_gmm_peaks(y_values))
    x_intersections = get_polygon_horizontal_intersection(x_values, y_values, center_y)

    if len(x_intersections) > 0:
        left_x_intersection = x_intersections[0]
        right_x_intersection = x_intersections[-1]
    else:
        average_x = np.average(x_values)
        left_x_intersection = average_x
        right_x_intersection = average_x

    return left_x_intersection, right_x_intersection, (right_x_intersection - left_x_intersection) / 2, (right_x_intersection + left_x_intersection) / 2, (np.max(x_values) - np.min(x_values)) / 2

def get_polygon_horizontal_intersection(x: np.ndarray, y: np.ndarray, y_line: float | np.float64):
    """
    Calculate the intersection of a polygon and a horizontal line.`

    Args:
        x (np.ndarray): A numpy array of x values of the polygon.
        y (np.ndarray): A numpy array of y values of the polygon.
        y_line (float | np.float64): The y value of the horizontal line.

    Returns:
        np.ndarray: A numpy array of x values of the intersections in ascending order
    """

    # Ensure the polygon is closed by appending the first point to the end
    x = np.append(x, x[0])
    y = np.append(y, y[0])

    x1 = x[:-1]
    y1 = y[:-1]
    x2 = x[1:]
    y2 = y[1:]

    # Check if (x1, y1) and (x2, y2) are on different side of y_line
    cross_mask = ((y1 >= y_line) != (y2 >= y_line)) & (y1 != y2)

    x1 = x1[cross_mask]
    y1 = y1[cross_mask]
    x2 = x2[cross_mask]
    y2 = y2[cross_mask]

    x_intersections = x1 + (y_line - y1) * (x2 - x1) / (y2 - y1)

    return np.sort(x_intersections)

def get_gmm_peaks(x_values: np.ndarray, num_of_peaks: int = 2, random_state: int = 42):
    """
    Generate the position of the two peaks

    Args:
        x_values (np.ndarray): An 1D numpy array of x values
        num_of_peaks (int): Num of peaks of the Gaussian mixture
        random_state (int): The seed for initial random guess

    Returns:
        np.ndarray: An array of peaks
    """

    x_column = x_values.reshape(-1, 1)
    gmm = GaussianMixture(n_components=num_of_peaks, random_state=random_state)
    gmm.fit(x_column)

    return gmm.means_.flatten()

def draw_CFB_hysteresis():
    CFB_hysteresis_data = read_csv_to_json(CFB_hysteresis_data_path)

    magnetic_field = np.array([d["Magnetic Field (Oe)"] for d in CFB_hysteresis_data])
    magnetization = np.array([d["Moment (emu)"] for d in CFB_hysteresis_data]) / sample_volume

    analysis_results = calculate_charateristic(magnetic_field, magnetization)

    print("Switching Field (Left) (kG)", analysis_results[0])
    print("Switching Field (Right) (kG)", analysis_results[1])
    print("Relative Switching Field (kG)", analysis_results[2])
    print("Exchange Bias (kG)", analysis_results[3])
    print("Field Range (kG)", analysis_results[4])

if __name__ == "__main__":

    draw_CFB_hysteresis()
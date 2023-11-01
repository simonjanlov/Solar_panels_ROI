import pandas as pd
import os

def find_tilt_and_direction_value(tilt, direction):
    """Input tilt as an integer and direction as a string to return a
    float value for combined tilt and direction"""

    # Determine the directory of your current script
    current_dir = os.path.dirname(os.path.realpath(__file__ if '__file__' in globals() else sys.executable))
    data_dir = os.path.join(current_dir, "data")  # Define the data directory path

    # Use an absolute path to load the CSV file
    df = pd.read_csv(os.path.join(data_dir, 'tilt_and_direction_table.csv'), delimiter=';', index_col='Lutning')
    return df[direction][tilt] / 100

if __name__ == '__main__':
    print(find_tilt_and_direction_value(20, '225 SV'))

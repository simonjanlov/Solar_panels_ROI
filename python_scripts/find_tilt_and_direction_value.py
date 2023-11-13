import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path('.').absolute().parent) + '\\Solar_panels_ROI')

from config2 import *


def find_tilt_and_direction_value(tilt, direction):
    """Input tilt as an integer and direction as a string to return a
    float value for combined tilt and direction"""
    
    df = pd.read_csv(tilt_and_direction_table_csvpath, delimiter=';', index_col='Lutning')
    return df[direction][tilt] / 100



if __name__=='__main__':
    print(find_tilt_and_direction_value(20, '225 SV'))

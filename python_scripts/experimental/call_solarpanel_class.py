import sys
import pandas as pd

sys.path.append(r'python_scripts')

from electricity_output_calc import SolarPanelSystem
from find_tilt_and_direction_value import find_tilt_and_direction_value


# This script allows us to test run the SolarPanelSystem class and its methods with user input

price = int(input("Input system price (SEK): "))
system_effect = float(input("Input system effect (kWp): "))
insolation = float(input("Input your location's average yearly insolation: "))
tilt_and_direction = find_tilt_and_direction_value(int(input("Input tilt: ")), input("Input direction: "))

my_system = SolarPanelSystem(price, system_effect, insolation, tilt_and_direction=tilt_and_direction)
    
mockup_electricity_prices = [1.02, 0.52, 0.49, 1.03, 0.89, 
                             0.98, 0.59, 0.42, 0.38, 0.36, 
                             0.48, 0.66, 0.94, 0.82, 0.39, 
                             0.31, 0.84, 0.57, 0.84, 0.46, 
                             0.45, 0.34, 0.66, 0.64, 0.97, 
                             0.39, 0.88, 0.35, 0.8, 0.33]

electricity_prices_df = pd.read_csv(r'data\predicted_prices_withzones.csv')
predicted_prices = list(electricity_prices_df['zone1'])
    
# print(my_system.calc_yearly_electricity_output())
# print(my_system.electricity_cost_saved_per_year(0.98))

# print(my_system.profitability_over_time(mockup_electricity_prices))
print(my_system.profitability_over_time(predicted_prices))

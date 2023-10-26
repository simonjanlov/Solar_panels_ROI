import sys

sys.path.append(r'C:\projekt\slutprojekt\final_project\python_scripts')

from electricity_output_calc import SolarPanelSystem

price = int(input("Input system price (SEK): "))
system_effect = float(input("Input sytstem effect (kWp): "))
insolation = float(input("Input your location's average yearly insolation: "))

my_system = SolarPanelSystem(price, system_effect, insolation)
    
mockup_electricity_prices = [1.02, 0.52, 0.49, 1.03, 0.89,
                             0.98, 0.59, 0.42, 0.38, 0.36, 
                             0.48, 0.66, 0.94, 0.82, 0.39, 
                             0.31, 0.84, 0.57, 0.84, 0.46]
    
# print(my_system.calc_yearly_electricity_output())
# print(my_system.electricity_cost_saved_per_year(0.98))

print(my_system.profitability_over_time(mockup_electricity_prices))

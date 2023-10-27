
years = [2010, 2011, 2012, 2013, 2014, 2015]
profits = [-5000, -3000, -1000, 500, 2000, 4000]

# Find the index where the profit crosses zero
negative_index = next((i for i, profit in enumerate(profits) if profit < 0), None)
positive_index = next((i for i, profit in enumerate(profits) if profit >= 0), None)


if negative_index is not None and positive_index is not None:
    # Linear interpolation to estimate the year when profit becomes zero
    x1, x2 = profits[negative_index], profits[positive_index]
    year_at_zero_profit = years[negative_index] + (years[positive_index] - years[negative_index]) * (0 - x1) / (x2 - x1)
    print(float(f"{year_at_zero_profit - years[0]:.1f}"))
    # return float(f"{year_at_zero_profit - years[0]:.1f}")
else:
    print("Couldn't calculate ")
    # return -1
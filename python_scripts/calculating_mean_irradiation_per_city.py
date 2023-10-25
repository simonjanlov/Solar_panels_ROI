import pandas as pd
from clean_raw_file import *


df_lulea = clean_raw_file('C:\\Users\\henry\\Documents\\projekt\\examens_proj\\final_project\\data\\Monthlydata_ghi_luleå_2005_2020.csv')
df_malmo = clean_raw_file('C:\\Users\\henry\\Documents\\projekt\\examens_proj\\final_project\\data\\Monthlydata_ghi_malmo_2005_2020.csv')
df_stockholm = clean_raw_file('C:\\Users\\henry\\Documents\\projekt\\examens_proj\\final_project\\data\\Monthlydata_ghi_stockholm_2005_2020.csv')
df_sundsvall = clean_raw_file('C:\\Users\\henry\\Documents\\projekt\\examens_proj\\final_project\\data\\Monthlydata_ghi_sundsvall_2005_2020.csv')

df_lulea_sum_ghi = df_lulea.groupby('year').sum('ghi')
df_malmo_sum_ghi = df_malmo.groupby('year').sum('ghi')
df_stockholm_sum_ghi = df_stockholm.groupby('year').sum('ghi')
df_sundsvall_sum_ghi = df_sundsvall.groupby('year').sum('ghi')

avg_ghi_lulea = df_lulea_sum_ghi.ghi.mean()
avg_ghi_malmo = df_malmo_sum_ghi.ghi.mean()
avg_ghi_stockholm = df_stockholm_sum_ghi.ghi.mean()
avg_ghi_sundsvall = df_sundsvall_sum_ghi.ghi.mean()
print(avg_ghi_lulea)


import pandas as pd


def clean_and_find_avg_ghi(file_path):
    """Function that takes file path(what file to read) as arguments
    and reads the csv, drop unnessery info and rename column and returns a avg ghi"""
    df = pd.read_csv(file_path, sep='\t\t',engine='python')
    df.drop(df.index[-3:],inplace=True)
    df.rename(columns={'H(h)_m':'ghi'},inplace=True) # ghi = global horizontal irradiation
    df_sum_ghi = df.groupby('year').sum('ghi')
    avg_ghi = df_sum_ghi.ghi.mean()

    return avg_ghi






if __name__ == "__main__":
    print(clean_and_find_avg_ghi("C:\\Users\\henry\\Downloads\\Monthlydata_65.683_22.167_E5_2005_2020.csv"))
   




import pandas as pd


def clean_raw_file(file_path,folder_path):
    """Function that takes file path(what file to read) and file_name(what name you want to save as) as arguments
    and reads the csv, drop unnessery info and rename column"""
    df = pd.read_csv(file_path, sep=',',header=3)
    df.drop([192,193],inplace=True)
    df.rename(columns={'H(h)_m':'ghi'},inplace=True) # ghi = global horizontal irradiation
    df.to_csv(folder_path + '')
    return df

if __name__ == "__main__":
    df=clean_raw_file('Monthlydata_55.703_13.192_SA2_2005_2020.csv')
    print(df)

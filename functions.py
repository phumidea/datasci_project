import pandas as pd
from datetime import datetime, timedelta
from time import time
import matplotlib.pyplot as plt

def pm_data(city):
    with open(city) as f:
        lines = f.read().splitlines()
        
    info = lines[:9]
    conv = lambda x: (x[0].replace("% ",""), [x[1]])
    info = dict(conv(i.split(': ')) for i in info)
    info_df = pd.DataFrame.from_dict(info)

    columns = lines[9].replace("% ","").split(", ")
    data = lines[10:]
    data = [d.split("\t") for d in data]
    df = pd.DataFrame(data,columns=columns)
    datetime_data = pd.to_datetime(dict(year = df.Year, month =df.Month, day = df.Day, hour = df["UTC Hour"])) + timedelta(hours = 7)
    df.insert(0, 'datetime', datetime_data)
    return info_df,df

def check_null_all(df):
    null_counts = df.isnull().sum()
    print(f"Number of null values in each column:\n{null_counts}")

def check_city_feature_unique(df, headers, city):
    print("-"*30)
    for header in headers:
        print(city + " " + header)
        print(df[header].unique())
        print("-"*30)

def trend_each_year(df,col):
    years = df["Year"].unique()
    month_range = df.groupby('Year').agg({'Month': ['min','max']})
    month_range = month_range.to_dict()
    for year in years:
        df_plot = df[df["Year"] == year].groupby(["Month"]).mean()

        min_month,max_month = month_range[('Month', 'min')][year],month_range[('Month', 'max')][year]
        plt.plot([i for i in range(min_month,max_month + 1)], df_plot[col], label = f"Year {year}")

    plt.legend()
    plt.show()

def extract_date_string(df):    
    df["Year"] = df["datetime"].apply(lambda x: int(x[:4]))
    df["Month"] = df["datetime"].apply(lambda x: int(x[5:7]))
    df["Day"] = df["datetime"].apply(lambda x: int(x[8:10]))
    df["UTC Hour"] = df["datetime"].apply(lambda x: int(x[11:13]))
    return df
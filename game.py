import pandas as pd
import numpy as np

f=pd.read_csv('data/citibike-tripdata.csv', sep=',')
f_base = f.copy()

f.drop(['end station id', 'start station id'], axis=1, inplace=True)

f['age'] = 2018 - f['birth year']
f.drop('birth year', axis=1, inplace=True)

# print(f[f['age'] > 60].count())

f['starttime'] = pd.to_datetime(f['starttime'])
f['stoptime'] = pd.to_datetime(f['stoptime'])

f['trip duration'] = f['stoptime'] - f['starttime']
f['trip duration'] = f['trip duration'].dt.seconds

f['weekend'] = f['starttime'].dt.dayofweek
f['weekend'] = f['weekend'].apply(lambda x: 1 if x == 5 or x == 6 else 0)

def tod(x):
    if x <=6 and x >=0:
        return 'night'
    elif 6< x <=12:
        return 'morning'
    elif 12 < x <=18:
        return 'day'
    else: 
        return 'evening'

f['time_of_day'] = f['starttime'].dt.hour.apply(tod)
print(f[f['time_of_day'] == 'day']['time_of_day'].count()/f[f['time_of_day'] == 'night']['time_of_day'].count())
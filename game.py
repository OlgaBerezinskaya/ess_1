import pandas as pd

melb_data = pd.read_csv('data/melb_data.csv', sep=',')
melb_data['Postcode'] = melb_data['Postcode'].astype('int64')
melb_data['Car'] = melb_data['Car'].astype('int64')
melb_data['Bedroom'] = melb_data['Bedroom'].astype('int64')
melb_data['Bathroom'] = melb_data['Bathroom'].astype('int64')
melb_data['Propertycount'] = melb_data['Propertycount'].astype('int64')
melb_data['YearBuilt'] = melb_data['YearBuilt'].astype('int64')
# print(melb_data.describe().loc[:, ['Distance', 'BuildingArea' , 'Price']])
# print(melb_data.describe(include=['int64']))
# print( melb_data.info())
# print(melb_data['Type'].value_counts())
# print(melb_data['Propertycount'].max())
f = melb_data.copy()
f = f.drop(['index', 'Coordinates'], axis=1)
f['Date'] = pd.to_datetime(f['Date'])
f['MonthSale'] = f['Date'].dt.month
delta = f['Date'] - pd.to_datetime('2016-01-01') # – разница в днях между фикс датой и датой

AgeBuilding = f['Date'].dt.year - f['YearBuilt']

f['WeekdaySale'] = f['Date'].dt.dayofweek
su = f[(f['WeekdaySale'] == 5) | (f['WeekdaySale'] == 6)]['Price'].sum()
su1 = f[f['WeekdaySale'] == 5]['WeekdaySale'].sum()/5 +f[f['WeekdaySale'] == 6]['WeekdaySale'].sum()/6
        
        
        

serf = f['SellerG'].value_counts()[:49]

f['SellerG'] = f['SellerG'].apply(lambda x: x if x in serf else 'other')

 

print(f[f['SellerG'] == 'Nelson']['Price'].min() / f[f['SellerG'] == 'other']['Price'].min())


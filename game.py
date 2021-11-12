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
# 1075684.079455081
# print(melb_data.describe(include=['float64']))
pr = melb_data['Price'].mean()
print(melb_data[(melb_data['Type']=='h')&(melb_data['Price']<3000000)]['Regionname'].value_counts())



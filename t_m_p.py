import pandas as pd

f=pd.read_csv('data/countries.csv', sep=';')
f1 = pd.read_csv('data/melb_data.csv', sep=',')
f2 = pd.read_csv('data/students_performance.csv', sep=',')

unique_list = []
for el in f1.columns:
    unique_list.append([el, f1[el].nunique(),f1[el].dtype])
    
unique_counts = pd.DataFrame(
    unique_list,
    columns=['Column_Name', 'Num_Unique', 'Type']
).sort_values(by='Num_Unique', ignore_index=True)

#print(unique_counts)

cols_to_exclude = ['Date', 'Rooms', 'Bedroom', 'Bathroom', 'Car']
max_unique_count = 150
for el in f1.columns: # цикл по именам столбцов
    if f1[el].nunique() < max_unique_count and el not in cols_to_exclude: # проверяем условие
        f1[el] = f1[el].astype('category') # преобразуем тип столбца
print(f1.info()) 
print('*'*20)
sub_new = f1['Suburb'].value_counts().nlargest(119).index
f1['Suburb'] = f1['Suburb'].apply(lambda x: x if x in sub_new else 'other') 
cols_to_exclude = ['Date', 'Rooms', 'Bedroom', 'Bathroom', 'Car']
max_unique_count = 150
for el in f1.columns: # цикл по именам столбцов
    if f1[el].nunique() < max_unique_count and el not in cols_to_exclude: # проверяем условие
        f1[el] = f1[el].astype('category') # преобразуем тип столбца
print(f1.info()) 

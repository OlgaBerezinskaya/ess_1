import pandas as pd

ev = pd.read_csv('data/events.csv', sep=',')
pur = pd.read_csv('data/purchase.csv', sep=',')


cond1=(ev['event_type']=='registration')&(ev['start_time']>='2018-01-01')&(ev['start_time']<'2019-01-01') # рега-2018
spisok_users=ev[cond1]['user_id'].to_list()  #список с номерами юзеров с регой 2018
ev = ev[ev['user_id'].isin(spisok_users)] # новый файл, в котором только юзеры с регой 2018 г.    66959 строк    38/4/1 ДА
# print(ev.info)

ev['start_time'] = pd.to_datetime(ev['start_time'])       # преобразование даты
var1 = ev['selected_level']                                # 8342 непустых значений в столбце selected_level 38/4/2 ДА
# print(var1.describe())

cnt_reg = ev[ev['event_type'] == 'registration']['user_id'].nunique()   # все id юзеров с регой-2018    19926 38/4/3, 38/5/1  ДА
cnt_tut = ev[ev['event_type'] == 'tutorial_start']['user_id'].nunique() # Какое колво юзеров совершает событие tutorial_start 11858  38/5/2 ДА 
cnt_fin = ev[ev['event_type'] == 'tutorial_finish']['user_id'].nunique() # все id юзеров с концом учебы 10250 38/5/2 ДА
cnt_lev = ev[ev['event_type'] == 'level_choice']['user_id'].nunique() # все id юзеров с выборомвопр 8342 38/5/3 ДА
cnt_pac = ev[ev['event_type'] == 'pack_choice']['user_id'].nunique() # все id юзеров с началом учебы 5737 38/5/6 ДА 
# print(cnt_reg, cnt_tut, cnt_fin, cnt_lev, cnt_pac, sep='\n')

pur['event_datetime'] = pd.to_datetime(pur['event_datetime'])   # преобразование даты
pur = pur[pur['user_id'].isin(spisok_users)]    # новый файл, в котором только юзеры с регой-2018   1600 строк   38/4/4 ДА
# print(pur)                  

var2 = pur['amount'].mean() # среднее значение в столбце amount 110.73 38/4/6 ДА
# print(var2)      

var3 = round(cnt_tut*100/cnt_reg, 2) # Какой % юзеров, начавших обучение (от общего числа зарегистрировавшихся)? 59.51 38/5/3 ДА
# print(var3)

var4 = round(cnt_fin*100/cnt_tut, 2) # Какой % юзеров, завершивших обучение (от числа начавших обучение)? 86.44 38/5/4 ДА
# print(var4)

var5 = round(cnt_lev*100/cnt_reg, 2) # Какой % юзеров, выбравших уровень сложности (от общего числа зарегистрировавшихся)? 41.86 38/5/5 ДА
# print(var5)

var6 = round(cnt_pac*100/cnt_lev, 2) # Какой % юзеров, выбравших пакет бесплатных вопросов (от числа выбравших уровень сложности)? 68.77 38/5/6 ДА
# print(var6)

cnt_pur = pur['user_id'].nunique()                                  # Сколько пользователей купили пакеты вопросов? 1600 38/5/7 ДА
# print(cnt_pur)

var7 = round(cnt_pur*100/cnt_reg, 2) # Какой % юзеров, оплативших пакеты вопросов (от числа зарегистрировавшихся пользователей)? 8.03 38/5/8 ДА
# print(var7)

pur['event_type'] = 'purchase'
ev = ev.rename(columns={"id": "event_id"})
pur = pur.rename(columns={"id": "purchase_id"})
total_ev = pd.concat([ev,pur],sort=False)  # объединили две таблицы, 68559 строк 9 столбцов 38/6/1 ДА
total_ev = total_ev.reset_index(drop=True).sort_values('start_time')
# print(total_ev) 

user_path_df = total_ev.groupby(["user_id"])["event_type"].apply(list).reset_index() # формирование списка путей
# print(user_path_df)
user_path_df = user_path_df['event_type'].apply(lambda x: ' >> '.join(x)) # оформили пути в строки
# print(user_path_df)
var8 = user_path_df.value_counts() # группировка по строкам - частота реализации путей
# print(var8.head(10)) # 10 лучших, purchase N 5 и единственный, 1083 случая 38.6.2 ДА
var9 = var8[var8.index.str.contains('purchase')].head(10) # 10 лучших, заканчивающихся purchase
# print(var9)

reg = total_ev[total_ev['event_type'] == 'registration'] # таблица с регистрацией только
reg = reg[['user_id', 'start_time']].rename(columns={'start_time':'registration_time'}) # оставили только id и время
# print(reg)

tut = total_ev[total_ev['event_type'] == 'tutorial_start'] # таблица с началом учебы только
tut = tut.sort_values('start_time').drop_duplicates('user_id')  # удалили повторные обучения
tut = tut[['user_id', 'start_time', 'tutorial_id']].rename(columns={'start_time':'tut_time'}) # оставили только id и время
# print(tut)

# объединяем регистрацию и начало учебы
merge1 = reg.merge(tut, on='user_id', how='inner')
merge1['timedelta'] = merge1['tut_time'] - merge1['registration_time']
# print(merge1['timedelta'].describe())

tuf = total_ev[total_ev['event_type'] == 'tutorial_finish'] # таблица с концом учебы только
tuf = tuf[tuf['tutorial_id'].isin(merge1['tutorial_id'])] # оставили только финалы обучений, учтенных ранее
tuf = tuf[['user_id', 'start_time']].rename(columns={'start_time':'tuf_time'}) # оставили только id и время
# print(tuf)

# объединяем начало и конец учебы
merge2 = tut.merge(tuf, on='user_id', how='inner')
merge2['timedelta'] = merge2['tuf_time'] - merge2['tut_time']
# print(merge2['timedelta'].describe())

lev = total_ev[total_ev['event_type'] == 'level_choice'] # таблица с выбором уровня только
lev = lev[['user_id', 'start_time']].rename(columns={'start_time':'lev_time'}) # оставили только id и время
# print(lev)

# объединяем регистрацию и выбор уровня
merge3 = reg.merge(lev, on='user_id', how='inner')
merge3['timedelta'] = merge3['lev_time'] - merge3['registration_time']
# print(merge3['timedelta'].describe())

pac = total_ev[total_ev['event_type'] =='pack_choice']  # таблица с выбором пакета вопросов только
pac = pac[['user_id', 'start_time']].rename(columns={'start_time': 'pac_time'})     # оставили только id и время
# print(pac) 

# объединяем выбор уровня и выбор пакета вопросов
merge4 = lev.merge(pac, on='user_id', how='inner')
merge4['timedelta'] = merge4['pac_time']- merge4['lev_time'] 
# print(merge4['timedelta'].describe())

purch = total_ev[total_ev['event_type'] =='purchase']  # таблица с оплатой только
purch = purch[['user_id', 'event_datetime']].rename(columns={'event_datetime': 'purch_time'}) 
purch = purch.sort_values('purch_time').drop_duplicates('user_id') # оставили только id и время
# print(purch) 

# объединяем выбор уровня и оплату
merge5 = lev.merge(purch, on='user_id', how='inner')
merge5['timedelta'] = merge5['purch_time']- merge5['lev_time'] 
# print(merge5['timedelta'].describe())


users_tut_fin = total_ev[total_ev['event_type'] == 'tutorial_finish']['user_id'] # номера юзеров, кот хотя бы раз окончили обучение 
users_tut_fin = set(users_tut_fin) # уникальные номера юзеров, кот хотя бы раз окончили обучение 10250 

users_tut_start = total_ev[total_ev['event_type'] == 'tutorial_start']['user_id'] # номера юзеров, кот хотя бы раз начали обучение 
users_tut_start = set(users_tut_start) # уникальные номера юзеров, кот хотя бы раз начали обучение 11858 
# print(len(users_tut_start))

users_no_fin = users_tut_start.difference(users_tut_fin) # уникальные номера юзеров, кот ни разу не окончили обучение 1608 
# print(len(users_no_fin))

users_total = set(total_ev['user_id']) #  уникальные номера юзеров с регой 2018 г. 19926
users_no_tut = users_total.difference(users_tut_start) #  уникальные номера юзеров, кот не начинали учебу 8068
# print(len(users_no_tut))
# 10250 + 1608 + 8068 = 19926

# счет для тех, кто хотя бы 1 раз отучился
pur_tut_fin =  pur[pur['user_id'].isin(users_tut_fin)] # часть баз.таблицы с оплатами по тем, кто окончил обучение 1447строк
# print(pur_tut_fin)
pur_tut_fin_procent = round(pur_tut_fin['user_id'].nunique() * 100/ len(users_tut_fin), 2) # % тех, кто хотя бы 1 раз отучился и заплатил, в отучившихся 14,12 
# print(pur_tut_fin_procent)
sum_tut_fin = pur_tut_fin['amount'].sum() # сумма оплаты тех, кто отучился 160600, или 90,64% от общей
# print(round(pur_tut_fin['amount'].mean(), 2)) # средний платеж тех, кто отучился, 110.99
# print(pur['amount'].mean()) # средний платеж по всем 110.73

# счет для тех, кто начал, но не окончил учебу
# users_no_fin # уникальные номера юзеров, кот ни разу не окончили обучение 1608 
pur_no_fin =  pur[pur['user_id'].isin(users_no_fin)] # часть баз.таблицы с оплатами по тем, кто не окончил обучение 131 строка
# print(pur_no_fin)
pur_no_fin_procent = round(pur_no_fin['user_id'].nunique() * 100/ len(users_no_fin), 2) # % тех, кто заплатил, в неотучившихся 8.15 
# print(pur_no_fin_procent)
sum_no_fin = pur_no_fin['amount'].sum() # сумма оплаты тех, кто неотучился 13750, или 7.76% от общей
# print(round(pur_no_fin['amount'].mean(), 2)) # средний платеж тех, кто не отучился, 104,96
# print(pur['amount'].mean()) # средний платеж по всем 110.73

# счет для тех, кто не начинал учебу
# users_no_tut # уникальные номера юзеров, кот ни разу не начинали обучение 8068
pur_no_tut =  pur[pur['user_id'].isin(users_no_tut)] # часть баз.таблицы с оплатами по тем, кто не начинал обучение 22 строки
# print(pur_no_tut)
pur_no_tut_procent = round(pur_no_tut['user_id'].nunique() * 100/ len(users_no_tut), 2) # % тех, кто заплатил, в неотучившихся 0,27 
# print(pur_no_tut_procent)
sum_no_tut = pur_no_tut['amount'].sum() # сумма оплаты тех, кто неотучился 2825, или 1.59% от общей
# print(sum_no_tut/pur['amount'].sum())
print(round(pur_no_tut['amount'].mean(), 2)) # средний платеж тех, кто не отучился, 128.41
print(pur['amount'].mean()) # средний платеж по всем 110.73
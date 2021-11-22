import pandas as pd

# считываем базовые файлы
ev = pd.read_csv('data/events.csv', sep=',')  # 252334 rows x 6 columns : id > event_type > selected_level > start_time > tutorial_id > user_id 
pur = pd.read_csv('data/purchase.csv', sep=',')   # 5956 rows x 4 columns : id > user_id > event_datetime > amount 

# оставляем только юзеров с регой от 2018 г.
cond1=(ev['event_type']=='registration')&(ev['start_time']>='2018-01-01')&(ev['start_time']<'2019-01-01') # фильтр реги-2018
spisok_users=ev[cond1]['user_id'].to_list()  #список с номерами юзеров с регой-2018
ev = ev[ev['user_id'].isin(spisok_users)] # обновленный файл, в котором только юзеры с регой-2018    66959 rows x 6 columns
pur = pur[pur['user_id'].isin(spisok_users)] # обновленный файл, в котором только юзеры с регой-2018   1600 rows x 4 columns

# преобразовываем даты
ev['start_time'] = pd.to_datetime(ev['start_time'])
pur['event_datetime'] = pd.to_datetime(pur['event_datetime'])

# считаем юзеров, выбравших уровень сложности
ev_cnt_lev = ev[ev['event_type'] == 'level_choice']['user_id']  # 8342 в ev 
pur_cnt_lev = pur[pur['user_id'].isin(ev_cnt_lev)]['user_id'] # 1600 в pur 
# print(ev_cnt_lev)

# составляем списки оригинальных id юзеров, выбравших различные уровни
medium_level = set(ev[ev['selected_level'] == 'medium']['user_id']) # 4645 в ev
easy_level = set(ev[ev['selected_level'] == 'easy']['user_id']) # 2448 в ev
hard_level = set(ev[ev['selected_level'] == 'hard']['user_id']) # 1249 в ev
# print(len(hard_level))

# структура выбранных уровней в ev --  по сложности, все=100%
ev_medium_proc = len(medium_level)*100/ev_cnt_lev.nunique() # 55.68%
ev_easy_proc = len(easy_level)*100/ev_cnt_lev.nunique() # 29.35%
ev_hard_proc = len(hard_level)*100/ev_cnt_lev.nunique() # 14.97%
# print(round(ev_hard_proc, 2))

# проверяем количество оплативших по выбранным уровням  
pur_medium = pur[pur['user_id'].isin(medium_level)] # 969 rows
pur_easy = pur[pur['user_id'].isin(easy_level)] # 189 rows
pur_hard = pur[pur['user_id'].isin(hard_level)] # 442 rows
# print(pur_hard)

# проверяем долю оплативших для каждого выбранного уровня
pur_medium_proc = pur_medium['user_id'].nunique()*100/len(medium_level) # 20.86%
pur_easy_proc = pur_easy['user_id'].nunique()*100/len(easy_level) # 7.72%
pur_hard_proc = pur_hard['user_id'].nunique()*100/len(hard_level) # 35.39%
pur_total_proc = pur_cnt_lev.nunique()*100/ev_cnt_lev.nunique() # по всем уровням 19.18%
print('Процент пользователей, которые выбрали уровень medium и оплатили вопросы:', round(pur_medium_proc, 2))
print('Процент пользователей, которые выбрали уровень easy и оплатили вопросы:', round(pur_easy_proc, 2))
print('Процент пользователей, которые выбрали уровень hard и оплатили вопросы:', round(pur_hard_proc, 2))
print('Процент пользователей, которые выбрали уровень и оплатили вопросы', round(pur_total_proc, 2))
print('*'*50)

# считаем вклад уровней в выручку
sum_medium = pur_medium['amount'].sum() # 106125Rub
sum_easy = pur_easy['amount'].sum() # 21724Rub
sum_hard = pur_hard['amount'].sum() # 49327Rub
sum_total = pur['amount'].sum() # 177175Rub
# print(sum_medium)

# считаем средний платеж по выбранным уровням
av_medium = pur_medium['amount'].mean() # 109.52Rub/us
av_easy = pur_easy['amount'].mean() # 114.95Rub/us
av_hard = pur_hard['amount'].mean() # 111.6Rub/us
av_total = pur['amount'].mean() # 110.73Rub/us
# print(round(av_total, 2))

# определяем момент регистрации
reg_medium = ev[(ev['event_type'] == 'registration') & (ev['user_id'].isin(medium_level))][['start_time', 'user_id']]
reg_easy = ev[(ev['event_type'] == 'registration') & (ev['user_id'].isin(easy_level))][['start_time', 'user_id']]
reg_hard = ev[(ev['event_type'] == 'registration') & (ev['user_id'].isin(hard_level))][['start_time', 'user_id']]
reg_total = ev[(ev['event_type'] == 'registration') & (ev['user_id'].isin(ev_cnt_lev))][['start_time', 'user_id']]
# print(reg_total)

# определяем момент выбора уровня
choice_medium = ev[(ev['event_type'] == 'level_choice') & (ev['user_id'].isin(medium_level))][['start_time', 'user_id']]
choice_easy = ev[(ev['event_type'] == 'level_choice') & (ev['user_id'].isin(easy_level))][['start_time', 'user_id']]
choice_hard = ev[(ev['event_type'] == 'level_choice') & (ev['user_id'].isin(hard_level))][['start_time', 'user_id']]
choice_total = ev[(ev['event_type'] == 'level_choice') & (ev['user_id'].isin(ev_cnt_lev))][['start_time', 'user_id']]
# print(choice_total)

# определяем момент покупки
purch_medium = pur[pur['user_id'].isin(medium_level)][['event_datetime', 'user_id']]
purch_easy = pur[pur['user_id'].isin(easy_level)][['event_datetime', 'user_id']]
purch_hard = pur[pur['user_id'].isin(hard_level)][['event_datetime', 'user_id']]
purch_total = pur[pur['user_id'].isin(ev_cnt_lev)][['event_datetime', 'user_id']]
# print(purch_total)

# ТРИ блока: 
# объединяем тайминги регистрации и покупки
# находим временной промежуток между регистрацией и оплатой у групп пользователей с разным уровнем сложности
# 1 строка объединение, 2  - расчет промежутка, 3 - расчет среднего промежутка
# по трем группам (1) medium (2) easy (3) hard (4) total

# (1)
merge_medium = reg_medium.merge(purch_medium, on='user_id', how='inner')
merge_medium['timedelta'] = merge_medium['event_datetime'] - merge_medium['start_time']
deltatime_medium = merge_medium['timedelta'].mean() # 4 days 06:12:07
print('Среднее время между регистрацией и оплатой в случае выбора уровня medium:',deltatime_medium)
# (2)
merge_easy = reg_easy.merge(purch_easy, on='user_id', how='inner')
merge_easy['timedelta'] = merge_easy['event_datetime'] - merge_easy['start_time']
deltatime_easy = merge_easy['timedelta'].mean() # 3 days 22:10:23
print('Среднее время между регистрацией и оплатой в случае выбора уровня easy:', deltatime_easy)
# (3)
merge_hard = reg_hard.merge(purch_hard, on='user_id', how='inner')
merge_hard['timedelta'] = merge_hard['event_datetime'] - merge_hard['start_time']
deltatime_hard = merge_hard['timedelta'].mean() # 3 days 14:55:19
print('Среднее время между регистрацией и оплатой в случае выбора уровня hard:', deltatime_hard)
# (4)
merge_total = reg_total.merge(purch_total, on='user_id', how='inner')
merge_total['timedelta'] = merge_total['event_datetime'] - merge_total['start_time']
deltatime_total = merge_total['timedelta'].mean() # 3 days 14:55:19
print('Среднее время между регистрацией и оплатой в случае выбора уровня:', deltatime_total)
print('*'*50)

# ТРИ блока: 
# объединяем тайминги выбора и покупки
# находим временной промежуток между выбором уровня и оплатой у групп пользователей с разным уровнем сложности
# 1 строка объединение, 2  - расчет промежутка, 3 - расчет среднего промежутка
# по трем группам (1) medium (2) easy (3) hard

# (1)
merge_medium1 = choice_medium.merge(purch_medium, on='user_id', how='inner')
merge_medium1['timedelta'] = merge_medium1['event_datetime'] - merge_medium1['start_time']
deltatime_medium1 = merge_medium1['timedelta'].mean() # 4 days 06:12:07
print('Среднее время между выбором уровня сложности и оплатой в случае выбора уровня medium:',deltatime_medium1)
# (2)
merge_easy1 = choice_easy.merge(purch_easy, on='user_id', how='inner')
merge_easy1['timedelta'] = merge_easy1['event_datetime'] - merge_easy1['start_time']
deltatime_easy1 = merge_easy1['timedelta'].mean() # 3 days 22:10:23
print('Среднее время между выбором уровня сложности и оплатой в случае выбора уровня easy:', deltatime_easy1)
# (3)
merge_hard1 = choice_hard.merge(purch_hard, on='user_id', how='inner')
merge_hard1['timedelta'] = merge_hard1['event_datetime'] - merge_hard1['start_time']
deltatime_hard1 = merge_hard1['timedelta'].mean() # 3 days 14:55:19
print('Среднее время между выбором уровня сложности и оплатой в случае выбора уровня hard:', deltatime_hard1)
# (4)
merge_total1 = choice_total.merge(purch_total, on='user_id', how='inner')
merge_total1['timedelta'] = merge_total1['event_datetime'] - merge_total1['start_time']
deltatime_total1 = merge_total1['timedelta'].mean() # 3 days 14:55:19
print('Среднее время между выбором уровня сложности и оплатой в случае выбора уровня:', deltatime_total1)
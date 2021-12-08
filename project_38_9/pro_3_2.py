import pandas as pd

# считываем базовые файлы
ev = pd.read_csv('data/7_4_Events.csv', sep=',')  # 252334 rows x 6 columns : id > event_type > selected_level > start_time > tutorial_id > user_id 
pur = pd.read_csv('data/purchase.csv', sep=',')   # 5956 rows x 4 columns : id > user_id > event_datetime > amount 

# оставляем только юзеров с регой от 2018 г.
cond1=(ev['event_type']=='registration')&(ev['start_time']>='2018-01-01')&(ev['start_time']<'2019-01-01') # фильтр реги-2018
spisok_users=ev[cond1]['user_id'].to_list()  #список с номерами юзеров с регой-2018
ev = ev[ev['user_id'].isin(spisok_users)] # обновленный файл, в котором только юзеры с регой-2018: 66959 rows x 6 columns; 19926 уник
pur = pur[pur['user_id'].isin(spisok_users)] # обновленный файл, в котором только юзеры с регой-2018: 1600 rows x 4 columns; 1600 уник

# преобразовываем даты
ev['start_time'] = pd.to_datetime(ev['start_time'])
pur['event_datetime'] = pd.to_datetime(pur['event_datetime'])

#  КОНЕЦ ОБЩЕЙ ЧАСТИ

# считаем структуру событий ФАКУЛЬТАТИВНО
str_ev = ev['event_type'].value_counts() 
# registration 19926, tutorial_start 18050, tutorial_finish 14904, level_choice 8342, pack_choice 5737. СУММА=66959 записей
# уникальных юзеров 19926
# print(str_ev)

# РАЗДЕЛ, ГДЕ РАССЧИТЫВАЕМ ЗАВИСИМОСТЬ ОПЛАТЫ ОТ КОЛИЧЕСТВА СТАРТОВ УЧЕБЫ 
# ищем, сколько раз юзеры начинали обучение
ev['tmp1'] = ev['event_type'].apply(lambda x: 1 if x == 'tutorial_start' else 0) # доп.столбец с 1 на начале учебы
ev_ser = ev.groupby('user_id')['tmp1'].sum()     #группировка по юзерам - количество стартов обучения
ev_ser_max = ev_ser.max()           # максимальное количество стартов обучения 
ev = ev.drop('tmp1', axis=1)        # удаляем вспомогательный столбец

# составляем список тех, кто прошел обучение n раз и список тех, кто потом совершил платеж 
sp_ev = [0] * (ev_ser_max+1)  # список с номерами юзеров, которые начинали учебу n раз
sp_pur = [0] * (ev_ser_max+1)  # список с номерами юзеров, которые начинали учебу n раз и потом совершили платеж
sp_pur_mean = [0] * (ev_ser_max+1) # список со средним платежом по количеству стартов учебы
for i in range(ev_ser_max+1):
    sp_ev[i] = ev_ser[ev_ser == i].index
    sp_pur[i] = pur[pur['user_id'].isin(sp_ev[i])]['user_id']
    sp_pur_mean[i] = round(pur[pur['user_id'].isin(sp_ev[i])]['amount'].mean(),2)

# считаем их количества и доли совершивших оплату ЭТО ВТОРОЙ ВОПРОС ПРОЕКТА
sp_ev_cnt = [len(el) for el in sp_ev] # [8068, 9103, 1589, 427, 221, 109, 116, 94, 86, 113] количества юзеров, начинавших учебу 
sp_pur_cnt = [len(el) for el in sp_pur] # [22, 1207, 218, 51, 30, 16, 14, 12, 13, 17] из них - количества оплативших
conv = [round(sp_pur_cnt[i] * 100 / sp_ev_cnt[i],2) for i in range(ev_ser_max+1)] 
# [0.27, 13.26, 13.72, 11.94, 13.57, 14.68, 12.07, 12.77, 15.12, 15.04] - вероятность оплаты после n раз учебы 

sp_ev_cnt_tut = sum(sp_ev_cnt)- sp_ev_cnt[0] # количество начинавших учебу ВСЕГО 11858
sp_pur_cnt_tut = sum(sp_pur_cnt) - sp_pur_cnt[0] # из них - количество оплативших 1578
conv_tut = round(sp_pur_cnt_tut*100/sp_ev_cnt_tut,2) # вероятность оплаты после начала учебы 13.31
pur_tut = round(pur[~pur['user_id'].isin(sp_pur[0])]['amount'].mean(), 2) # средний платеж начала окончания учебы 110.49


# РАЗДЕЛ, ГДЕ РАССЧИТЫВАЕМ ЗАВИСИМОСТЬ ОПЛАТЫ ОТ КОЛИЧЕСТВА ФИНИШЕЙ УЧЕБЫ 
# ищем, сколько раз юзеры оканчивали обучение
ev['tmp2'] = ev['event_type'].apply(lambda x: 1 if x == 'tutorial_finish' else 0) # доп.столбец с 1 на конце учебы
ev_serr = ev.groupby('user_id')['tmp2'].sum()     #группировка по юзерам - количество финишей обучения
ev_serr_max = ev_serr.max()           # максимальное количество финишей обучения 
ev = ev.drop('tmp2', axis=1)        # удаляем вспомогательный столбец

# составляем список тех, кто окончил обучение n раз и список тех, кто потом совершил платеж 
sp_evr = [0] * (ev_serr_max+1)  # список номеров юзеров, которые окончили учебу n раз
sp_purr = [0] * (ev_serr_max+1)  # список номеров юзеров, которые окончили учебу n раз и потом совершили платеж
sp_purr_mean = [0] * (ev_serr_max+1)  # список со средним платежом по количеству финишей учебы
for i in range(ev_serr_max+1):
    sp_evr[i] = ev_serr[ev_serr == i].index
    sp_purr[i] = pur[pur['user_id'].isin(sp_evr[i])]['user_id']
    sp_purr_mean[i] = round(pur[pur['user_id'].isin(sp_evr[i])]['amount'].mean(),2)

    
# считаем их количества и доли совершивших оплату ЭТО ВТОРОЙ ВОПРОС ПРОЕКТА
sp_evr_cnt = [len(el) for el in sp_evr] # [9676, 8015, 1321, 345, 178, 117, 101, 97, 54, 22] количества окончивших учебу 
sp_purr_cnt = [len(el) for el in sp_purr] # [153, 1143, 182, 44, 19, 19, 15, 15, 6, 4] из них - количества оплативших
convr = [round(sp_purr_cnt[i] * 100 / sp_evr_cnt[i],2) for i in range(ev_serr_max+1)] 
# [1.58, 14.26, 13.78, 12.75, 10.67, 16.24, 14.85, 15.46, 11.11, 18.18] - вероятность оплаты после n раз окончания учебы 

sp_evr_cnt_tut = sum(sp_evr_cnt)- sp_evr_cnt[0] # количество окончивших учебу ВСЕГО 10250
sp_purr_cnt_tut = sum(sp_purr_cnt) - sp_purr_cnt[0] # из них - количество оплативших 1447
convr_tut = round(sp_purr_cnt_tut*100/sp_evr_cnt_tut,2) # вероятность оплаты после окончания учебы 14.12
purr_tut = round(pur[~pur['user_id'].isin(sp_purr[0])]['amount'].mean(), 2) # средний платеж после окончания учебы 110.99

print('*'*25)
print('Количество начинавших учебу ВСЕГО  ', sp_ev_cnt_tut)
print('Вероятность оплаты в случае начала обучения, %  ',  conv_tut)
print('Средний платеж в случае начала учебы', pur_tut) 
print()
print('Количество окончивших учебу ВСЕГО  ', sp_evr_cnt_tut)
print('Вероятность оплаты в случае окончания обучения, %  ', convr_tut)
print('Средний платеж в случае окончания учебы', purr_tut) 
print()
print('Количество начинавших учебу (индекс=количеству стартов обучения)  ', sp_ev_cnt)
print('Вероятность оплаты в случае начала обучения (индекс=количеству стартов обучения), %  ',conv)
print('Средний платеж в случае начала обучения (индекс=количеству стартов обучения)', sp_pur_mean )
print()
print('Количество окончивших обучение (индекс=количеству финишей обучения)  ',sp_evr_cnt)
print('Вероятность оплаты в случае завершения обучения (индекс=количеству финишей обучения), %  ', convr)
print('Средний платеж в случае завершения обучения (индекс=количеству финишей обучения)', sp_purr_mean)
print('*'*25)
res2 = pd.DataFrame(
    {'start_tut,pers': sp_ev_cnt, 
    'purch_start,pers': sp_pur_cnt,
    'purch/start,%': conv,
    'purch/start,mean': sp_pur_mean,
    'finish_tut,pers': sp_evr_cnt, 
    'purch_finish,pers': sp_purr_cnt,
    'purch/finish,%': convr,
    'purch/finish,mean': sp_purr_mean,}
)
print('Сводная таблица влияния начала/завершения обучения на совершение платежа, по количеству прохождений обучения:')
print()
print(res2)
print('Обозначения:')
print('start_tut,pers - количество пользователей по количеству стартов обучения',
    'purch_start,pers - из них совершивших платеж',
    'purch/start,% - доля совершивших платеж в проходивших обучение, по количеству стартов, %',
    'purch/start,mean - средний платеж проходивших обучение, по количеству стартов',
    'finish_tut,pers - количество пользователей по количеству завершенных обучений', 
    'purch_finish,pers - из них совершивших платеж',
    'purch/finish,% - доля совершивших платеж в завершивших обучение, по количеству финишей, %', 
    'purch/finish,mean - средний платеж завершивших обучение, по количеству финишей', sep='\n')



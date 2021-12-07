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


# ПЕРВЫЙ ВОПРОС ПРО ТАЙМИНГ ГРУПП
# сначала - группы юзеров и воронка 

# формируем три группы юзеров - без обучения, с оконченным обучением, с неоконченным обучением
gr_notut = sp_ev[0] # список индексов тех, кто не начинал учебу 8068
gr_nofintut = sp_evr[0].difference(gr_notut) # список индексов тех, кто начинал, но не окончил учебу 1608
gr_fintut = ev_ser[ev_ser >0].index.difference(gr_nofintut) # список индексов тех, кто начал и окончил учебу 10250
# сумма по трем группам 8068 + 1608 + 10250 = 19926 - все зарегившиеся в 2018 норм

# считаем выбравших уровень сложности вопросов по трем группам юзеров - без обучения, с оконченным обучением, с неоконченным обучением  
ev['tmp3'] = ev['event_type'].apply(lambda x: 1 if x == 'level_choice' else 0) # доп.столбец с 1 на выборе уровня
ev_tmp3 = ev.groupby('user_id')['tmp3'].sum()
s_level = ev_tmp3[ev_tmp3 > 0].index              # список индексов всех выбравших уровень 8342
ev = ev.drop('tmp3', axis=1)        # удаляем вспомогательный столбец
del ev_tmp3                         # удаляем вспомогательный фр
gr_notut_level = gr_notut.intersection(s_level) # без обучения выбрали уровень 98
gr_nofintut_level = gr_nofintut.intersection(s_level) # не окончив обучения выбрали уровень 743
gr_fintut_level = gr_fintut.intersection(s_level) # по окончании обучения выбрали уровень 7501

# считаем выбравших бесплатные пакеты вопросов по трем группам юзеров - без обучения, с оконченным обучением, с неоконченным обучением  
ev['tmp4'] = ev['event_type'].apply(lambda x: 1 if x == 'pack_choice' else 0) # доп.столбец с 1 на бесплатном пакете
ev_tmp4 = ev.groupby('user_id')['tmp4'].sum()
s_pack = ev_tmp4[ev_tmp4 > 0].index              # список индексов всех выбравших пакет вопросов 5737
ev = ev.drop('tmp4', axis=1)        # удаляем вспомогательный столбец
del ev_tmp4                         # удаляем вспомогательный фр
gr_notut_pack = gr_notut.intersection(s_pack) # без обучения выбрали бесплатный пакет 74
gr_nofintut_pack = gr_nofintut.intersection(s_pack) # не окончив обучения выбрали бесплатный пакет 487
gr_fintut_pack = gr_fintut.intersection(s_pack) # по окончании обучения выбрали бесплатный пакет 5176
# сумма по трем группам 74 + 487 + 5176 = 5737 - норм

# считаем, сколько оплативших по трем группам юзеров - без обучения, с оконченным обучением, с неоконченным обучением  
gr_notut_pur = pur[pur['user_id'].isin(gr_notut)]['user_id'] # оплатившие из необучавшихся 22
gr_nofintut_pur = pur[pur['user_id'].isin(gr_nofintut)]['user_id'] # оплатившие из неокончивших учебу 131
gr_fintut_pur = pur[pur['user_id'].isin(gr_fintut)]['user_id'] # оплатившие из окончивших обучение 1447
# сумма по трем группам 22 + 131 + 1447 = 1600 - норм

# определяем моменты событий
time_reg = ev[ev['event_type'] == 'registration'][['user_id', 'start_time']]
time_level = ev[ev['event_type'] == 'level_choice'][['user_id', 'start_time']]
time_pack = ev[ev['event_type'] == 'pack_choice'][['user_id', 'start_time']]
# определяем разницу между событиями
delt = time_reg.merge(time_level, on='user_id', how='left').merge(time_pack, on='user_id', how='left').merge(pur, on='user_id', how='left')
delt.columns = ['user_id', 'registration', 'level_ch', 'pack_ch', 'id', 'purchase', 'am']
delt = delt.drop(['id','am'], axis=1)
delt['step1'] = delt['level_ch'] - delt['registration']
delt['step2'] = delt['pack_ch'] - delt['registration']
delt['step3'] = delt['purchase'] - delt['registration']

step0 = ['Группа "без обучения"', 'Группа "с неоконченным обучением"', 'Группа "с оконченным обучением"']

step1 = [0, 0, 0] # время от реги до выбора уровня вопросов 
step1[0] = delt[delt['user_id'].isin(gr_notut_level)]['step1'].mean()
step1[1] = delt[delt['user_id'].isin(gr_nofintut_level)]['step1'].mean()
step1[2] = delt[delt['user_id'].isin(gr_fintut_level)]['step1'].mean()
 
step2 = [0, 0, 0] # время от реги до выбора бесплатного пакета вопросов 
step2[0] = delt[delt['user_id'].isin(gr_notut_pack)]['step2'].mean()
step2[1] = delt[delt['user_id'].isin(gr_nofintut_pack)]['step2'].mean()
step2[2] = delt[delt['user_id'].isin(gr_fintut_pack)]['step2'].mean()

step3 = [0, 0, 0] # время от реги до покупки платного пакета вопросов 
step3[0] = delt[delt['user_id'].isin(gr_notut_pur)]['step3'].mean()
step3[1] = delt[delt['user_id'].isin(gr_nofintut_pur)]['step3'].mean()
step3[2] = delt[delt['user_id'].isin(gr_fintut_pur)]['step3'].mean()

print('-' *50)
print('Время прохождения различных этапов для пользователей из различных групп')
for i in range(3):
    print('-'*15)
    print(step0[i], ': среднее время от регистрации до выбора уровня вопросов - ', step1[i])
    print(step0[i], ': среднее время от регистрации до выбора бесплатного пакета вопросов - ', step2[i])
    print(step0[i], ': среднее время от регистрации до покупки платного пакета вопросов - ', step3[i])
print('-' *50)

if step1[0] > step1[2]:
    print(step0[2], 'БЫСТРЕЕ переходит от регистрации к выбору УРОВНЯ СЛОЖНОСТИ бесплатных вопросов, чем', step0[0], 'на', step1[0] - step1[2])
else:
    print(step0[0], 'БЫСТРЕЕ переходит от регистрации к выбору УРОВНЯ СЛОЖНОСТИ бесплатных вопросов, чем', step0[2], 'на', step1[2] - step1[0])
print()
if step2[0] > step2[2]:
    print(step0[2], 'БЫСТРЕЕ переходит от регистрации к выбору БЕСПЛАТНОГО ПАКЕТА вопросов, чем', step0[0], 'на', step2[0] - step2[2])
else:
    print(step0[0], 'БЫСТРЕЕ переходит от регистрации к выбору БЕСПЛАТНОГО ПАКЕТА вопросов, чем', step0[2], 'на', step2[2] - step2[0])
print()
if step3[0] > step3[2]:
    print(step0[2], 'БЫСТРЕЕ переходит от регистрации к ПОКУПКЕ платного пакета вопросов, чем', step0[0], 'на', step3[0] - step3[2])
else:
    print(step0[0], 'БЫСТРЕЕ переходит от регистрации к ПОКУПКЕ платного пакета вопросов, чем', step0[2], 'на', step3[2] - step3[0])
print()
    
mi = min(step1)
ma = max(step1)
for i in range(3):
    if step1[i] == mi:
        i_mi = i
    elif step1[i] == ma:
        i_ma = i
print('По увеличению времени от регистрации к выбору УРОВНЯ СЛОЖНОСТИ бесплатных вопросов, от самого быстрого к самому медленному:')
print(step0[i_mi], '>>>', step0[3 - i_mi - i_ma], '>>>', step0[i_ma])
print()
mi = min(step2)
ma = max(step2)
for i in range(3):
    if step2[i] == mi:
        i_mi = i
    elif step2[i] == ma:
        i_ma = i
print('По увеличению времени от регистрации к выбору БЕСПЛАТНОГО ПАКЕТА вопросов, от самого быстрого к самому медленному:')
print(step0[i_mi], '>>>', step0[3 - i_mi - i_ma], '>>>', step0[i_ma])
print()
mi = min(step3)
ma = max(step3)
for i in range(3):
    if step3[i] == mi:
        i_mi = i
    elif step3[i] == ma:
        i_ma = i
print('По увеличению времени от регистрации к ПОКУПКЕ платного пакета вопросов, от самого быстрого к самому медленному:')
print(step0[i_mi], '>>>', step0[3 - i_mi - i_ma], '>>>', step0[i_ma])
print()





#КВАЗИВОРОНКА ПЕЧАТЬ
print('='*30)
print('КВАЗИВОРОНКА')
print('='*30)
print('Группа "без обучения"')
print('Всего: ', len(gr_notut), 'человек')
print('Выбрали уровень сложности: ', len(gr_notut_level), 'или в % от их стартовой численности: ', round(len(gr_notut_level)*100/len(gr_notut), 2))
print('Выбрали пакет бесплатных вопросов: ', len(gr_notut_pack), 'или в % от их стартовой численности: ', round(len(gr_notut_pack)*100/len(gr_notut), 2))
print('Купили платный пакет вопросов: ', len(gr_notut_pur), 'или в % от их стартовой численности: ', round(len(gr_notut_pur)*100/len(gr_notut), 2))
print('='*30)

print('Группа "с неоконченным обучением"')
print('Всего: ', len(gr_nofintut), 'человек')
print('Выбрали уровень сложности: ', len(gr_nofintut_level), 'или в % от их стартовой численности: ', round(len(gr_nofintut_level)*100/len(gr_nofintut), 2))
print('Выбрали пакет бесплатных вопросов: ', len(gr_nofintut_pack), 'или в % от их стартовой численности: ', round(len(gr_nofintut_pack)*100/len(gr_nofintut), 2))
print('Купили платный пакет вопросов: ', len(gr_nofintut_pur), 'или в % от их стартовой численности: ', round(len(gr_nofintut_pur)*100/len(gr_nofintut), 2))
print('='*30)

print('Группа "с оконченным обучением"')
print('Всего: ', len(gr_fintut), 'человек')
print('Выбрали уровень сложности: ', len(gr_fintut_level), 'или в % от их стартовой численности: ', round(len(gr_fintut_level)*100/len(gr_fintut), 2))
print('Выбрали пакет бесплатных вопросов: ', len(gr_fintut_pack), 'или в % от их стартовой численности: ', round(len(gr_fintut_pack)*100/len(gr_fintut), 2))
print('Купили платный пакет вопросов: ', len(gr_fintut_pur), 'или в % от их стартовой численности: ', round(len(gr_fintut_pur)*100/len(gr_fintut), 2))
print('='*30)

#ЭТО ТРЕТИЙ ВОПРОС
lev_ch = ev[ev['event_type'] == 'level_choice'][['user_id', 'start_time']]
tut_st = ev[ev['event_type'] == 'tutorial_start'][['user_id', 'start_time']]
lev_ch = lev_ch.merge(tut_st, on = 'user_id', how = 'left')
lev_ch.columns = ['user_id', 'tm_lev_choice', 'tm_tutorial_st']
lev_ch = lev_ch[lev_ch['tm_lev_choice'] <= lev_ch['tm_tutorial_st']]
print('0'*25)
print('Из общего количества стартов учебы', len(tut_st['user_id']), 'после выбора уровня сложности вопросов -', len(lev_ch['user_id']), 'или', round(len(lev_ch['user_id'])*100/len(tut_st['user_id']), 2), '%')
print('Из общего количества начинавших учебу', tut_st['user_id'].nunique(), 'после выбора уровня сложности вопросов -', lev_ch['user_id'].nunique(), 'или', round(lev_ch['user_id'].nunique()*100/tut_st['user_id'].nunique(), 2), '%')

# print('Количество стартов учебы после выбора уровня сложности вопросов:', len(lev_ch['user_id'], 'из общего количества стартов учебы', len(tut_st['user_id'])))
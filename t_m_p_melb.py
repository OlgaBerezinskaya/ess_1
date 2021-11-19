import pandas as pd



import re 
def get_year_release(arg):
    candidates = re.findall(r'\(\d{4}\)', arg)                  #находим все слова по шаблону "(DDDD)"
    if len(candidates) > 0:                         # проверяем число вхождений
        year = candidates[0].replace('(', '')           #если число вхождений больше 0,очищаем строку от знаков "(" и ")"
        year = year.replace(')', '')
        return int(year)
    else:                      #если год не указан, возвращаем None
        return None

af=pd.read_csv('data/ratings_movies.csv', sep=',')
s = []
for el in af['title']:
    s.append(get_year_release(el))
    
af['year_release'] = s

aff = af[af['year_release'] == 2000]
# print(aff.groupby(by='movieId')['rating'].mean().min())

# print(af[af['year_release'] == 1999].groupby(by='movieId')['rating'].mean().sort_values())
# print(af[af['movieId'] == 145951])

# print(af.groupby(by=['userId','genres'])['movieId'].count())

sp = af.groupby(by='userId')['rating'].count()
# print(sp)
smin = sp.min()

sps = []
for el in af['userId']:
    if af.groupby(by='userId')['rating'].count()[el] == smin:
        sps.append(el)
# print(sps)    
# print(sp.sort_values())
# print(af[af.groupby(by='userId')['rating'].count() == smin]['rating'].mean())
# merg = sp.sort_values().merge(af, on='userId')
# print(merg)
# af['new'] = af.groupby(by='userId')['rating'].count() 
# print(af)
print(100)



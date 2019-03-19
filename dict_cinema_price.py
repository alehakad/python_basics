
cinema = dict()
cinema['Пятница'] = {12:250,16:350,20:450}
cinema['Чемпионы'] = {10:250,13:350,16:350}
cinema['Пернатая банда'] = {10:350,14:350,18:350}
cinema['date']={'сегодня':0,'завтра':0.05}
film = input('Введите фильм:\n')
time = int(input('Время: \n'))
date = input('Дата:\n')
n = int(input('Количество:\n'))
print('Результат: ')

if n>=20:
    print(round((1-0.2-cinema['date'][date])*n*cinema[film][time]))
else:
    print(round((1-cinema['date'][date])*n*cinema[film][time]))

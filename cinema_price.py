film = input('Выберите фильм: \n')
day = input('Выберете дату: \n')
time = int(input('Выберете время: \n'))
n = int(input('Количество билетов: \n'))
res = 0
dis = 0
if film and day and time and n:
    if film == 'Пятница':
        if time == 12 :
            res = 250
        elif time == 16 :
            res = 350
        else :
            res = 450
    if film == 'Чемпионы':
        if time == 10 :
            res = 250
        else :
            res = 350
    if film == 'Пернатая банда':
        if time == 10 :
            res = 350
        else :
            res = 450
    if day == 'завтра' :
        dis = dis + 5
    if n >= 20:
        dis = dis + 20
else :
    print('Неверные данные')
print('Выбрали фильм: ',film ,'День: ',day ,'Время: ',time ,'Количество билетов: ',n ,'Результат', res*n*(1-dis/100),sep = "\n")

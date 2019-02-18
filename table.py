value = input("Введите номер элемента: \n")
if value:
    num = int(value)
    if num == 3:
        print("Это Li")
    elif num == 25:
        print("Это Mn")
    elif num == 80:
        print("Это Hg")
    elif num == 17:
        print("Это Cl")
    else:
        print("Ошибка")
else:
    print("Введите значение pH!")

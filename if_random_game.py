import random
a = random.randint(1,4)
b = int(input("Угадайте число от 1 до 4\n"))
if a == b : 
    print("Победа!")
else:
    print("Введите еще раз\n")
    if a < b :
        print("Загаданное меньше введенного")
    else :
        print("Загаданное больше введенного")

a=0
tsk=[]
k=[]
dl=[]
while a!=3 :
    a = int(input('Введите число\n'))
    if a==1 :
       tsk.append(input('Сформулируйте задачу:\n'))
       k.append(input('Добавьте категорию к задаче:\n'))
       dl.append(input('Добавьте время к задаче\n'))
    if a==2 :
        for i in range (len(tsk)):
            print('Задача: ',tsk[i],'Категория: ',k[i],'Дата: ',dl[i],'\n')

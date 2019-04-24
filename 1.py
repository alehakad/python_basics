from tkinter import *
root = Tk()
counter = DoubleVar()
r = StringVar()
i = StringVar()
counter.set(0)
def sphere():
    try:
        counter.set(4/3*3.14*int(r.get())**3)
    except:
        counter.set("Ошибка")
def write():
    if i.get=="Текст":
        with open("text.txt", 'w') as output_file:
            output_file.write(str(counter.get()))
    else:
        with open("text.html", 'w') as output_file:
            output_file.write(str(counter.get()))
Label(text="Программа для вычисления объема",fg="#eee", bg="#333",font="Arial 11").grid(row=0, column=2)      
Label(text="Введите радиус:").grid(row=1, column=0)
table_name = Entry(width=15,textvariable= r)
table_name.grid(row=1, column=1, columnspan=3)
     
Label(text="Результат вычислений ").grid(row=2, column=0)
table_row = Label(width=15,textvariable=counter)
table_row.grid(row=2, column=3)

Button(text="Вычислить",command = sphere).grid(row=3, column=2)
Button(text="Сохранить",command = write).grid(row=4, column=0)
 
i.set("Выпадающий список")
OptionMenu(root,i,"Текст","HTML").grid(row=4,column=3)


root.mainloop()

from tkinter import *
import json


with open('todo_list.json', 'w', encoding='windows-1251') as file_write:
            json.dump([], file_write)


def add():
    
    lst = [] 
    dictr = {}
    dictr['task'] = task.get()
    dictr['cat'] = cat.get()
    dictr['time'] = time.get()
    lst.append(dictr)
    
    try:
        with open('todo_list.json', 'r') as json_file:
            contents = json.load(json_file)
        for i in lst:
            contents.append(i)
        with open('todo_list.json', 'w') as file_write:
            json.dump(contents, file_write)
    except Exception as e:
        print(e)

def write():  
    text1.configure(state=NORMAL)
    text1.delete(1.0, END)
    try:
        with open('todo_list.json', 'r') as json_file:  
            contents = json.load(json_file)
        for todo in contents: 
            
            text1.insert(1.0, "Задача: " + todo['task'] + " " + "Категория: " + todo[
                'cat'] + " " + "Дата: " + todo['time'] + '\n')
           

    except:
           text1.insert(1.0,"error")     
    





    





def ext(): 
    root.destroy()
    

root = Tk() 
counter = DoubleVar() 
task = StringVar() 
cat = StringVar() 
time = StringVar() 
label_text = StringVar()

root.title("project")
Label(text="Менеджер задач",fg="#eee", bg="#333",font="Arial 11",width = 30).grid(row=0, column=2) 
Label(text="Задача:").grid(row=1, column=0) 
table_task = Entry(width=15,textvariable = task) 
table_task.grid(row=1, column=1, columnspan=3) 
Label(text="Категория:").grid(row=2, column=0) 
table_cat = Entry(width=15,textvariable= cat) 
table_cat.grid(row=2, column=1, columnspan=3) 
Label(text="Время").grid(row=3, column=0) 
table_time = Entry(width=15,textvariable= time) 
table_time.grid(row=3, column=1, columnspan=3) 


Button(text="Добавить",command = add).grid(row=5, column=2) 
Button(text="Список задач",command = write).grid(row=6, column=2) 
Button(text="Выход",command = ext).grid(row=7, column=2) 
text1= Text(width=50,height=20)
text1.grid(row =1,column =5,rowspan =3)

root.mainloop()

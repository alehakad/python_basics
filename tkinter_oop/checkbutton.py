# Эта программа демонстрирует группу элементов Checkbutton.
import tkinter
import tkinter.messagebox

class MyGUI:
    def __init__(self):
        # Создать главное окно.
        self.main_window = tkinter.Tk()

        # Создать две рамки. Одну для элементов Checkbutton
        # и еще одну для обычных элементов Button.
        self.top_frame = tkinter.Frame(self.main_window)
        self.bottom_frame = tkinter.Frame(self.main_window)
 
        # Создать три объекта IntVar для использования с
        # элементами Checkbutton.
        self.cb_var1 = tkinter.IntVar()
        self.cb_var2 = tkinter.IntVar()
        self.cb_var3 = tkinter.IntVar()
        self.cb_var4 = tkinter.IntVar()
        self.cb_var5 = tkinter.IntVar()
        self.cb_var6 = tkinter.IntVar()
        self.cb_var7 = tkinter.IntVar()
        
 
        # Назвначить объектам IntVar значения 0.
        self.cb_var1.set(0)
        self.cb_var2.set(0)
        self.cb_var3.set(0)
        self.cb_var4.set(0)
        self.cb_var5.set(0)
        self.cb_var6.set(0)
        self.cb_var7.set(0)
 
 
        # Создать элементы Checkbutton в рамке top_frame.
        self.cb1 = tkinter.Checkbutton(self.top_frame,
                                       text='Замена масла - $30.00',
                                       variable=self.cb_var1,onvalue = 30,offvalue=0)
        self.cb2 = tkinter.Checkbutton(self.top_frame,
                                       text='Смазочные работы - $20.00',
                                       variable=self.cb_var2,onvalue = 20,offvalue=0)
        self.cb3 = tkinter.Checkbutton(self.top_frame,
                                       text='Промывка радиатора  - $40.00',
                                       variable=self.cb_var3, onvalue = 40,offvalue=0)
        self.cb4 = tkinter.Checkbutton(self.top_frame,
                                       text='Замена жидкости в трансмиссии - $100.00',
                                       variable=self.cb_var4 ,onvalue = 100,offvalue=0)
        self.cb5 = tkinter.Checkbutton(self.top_frame,
                                       text='Осмотр - $35.00',
                                       variable=self.cb_var5, onvalue = 35,offvalue=0)
        self.cb6 = tkinter.Checkbutton(self.top_frame,
                                       text='Замена глушителя выхлопа - $200.00',
                                       variable=self.cb_var6, onvalue = 200,offvalue=0)
        self.cb7 = tkinter.Checkbutton(self.top_frame,
                                       text='Перестановка шин - $20.00',
                                       variable=self.cb_var7, onvalue = 20,offvalue=0)









        # Упаковать элементы Checkbutton.
        self.cb1.pack()
        self.cb2.pack()
        self.cb3.pack()
        self.cb4.pack()
        self.cb5.pack()
        self.cb6.pack()
        self.cb7.pack()
        

        # Создать кнопку 'OK' и кнопку 'Выйти'.
        self.ok_button = tkinter.Button(self.bottom_frame,
                                        text='OK',
                                        command=self.show_choice)
        self.quit_button = tkinter.Button(self.bottom_frame,
                                          text='Выйти',
                                 command=self.main_window.destroy)

        # Упаковать элементы Button.
        self.ok_button.pack(side='left')
        self.quit_button.pack(side='left')

        # Упаковать рамки.
        self.top_frame.pack()
        self.bottom_frame.pack()
 
        # Запустить главный цикл.
        tkinter.mainloop()

    # Метод show_choice является функцией обратного вызова
    # для кнопки 'OK'.

    def show_choice(self):
        # Создать символьную последовательность с сообщением.
        self.message = 'Ваши затраты = \n'
        s = 0
        # Определить, какие элементы Checkbuttons были выбраны и
        # составить соответствующее сообщение.
        s = s+ self.cb_var1.get()+self.cb_var2.get()+self.cb_var3.get()+self.cb_var4.get()+self.cb_var5.get()+self.cb_var6.get()+self.cb_var7.get()

        # Вывести сообщение в информационном диалоговом окне.
        tkinter.messagebox.showinfo('Общая стоимость',self.message+str(s))

# Создать экземпляр класса MyGUI.
my_gui = MyGUI()

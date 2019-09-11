import tkinter
import tkinter.messagebox

class MyGUI:
    def __init__(self):
        # Создать главное окно.
        self.main_window = tkinter.Tk()

        # Создать две рамки. Одну для элементов Radiobutton
        # и еще одну для обычных элементов Button.
        self.top_frame = tkinter.Frame(self.main_window)
        self.middle_frame = tkinter.Frame(self.main_window)
        self.bottom_frame = tkinter.Frame(self.main_window)
 
        # Создать объект IntVar для использования с
        # элементами Radiobutton.
        self.radio_var = tkinter.IntVar()
 
        # Назначить объекту IntVar значение 1.
        self.radio_var.set(1)

        # Создать элементы Radiobutton в рамке top_frame.
        self.rb1 = tkinter.Radiobutton(self.top_frame,
                                       text='Дневное время(6:00 - 17:59)',
                                       variable=self.radio_var,
                                       value=10)
        self.rb2 = tkinter.Radiobutton(self.top_frame,
                                       text='Вечернее время(18:00 - 23:59)',
                                       variable=self.radio_var,
                                       value=12)
        self.rb3 = tkinter.Radiobutton(self.top_frame,
                                       text='Ночное время(00:00 - 5:59)',
                                       variable=self.radio_var,
                                       value=5)

        # Упаковать элементы Radiobutton.
        self.rb1.pack()
        self.rb2.pack()
        self.rb3.pack()
        self.min_label = tkinter.Label(self.middle_frame, text = "Введите количество минут")
        self.min_entry = tkinter.Entry(self.middle_frame,width = 20)

        self.min_label.pack(side = "left")
        self.min_entry.pack(side = "right")
    
        # Создать кнопки
        self.ok_button = tkinter.Button(self.bottom_frame,
                                        text='Показать стоимость',
                                        command=self.show_choice)
        self.quit_button = tkinter.Button(self.bottom_frame,
                                          text='Выйти',
                                command=self.main_window.destroy)

        # Упаковать элементы Button.
        self.ok_button.pack(side='left')
        self.quit_button.pack(side='left')

        # Упаковать рамки.
        self.top_frame.pack()
        self.middle_frame.pack()
        self.bottom_frame.pack()
 
        # Запустить главный цикл.
        tkinter.mainloop()

    # Метод show_choice является функцией обратного вызова
    # для кнопки OK.
    def show_choice(self):
        tkinter.messagebox.showinfo('Общая стоимость', 'Ваши затраты -' +
                                    str(self.radio_var.get()* int(self.min_entry.get())/100)+"$")

# Создать экземпляр класса MyGUI.
my_gui = MyGUI()

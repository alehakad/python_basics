import tkinter
class MyGUI:

    def __init__(self):



        

        self.main_window = tkinter.Tk()



       
        self.top_frame = tkinter.Frame(self.main_window)
        self.middle_frame = tkinter.Frame(self.main_window)
        self.third_frame = tkinter.Frame(self.main_window)
        self.bottom_frame = tkinter.Frame(self.main_window)
        self.gallons_label = tkinter.Label(self.top_frame, text = "Введите галлоны")
        self.gallons_entry = tkinter.Entry(self.top_frame, width=20)
        self.miles_label = tkinter.Label(self.middle_frame, text = "Введите мили")
        self.miles_entry = tkinter.Entry(self.middle_frame, width =20)





        self.calc_button = tkinter.Button(self.bottom_frame,

                                    text='Вычислить MPG',

                                    command=self.convert)

        self.quit_button = tkinter.Button(self.bottom_frame,

                                    text='Выйти',

                                    command=self.main_window.destroy)
        
        self.top_frame.pack()
        self.middle_frame.pack()
        self.third_frame.pack()
        self.bottom_frame.pack()
        self.gallons_label.pack(side = "left")
        self.gallons_entry.pack(side = "right")
        self.miles_label.pack(side = "left")
        self.miles_entry.pack(side = "right")
        
        self.calc_button.pack(side = "left")
        self.quit_button.pack(side = "right")


        self.value = tkinter.StringVar()
        self.info_label = tkinter.Label(self.third_frame,justify ="left",
                   textvariable=self.value)
        self.info_label.pack(side = "bottom")
        tkinter.mainloop()



    # Метод convert является функцией обратного вызова

    # для кнопки 'Преобразовать'.



    def convert(self):
        try:
            self.value.set("Мили на галлон(MPG) ="+str(float(self.miles_entry.get())/float(self.gallons_entry.get())))
        except:
            self.value.set("Ошибка")






# Создать экземпляр класса KiloConverterGUI.

kilo_conv = MyGUI()



import tkinter


class MyGUI:

    def __init__(self):

      

        self.main_window = tkinter.Tk()
        self.mid_frame = tkinter.Frame()
        self.bframe = tkinter.Frame()
        
        self.my_button = tkinter.Button(self.bframe,

                                        text='Показать инфо',

                                        command=self.do_something)


        self.my_button1 = tkinter.Button(self.bframe,

                                        text='Выход',

                                        command=self.main_window.destroy)
      
        self.mid_frame.pack()
        self.bframe.pack()
        self.my_button.pack(side="left")
        self.my_button1.pack(side="right")

        
        
        self.value = tkinter.StringVar()
        


       

        self.info_label = tkinter.Label(self.mid_frame,justify ="left",
                   textvariable=self.value)
        self.info_label.pack(side = "top")
        tkinter.mainloop()

    def do_something(self):
        self.value.set("Стивен Маркус \n 274 Бэйли\n Северная Каролина")
    
my_gui = MyGUI()





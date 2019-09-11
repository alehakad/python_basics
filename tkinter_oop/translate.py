import tkinter


class MyGUI:

    def __init__(self):

        

        self.main_window = tkinter.Tk()
        self.mid_frame = tkinter.Frame()
        self.bframe = tkinter.Frame()
        
        self.my_buttonl = tkinter.Button(self.bframe,

                                        text='left',

                                        command=self.do_somethingl)

        self.my_buttonm = tkinter.Button(self.bframe,

                                        text='medium',

                                        command=self.do_somethingm)
        self.my_buttonr = tkinter.Button(self.bframe,

                                        text='right',

                                        command=self.do_somethingr)
        
        self.mid_frame.pack()
        self.bframe.pack()
        self.my_buttonl.pack(side="left")     
        self.my_buttonm.pack(side = "left")
        self.my_buttonr.pack(side="right")

        
        
        self.value = tkinter.StringVar()
        



        self.info_label = tkinter.Label(self.mid_frame,justify ="left",
                   textvariable=self.value)
        self.info_label.pack(side = "top")
        tkinter.mainloop()

    def do_somethingl(self):
        self.value.set("левый")
    def do_somethingm(self):
        self.value.set("центральный")
    def do_somethingr(self):
        self.value.set("правый")
    
my_gui = MyGUI()







# download pygame, alarm before running
import tkinter
from pygame import mixer 
class MyGUI:

    def __init__(self):

        

        
        self.plays = False
        self.alm = False
        self.set_alarm = False
        self.main_window = tkinter.Tk()
        self.main_window.title("project")

        self.h = tkinter.IntVar()
        self.h.set(0)
        self.m1 = tkinter.IntVar()
        self.m1.set(0)
        self.m2= tkinter.IntVar()
        self.m2.set(0)
        self.top_frame = tkinter.Frame(self.main_window,bg="black")
        self.middle_frame = tkinter.Frame(self.main_window)
        self.h_label = tkinter.Label(self.top_frame, textvariable = self.h,fg="green",bg="black",height=3,width=5,font=("Helvetica", 25))
        self.m1_label = tkinter.Label(self.top_frame, textvariable = self.m1,fg="green",bg="black",height=3,width=2,font=("Helvetica", 25))
        self.m2_label = tkinter.Label(self.top_frame, textvariable = self.m2,fg="green",bg="black",height=3,width=2,font=("Helvetica", 25))
    




        self.plush_button = tkinter.Button(self.middle_frame,

                                    text='H',

                                    command=self.plush)

        self.plusm_button = tkinter.Button(self.middle_frame,

                                    text='M',

                                    command=self.plusm)
        self.alarm_button = tkinter.Button(self.middle_frame,

                                    text='A',

                                    command=self.alarm)
        
        self.top_frame.pack()
        self.middle_frame.pack()
        self.h_label.pack(side = "left")
        self.m1_label.pack(side = "left")
        self.m2_label.pack(side = "left")
        
        
        self.plush_button.pack(side = "left")
        self.plusm_button.pack(side = "left")
        self.alarm_button.pack(side = "left")
        self.start()
           


        
        tkinter.mainloop()
    def start(self):
        if not self.alm:
            
             self.id=self.main_window.after(1000,self.plusm)
             self.main_window.after(1000,self.start)
    def plush(self):
        self.h.set((self.h.get()+1)%24)
        if self.set_alarm and not self.plays and not self.alm:
            self.check()
        
    def plusm(self):
        if self.m2.get()==9:
            self.m2.set(0)
            if self.m1.get() == 5:
                self.m1.set(0)
                self.plush()
            else:
                self.m1.set(self.m1.get()+1)
        else:
            self.m2.set(self.m2.get()+1)
        if self.set_alarm and not self.plays and not self.alm:
            self.check()
        
    def alarm(self):
        self.main_window.after_cancel(self.id)
        if self.plays:
            mixer.music.stop()
            self.plays = False
            self.set_alarm = False
        elif not self.alm:
            self.alm = True
            self.rh,self.rm1,self.rm2  = self.h.get(),self.m1.get(),self.m2.get()
            self.h.set(0)
            self.m1.set(0)
            self.m2.set(0)
            if self.set_alarm:
                print("Turning off")
                self.main_window.destroy()
        else:
            self.alm = False
            self.set_alarm = True
            self.arh,self.arm1,self.arm2  = self.h.get(),self.m1.get(),self.m2.get()
            self.h.set(self.rh)
            self.m1.set(self.rm1)
            self.m2.set(self.rm2)
            self.start()
            self.check()
            
            
            
            
            
    def check(self):
            if self.arh==self.h.get() and  self.arm1==self.m1.get()and self.arm2==self.m2.get():
                print("music is playng")
                mixer.init()
                mixer.music.load(r'alarm.mp3')
                mixer.music.play()
                self.plays = True
                self.set_alarm = False
                mixer.music.fadeout(60000)
                self.main_window.after(60000,self.test)
    def test(self):
        if self.plays:
            self.plays = False
            self.set_alarm = False
        
    



    


    
            


      


bud = MyGUI()






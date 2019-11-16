import feedparser
import tkinter as tk
import pyttsx3
from nltk.stem.snowball import SnowballStemmer
import webbrowser
from PIL import Image,ImageTk
from urllib.request import urlopen

st = SnowballStemmer("russian")

engine = pyttsx3.init()
engine.setProperty('voice',"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0")
engine.setProperty('rate', 125)



def say(text):
    engine.say(text)
    engine.runAndWait()
def speech():
    
    import speech_recognition as sr
    r = sr.Recognizer()
    with sr.Microphone(device_index =0) as source:
        r.adjust_for_ambient_noise(source)#,duration=0.5)
        print("say..")
        audio = r.listen(source)
    try:
        q = r.recognize_google(audio,language = "ru-RU")#,show_all=True)
        return q.lower()
    except sr.UnknownValueError:
            print( "Cant recognize!")
            return False
    except sr.RequestError as e:
            print( "Internet error!")
            return False


class Parser():
    
    def __init__(self):
        self.main_window = tk.Tk()
        # %d = Type of action (1=insert, 0=delete, -1 for others)
        # %i = index of char string to be inserted/deleted, or -1
        # %P = value of the entry if the edit is allowed
        # %s = value of entry prior to editing
        # %S = the text string being inserted or deleted, if any
        # %v = the type of validation that is currently set
        # %V = the type of validation that triggered the callback
        #      (key, focusin, focusout, forced)
        # %W = the tk name of the widget

        self.main_window.geometry("800x400") #You want the size of the app to be 500x500
        self.main_window.resizable(0, 0)

        vcmd = (self.main_window.register(self.check),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')



        #menu
        self.mainmenu = tk.Menu(self.main_window)
        self.main_window.config(menu=self.mainmenu)
        
        self.setmenu = tk.Menu(self.mainmenu,tearoff =0)
        self.setmenu1 = tk.Menu(self.setmenu,tearoff =0)
        self.setmenu1.add_command(label = "Black",command = self.set_bl)
        self.setmenu1.add_command(label = "White",command = self.set_wh)
        self.setmenu.add_cascade(label = "Font",menu =self.setmenu1)

        self.helpmenu = tk.Menu(self.mainmenu ,tearoff =0)
        self.helpmenu.add_command(label = "RSS",command = self.about)

        self.mainmenu.add_cascade(label = "Settings",menu = self.setmenu)
        self.mainmenu.add_cascade(label = "About",menu = self.helpmenu)
        

        #image
        try:
            load = Image.open(urlopen('https://findicons.com/files/icons/730/soft/128/rss.png'))
            img = ImageTk.PhotoImage(load)
            self.img_panel = tk.Label(self.main_window, image = img)
        except:
            self.img_panel = tk.Label(self.main_window)
        
        
        self.res = []
        
        self.link = "https://news.yandex.ru/sport.rss"
        self.kwords =[]
        self.words = tk.StringVar()
        self.cg_link = tk.StringVar()
        self.new = tk.StringVar()
        self.main_window.title("RSS search") 
        self.top_frame = tk.Frame(self.main_window)
        self.middle_frame = tk.Frame(self.main_window)
        self.bot_frame = tk.Frame(self.main_window)
        self.last_frame = tk.Frame(self.main_window)
        
        self.e_link = tk.Entry(self.top_frame,textvariable=self.cg_link,width =50)
        self.b_news = tk.Button(self.middle_frame,text='Get news',command=self.get_news)
        self.b_link = tk.Button(self.middle_frame,text='Change link',command=self.change_link)
        self.l_words=tk.Entry(self.bot_frame,textvariable = self.words,validate = 'key', validatecommand = vcmd)
        self.b_words = tk.Button(self.bot_frame,text='Add',command = self.add_kwords)
        self.b_voice = tk.Button(self.bot_frame,text='Add by voice',command = self.add_voice)
        self.delete = tk.Button(self.bot_frame,text='Delete last',command = self.delete)
        self.out = tk.Label(self.last_frame, textvariable= self.new, fg="blue")
        self.out.bind('<Button-1>',self.openl)
        self.main_window.bind('<Left>',self.next_l)
        self.main_window.bind('<Right>',self.next_r)
        
        self.top_frame.pack()
        self.middle_frame.pack()
        self.bot_frame.pack()
        self.last_frame.pack(pady = 50)
        self.e_link.pack()
        self.b_news.pack(side="left")
        self.b_link.pack(side="right")
        self.l_words.pack(side = "top")
        self.out.pack()
        self.b_words.pack(side="right")
        self.b_voice.pack(side="right")
        self.delete.pack(side = "right")
        self.img_panel.pack()
        
        self.parse()

        self.cg_link.set(self.link)
        
        tk.mainloop()

        
        
    def check(self, action, index, value,
                       pvalue, text, validation_type, trigger_type, widget_name):
        
        try:
            if value=="":
                return True
            else:
                lst = value[-1]
            lst2 = ","
            if len(value)>=2:
                lst2 = value[-2]
            
                
            if lst.isalpha() or (lst == ","  and lst2!=","):
                return True
            
            else:
                say("Wrong input")
                return False
                
        except:
            return False
    def add_kwords(self):
         n=0
         l = self.words.get().split(",")
         for i in l:
             i = st.stem(i)
             if not(i in self.kwords) and i!="":
                 self.kwords.append(i)
                 n+=1
              
         self.words.set("")
         if n==1:
            act = "word was "
            say(str(n)+" key "+act+ "added")
         elif n>1:
            act = "words were "
            say(str(n)+" key "+act+ "added")
         
         print(self.kwords)
    def delete(self):
        if self.kwords:
            say("Word deleted")
            self.kwords.pop()
            print(self.kwords)
    def change_link(self):
        self.link = self.cg_link.get()
        self.parse()
    def parse(self):
        d = feedparser.parse(self.link)
        self.news = {}
        for st in d.entries:
            self.news.update({st.description:[st.title,st.link]})
    def add_voice(self):
        n=0
        sp = speech()
        if sp:
            for i in sp.split(" "):
                i = st.stem(i)
                if not(i in self.kwords) and i!="":
                     self.kwords.append(i)
                     n+=1
                     
                     
        
        if n==1:
            act = "word was "
        else :
            act = "words were "
        say(str(n)+" key "+act+ "added")
        #print(self.kwords)
        
    def get_news(self):
        nex = True
        
        for w in self.kwords:
            for i in self.news.keys():
                if w in i.lower():
                    self.res.append(self.news[i])
                    nex = False
        if nex:
            self.new.set("no news")        
        else:
            self.new.set(self.res[0][0])
            self.newi =0 
    def openl(self,event):
        if self.res:
            webbrowser.open(self.res[self.newi][1])
    def next_r(self,event):
        if self.res:
            self.newi  = (self.newi +1)%len(self.res)
            self.new.set(self.res[self.newi][0])
    def next_l(self,event):
        if self.res:
            self.newi  = (self.newi -1)%len(self.res)
            self.new.set(self.res[self.newi][0])
    def about(self):
        webbrowser.open("https://en.wikipedia.org/wiki/RSS")
    def set_bl(self):
        self.main_window.configure(background='black')
        self.out.configure(background='black')
    def set_wh(self):
        self.main_window.configure(background='white')
        self.out.configure(background='white')
        
        
wnd = Parser()


engine.stop()

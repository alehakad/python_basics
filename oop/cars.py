allman = []
mes = "This model is not serviced, sorry"
def ser(car):
    if car.price():
        return True
    print(mes)
    return False
class Car:
    def __init__(self,manu,model,year):
        self.__manu = manu
        self.__model = model 
        self.__year = year 
        
    def price(self):
        s  = 0 
        if self.__manu == "Porche":
            if self.__model == "Cayenne":
                s += 15000
            if self.__model == "911":
                s += 16000
            if self.__model == "Cayman":
                s += 13000
        if self.__manu == "BMW":
            if self.__model[0] == "X":
                s = 10000 + 1000*(int(self.__model[1]))
            
        if self.__manu == "Mercedes":
            if self.__model == "A":
                s += 12000
            if self.__model == "B":
                s += 13000
            if self.__model == "C":
                s += 14000
            if self.__model == "E":
                s += 15000
        
        return s
class Man: 
    def __init__(self,tel,name,adress): 
        self.tel = tel 
        self.name = name 
        self.__adress = adress 
class Client(Man): 
    def __init__(self,tel,name,adress,*cars): 
        Man.__init__(self,tel,name,adress)
        self.man = None
        self.cars = cars
    def repr(self,num):
        
        if ser(self.cars[num-1]):
            i=0
            while i<len(allman) and not(self.man):
                if not(allman[i].work):
                    self.man = allman[i] 
                    print(self.name,", Your car is being repaired.","Your manager is ",self.man.name,sep ="")
                    self.man.addcar(self.cars[num-1],self)
                i+=1
            if not(self.man):
                print(self.name,", no free managers. Wait, please",sep="")
        
class Manager(Man): 
    def __init__(self,tel,name,adress): 
        Man.__init__(self,tel,name,adress)
        allman.append(self)
        self.work = False
    def addcar(self,car,client):
        self.work = True
        self.car = car
        self.client = client
    def repr(self):
        print(self.client.name,", Your car has been repaired",sep="")
        self.work = False
        print("Total spends:",self.car.price())
Mercedes1 = Car("Mercedes","a3",2017)
Porche1 = Car("Porche","911",2017)
BMW1 = Car("BMW","X5",2017)
BMW2 = Car("BMW","X4",2015)
man1 = Manager("+376767","Ivan","1street")
man2 = Manager("+376764","Paul","1street")
cl1 = Client("+344445","Nick","2street",Mercedes1,Porche1)
cl2 = Client("+344442","Bob","123street",BMW1)
cl3 = Client("+344441","Serge","12street",BMW2)
cl1.repr(1)
cl1.repr(2)
cl2.repr(1)
cl3.repr(1)
man1.repr()
man2.repr()
'''
This model is not serviced, sorry
Nick, Your car is being repaired.Your manager is Ivan
Bob, Your car is being repaired.Your manager is Paul
Serge, no free managers. Wait, please
Nick, Your car has been repaired
Total spends: 16000
Bob, Your car has been repaired
Total spends: 15000
'''





        

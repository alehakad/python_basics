import random
allbombs = []
allweapons =[]
allmed = []
allplayers = []
def itemcheck(obj):
    for b in allbombs:
        if b.x == obj.x and b.y == obj.y and b.z == obj.z:
            print(obj.name,"has blown up on a bomb")
            obj.hp -= b.damage
    for w in allweapons:
        if w.x == obj.x and w.y == obj.y and w.z == obj.z:
            print(obj.name,"has collected a new weapon")
            obj.power += w.power
    for m in allmed:
        if m.x == obj.x and m.y == obj.y and m.z == obj.z:
            print(obj.name,"has collected medicine")
            print(obj.name,"hp is",obj.hp)
            obj.hp += m.heal
def alive(obj):
    return obj.hp>0
    
class Hero:
    def __init__(self,x,y,power,name = "NoName"):
        allplayers.append(self)
        self.name = name
        self.x = x
        self.y = y
        self.z = 0 
        self.hp = 10
        self.power = power
        print("hero",name,"is created")
        
    def run(self,dx,dy):
        print(self.name,"moves to",self.x + dx,self.y + dy)
        if alive(self):
            self.x += dx
            self.y += dy
            itemcheck(self)
            alive(self)
    def shoot(self,enemy):
        if alive(self):
            print(self.name,"fires at",enemy.name)
            enemy.hp -= self.power
            if not alive(enemy):
                print(enemy.name, "is dead")
            else:
                print(enemy.name,"hp is",enemy.hp)
                
class FlyingHero(Hero):
    def __init__(self,x,y,power,name):
        Hero.__init__(self,x,y,power,name)
        print("he can fly")
    def fly(self):
        print(self.name,"is flying")
        self.z += 1
    def land(self):
        print(self.name,"is landing")
        self.z -= 1
class Object:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
class Bomb(Object):
    def __init__(self,damage,x=random.randint(0,10),y=random.randint(0,10),z=random.randint(0,3)):
        Object.__init__(self,x,y,z)
        print("a new bomb has appeared",self.x,self.y,self.z)
        self.damage = damage
        allbombs.append(self)
class Weapon(Object):
    def __init__(self,x=random.randint(0,10),y=random.randint(0,10),z=random.randint(0,3)):
        Object.__init__(self,x,y,z)
        print("a new weapon has appeared")
        self.power = random.randint(1,10)
        allweapons.append(self)
class Medicine(Object):
    def __init__(self,x=random.randint(0,10),y=random.randint(0,10),z=random.randint(0,3)):
        Object.__init__(self,x,y,z)
        print("a new medicine has appeared")
        self.heal = random.randint(1,10)
        allmed.append(self)
hero1 = Hero(1,2,5,"link")
hero2 = Hero(0,0,6,"hjk")
hero1.shoot(hero2)
hero3 = FlyingHero(2,2,2,"a")
md = Medicine(1,1,0)
hero1.run(0,-1)
'''
hero link is created
hero hjk is created
link fires at hjk
hjk hp is 5
hero a is created
he can fly
a new medicine has appeared
link moves to 1 1
link has collected medicine
link hp is 10
'''

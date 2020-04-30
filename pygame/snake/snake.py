import pygame as pg
import random
import copy


pg.init()
pg.display.set_caption('Snake')

width,height = 800,800

DISPLAYSURF = pg.display.set_mode((width, height), 0, 32)
FPS = 50 # fps in second
fpsClock = pg.time.Clock()
squares=[]
#colors
Black = (0,0,0)
White = (255,255,255)
Blue = (0,0,255)
Green = (0,255,0)
Red = (255,0,0)

class Square():
    def __init__(self,i,j,color):
        self.i = i
        self.j = j
        self.color = color
        
        squares.append(self)
    def draw(self):
        pg.draw.rect(DISPLAYSURF,self.color,(self.i*10,self.j*10,10,10))
for i in range(80):
    for j in range(80):
        Square(i,j,Black)
        
class Snake():
    def __init__(self,i,j,color):
        self.color  = color
        self.body = [[i,j],[2,1]]
        self.dr = ''
        self.last=[2,1]
    def draw(self):
        for sq in self.body:
            pg.draw.rect(DISPLAYSURF,self.color,(sq[0]*10,sq[1]*10,10,10))
        
        
        
sn = Snake(1,1,Green)





def game(pts):
  
    font = (255,255,255)
    gen_food=True
    food_color = Red
    while True:
        
        
        for sq in squares:
            sq.draw()
        DISPLAYSURF.fill(font)
        
        if max([sn.body.count(el) for el in sn.body ])>1:
            score(pts)
            return 0
        sn.draw()
        
        if sn.dr:
            sn.last=copy.deepcopy(sn.body[-1])
            sn.body=[sn.body[0]]+copy.deepcopy(sn.body[:-1])
            if sn.body[0] == [food.i,food.j]:
                food.color=Black
                gen_food=True
                sn.body.append(sn.last)
                sn.color = random.sample(range(256),3)
                food_color = random.sample(range(256),3)
                font = random.sample(range(256),3)
                pts+=1
        if sn.dr == 'left':
            sn.body[0][0] = (sn.body[0][0]-1)%80
            
            
            
                        

        if sn.dr == 'right':
            sn.body[0][0] = (sn.body[0][0]+1)%80
            
            
        if sn.dr == 'up':
            sn.body[0][1] = (sn.body[0][1]-1)%80
            
                        

            
        if sn.dr == 'down':
            sn.body[0][1] = (sn.body[0][1]+1)%80        
                               
        if gen_food:
            food = random.choice(squares)
            food.color = food_color
            gen_food = False
        else:
            food.draw()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if sn.body[0] == [food.i,food.j]:
                        food.color=Black
                        gen_food=True
                        sn.body.append(sn.last)
                        sn.color = random.sample(range(256),3)
                        food_color = random.sample(range(256),3)
                        font = random.sample(range(256),3)
                        pts+=1
                
                
                    
                if event.key == pg.K_LEFT and sn.dr!='right':
                    sn.body=[sn.body[0]]+copy.deepcopy(sn.body[:-1])
                    sn.body[0][0] = (sn.body[0][0]-1)%80
                    sn.dr = 'left'
                    
                        
                if event.key == pg.K_RIGHT and sn.dr!='left':
                    sn.body=[sn.body[0]]+copy.deepcopy(sn.body[:-1])
                    sn.body[0][0] = (sn.body[0][0]+1)%80
                    sn.dr = 'right'
                    
                if event.key == pg.K_UP and sn.dr!='down':
                    sn.body=[sn.body[0]]+copy.deepcopy(sn.body[:-1])
                    sn.body[0][1] = (sn.body[0][1]-1)%80
                    sn.dr = 'up'
                    
                        
                if event.key == pg.K_DOWN and sn.dr!='up':
                    sn.body=[sn.body[0]]+copy.deepcopy(sn.body[:-1])
                    sn.body[0][1] = (sn.body[0][1]+1)%80
                    sn.dr = 'down'
                    
                
                
                            


            
        pg.display.update()
        fpsClock.tick(FPS)
def score(pts):
    f = open("scores.txt", "a")
    f.write(str(pts)+'\n')
    f.close()
    max_pts=0#read from the file
    f1 = open("scores.txt", "r")
    for l in f1.readlines():
        if int(l) > max_pts:
            max_pts=int(l)
        
    
    while True:
        
        DISPLAYSURF.fill(Black)

    
        DISPLAYSURF.blit(pg.font.SysFont('Comic Sans MS', 30).render('Your score: {0}'.format(pts), False, (255, 0, 0)),(300,300))
        DISPLAYSURF.blit(pg.font.SysFont('Comic Sans MS', 30).render('High score: {0}'.format(max_pts), False, (255, 0, 0)),(300,350))
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            
                
                
                            


            
        pg.display.update()
        fpsClock.tick(FPS)

game(0)

#score(1)

import pygame as pg
import sys
import random
import winsound
import astar
import math
import copy
import time

from pygame.locals import *
#colors
Light_Blue = (0, 255, 255)

Black = (0,   0,   0)

Blue=(0,  0, 255)

Fuchsia=(255,   0, 255)

Gray=(128, 128, 128)

Green=(0, 128,   0)

Lime=(0,255,0)

Maroon=(128,0,0)

Navy_Blue=(0,0, 128)

Olive=(128, 128,   0)

Purple=(128,0, 128)

Red=(255,   0,   0)

Silver=(192, 192, 192)

Teal=(0, 128, 128)

White=(255, 255, 255)

Yellow=(255, 255,   0)

Pink = (255,20,147)

Orange = (255,165,0)

#game images
p_left = pg.image.load('p_left.png')
p_left_eat = pg.image.load('p_left_eat.png')
p_right = pg.image.load('p_right.png')
p_right_eat = pg.image.load('p_right_eat.png')
p_up = pg.image.load('p_up.png')
p_up_eat = pg.image.load('p_up_eat.png')
p_down = pg.image.load('p_down.png')
p_down_eat = pg.image.load('p_down_eat.png')
sound_off = pg.image.load('sound_off.png')
sound_on = pg.image.load('sound_on.png')
gh_b = pg.image.load('b_ghost.png')
gh_o = pg.image.load('o_ghost.png')
gh_p = pg.image.load('p_ghost.png')
gh_r = pg.image.load('r_ghost.png')
gh_run_w = pg.image.load('running_ghost_w.png')
gh_run_b = pg.image.load('running_ghost_b.png')
cherry =  pg.image.load('cherry.png')
banana =  pg.image.load('banana.png')
strawberry = pg.image.load('strawberry.png')
d_gh= pg.image.load('dead_ghost.png')
b_pause = pg.image.load('b_pause.png')
b_unpause = pg.image.load('b_unpause.png')
home = pg.image.load('intro.png')
flag = pg.image.load('flag.png')
#intro images
name = pg.image.load('name.png')
gh_r_logo = pg.image.load('r_ghost_logo.png')
gh_b_logo = pg.image.load('b_ghost_logo.png')
gh_o_logo = pg.image.load('o_ghost_logo.png')
gh_p_logo = pg.image.load('p_ghost_logo.png')




#main
pg.init()
pg.display.set_caption('Pac-Man')
DISPLAYSURF = pg.display.set_mode((1010, 730), 0, 32)
FPS = 50 # кадров в секунду
fps_eat = 30 # кадров в секунду, еда
fpsClock = pg.time.Clock()
#координаты начала,конца и центра
upx,upy = 20,20
dx,dy = 980,660
cx,cy = (dx+upx)//2,(dy+upy)//2


#cursor
pg.mouse.set_cursor(*pg.cursors.broken_x)


#количество съеденной еды
eaten_food = 0 
#музыка
pg.mixer.init()
pg.mixer.music.load(r'bg_music.mp3')
pg.mixer.music.play(-1, 0.0)
pg.mixer.music.pause()

#все приведения
ghosts = []
#анимация курсора (глаз)
eyes = []
#тексты
texts=[]
#игровое поле - все клетки
squares_all = {}
#граф поля - список списков соседей
game_graph ={}
#все кнопки
buttons=[]
for i in range(upx,dx+1,40):
    for j in range(upy,dy+1,40):
        game_graph.update({(i,j):[]})
for i in game_graph.keys():
        v = list([((i[0]+40)%(dx+upx),i[1]),((i[0]-40)%(dx+upx),i[1]),(i[0],(i[1]+40)%(dy+upy)),(i[0],(i[1]-40)%(dy+upy))])
        for k in v:
            game_graph[i].append(k)
default_graph = copy.deepcopy(game_graph)

class Hero():
    def __init__(self,x,y,v=0):
       self.x = x
       self.y = y
       self.startx = x
       self.starty = y
       self.v = v
       self.v_stop = v
       self.motion = "STOP"
       
    def show(self):
        self.rect = self.image.get_rect(center =(self.x,self.y))
        DISPLAYSURF.blit(self.image, self.rect)
    def get_sq(self):#определение клетки игрока
        xsq = int(round(abs(self.x-upx)/40)*40+upx)
        ysq = int(round(abs(self.y-upy)/40)*40+upy)
        return (xsq,ysq)
class PacMan(Hero):
    def __init__(self,x,y,v):   
        Hero.__init__(self,x,y,v)
        self.image = pg.image.load('p_stop.png')
        self.lives = 3#оставшиеся жизни
        self.pts =  0#набранные очки
        self.eat = 0 #для смены картинок
    
class Ghost(Hero):
    def __init__(self,x,y,color,v):   
        Hero.__init__(self,x,y,v)
        if color == 'b':
            self.image = gh_b
            self.default_image = gh_b
            self.hide = (dx-40,dy)#клетка разбегания
        if color == 'p':
            self.image = gh_p
            self.default_image = gh_p
            self.hide = (dx-40,upy)
        if color == 'r':
            self.image = gh_r
            self.default_image = gh_r
            self.hide = (upx+40,upy)
        if color == 'o':
            self.image = gh_o
            self.default_image = gh_o
            self.hide = (upx+40,dy)
        self.color = color
        #частота смены картинок
        self.i = 0
        self.ghm = 0

        self.mode = "chase"
        self.last_sq = game_graph[(x,y)][0]
        
        
        ghosts.append(self)
    def aim(self):#целевые клетки приведений
        sq = pman.get_sq()
        col = self.color
        if col == "b":#для синего цель - конец отрезка между кр. и пк. доработать
            return random.choice(list(squares_all.keys()))
        if col == "p":#для розового цель - +4 клетки в сторону движения пэкмана
            if pman.motion == "STOP":
                return sq
            if pman.motion == "UP":
                for i in range(3,0,-1):
                    
                    if (sq[0],(sq[1]-i*40)%(dy+40-upy)) in game_graph.keys():
                        return (sq[0],(sq[1]-i*40)%(dy+40-upy))
                return sq
            if pman.motion == "DOWN":
                for i in range(3,0,-1):
                    
                    if (sq[0],(sq[1]+i*40)%(dy+40-upy)) in game_graph.keys():
                        return (sq[0],(sq[1]+i*40)%(dy+40-upy))
                return sq
            if pman.motion == "RIGHT":
                for i in range(3,0,-1):
                    
                    if ((sq[0]+i*40)%(dx+40-upx),sq[1])in game_graph.keys():
                        return ((sq[0]+i*40)%(dx+40-upx),sq[1])
                return sq
            if pman.motion == "LEFT":
                for i in range(3,0,-1):
                    
                    if ((sq[0]-i*40)%(dx+40-upx),sq[1]) in game_graph.keys():
                        return ((sq[0]-i*40)%(dx+40-upx),sq[1])

                return sq
        if col == "o":#для орж цель - сам пэкман, если до него меньше 8 клеток(иначе левый нижний угол)
            res = astar.a(sq,self.get_sq(),game_graph)
            if res and len(res)>=8:
                return sq
            else:
                return (upx+40,dy)
        if col == "r":#для красного цель - сам пэкман
            return sq
    
class Square():#клетки поля - в каждом еда - границы орределяют положение игрока
    def __init__(self,x,y,sides=[],color = Red,b_color = Blue):
        self.x=x
        self.y=y
        self.color = color
        self.b_color = b_color#цвет границы
        self.food = pg.Rect(self.x,self.y,5,5)#еда
        self.pts =10
        self.e = False #энерджайзер
        self.img = False#бонус
        self.img_rect = False#бонус
        self.centerx = self.food.centerx
        self.centery = self.food.centery
        self.borders = []
        self.get_borders(sides)
        self.sides=sides
        squares_all.update({(self.x,self.y):self})
        
    def draw_food(self):
        pg.draw.rect(DISPLAYSURF,self.color,self.food)
        if self.img and self.color!=Black:
            DISPLAYSURF.blit(self.img,self.img_rect)
    def get_borders(self,sides):
        self.borders=[]
        for i in sides:
            if i=="left":
                self.borders.append(pg.Rect(self.centerx - 20,self.centery -20,1,40))
            if i=="right":
                self.borders.append(pg.Rect(self.centerx + 20,self.centery -20,1,40))
            if i=="up":
                self.borders.append(pg.Rect(self.centerx -20,self.centery -20,40,1))
            if i=="down":
                self.borders.append(pg.Rect(self.centerx -20,self.centery +20,40,1))

    def draw_lines(self):
        for i in self.borders:
            pg.draw.rect(DISPLAYSURF,self.b_color,i)
#заполнение поля
for i in range(upx,dx+1,40):
    for j in range(upy,dy+1,40):
        Square(i,j)
#кнопки
class Button():
    def __init__(self,x,y,t):
        self.x = x
        self.y = y
        if t == "sound_off":
            self.sound = False
            self.image = sound_off
        if t == "pause":
            self.image = b_pause
        if t=="intro":
            self.image = home
        buttons.append(self)
    def show(self):
        self.rect = self.image.get_rect(center =(self.x,self.y))
        DISPLAYSURF.blit(self.image, self.rect)
#текст    
class text():
    def __init__(self,size,text,fg,bg,x,y):
        self.fontObj = pg.font.SysFont('microsoftsansserif', size)#change
        self.text = text
        self.x =x
        self.y = y
        self.textSurfaceObj = self.fontObj.render(self.text, True, fg, bg)
        self.textRectObj = self.textSurfaceObj.get_rect()
        self.textRectObj.center = (x,y)
        texts.append(self)
    def draw(self):
        DISPLAYSURF.blit(self.textSurfaceObj, self.textRectObj)
#глаз
class moving_eye():
    def __init__(self,r1,r2,start_x,start_y):
        self.r1 = r1
        self.r2 = r2
        self.start_x = start_x
        self.start_y = start_y
        eyes.append(self)
    def draw(self):
        pg.draw.circle(DISPLAYSURF, White, (self.start_x,self.start_y), self.r1)
        r = ((pg.mouse.get_pos()[0]- self.start_x)**2 + (pg.mouse.get_pos()[1]- self.start_y)**2)**0.5
        if r!=0:
            eye_x = int(self.start_x + self.r2*(pg.mouse.get_pos()[0]- self.start_x)/r)
            eye_y = int(self.start_y + self.r2*(pg.mouse.get_pos()[1]- self.start_y)/r)
        else:
            eye_x = self.start_x
            eye_y = self.start_y
        pg.draw.circle(DISPLAYSURF,Black,(eye_x,eye_y),self.r2)
        
        
        
    
def right_way(side):# можно ли пойти в данном направлении
        if side=="down":
            test_rect=pman.image.get_rect(center =(pman.x,pman.y+pman.v_stop))
            psq = pman.get_sq()
            chl = [squares_all[psq]]
            for sq in default_graph[psq]:
                chl.append(squares_all[sq])
            chl.append(squares_all[(psq[0]+40)%(dx+40-upx),(psq[1]+40)%(dy+40-upy)])
            chl.append(squares_all[(psq[0]+40)%(dx+40-upx),(psq[1]-40)%(dy+40-upy)])
            chl.append(squares_all[(psq[0]-40)%(dx+40-upx),(psq[1]+40)%(dy+40-upy)])
            chl.append(squares_all[(psq[0]-40)%(dx+40-upx),(psq[1]-40)%(dy+40-upy)])
            
            for sq in chl:
                for b in sq.borders:
                    if test_rect.colliderect(b):
                        
                        return False
            return True
        if side=="up":
            test_rect=pman.image.get_rect(center =(pman.x,pman.y-pman.v_stop))
            psq = pman.get_sq()
            chl = [squares_all[psq]]
            for sq in default_graph[psq]:
                chl.append(squares_all[sq])
            chl.append(squares_all[(psq[0]+40)%(dx+40-upx),(psq[1]+40)%(dy+40-upy)])
            chl.append(squares_all[(psq[0]+40)%(dx+40-upx),(psq[1]-40)%(dy+40-upy)])
            chl.append(squares_all[(psq[0]-40)%(dx+40-upx),(psq[1]+40)%(dy+40-upy)])
            chl.append(squares_all[(psq[0]-40)%(dx+40-upx),(psq[1]-40)%(dy+40-upy)])            
            for sq in chl:
                
                for b in sq.borders:
                    if test_rect.colliderect(b):
                        
                        return False
            return True
        if side=="left":
            test_rect=pman.image.get_rect(center =(pman.x-pman.v_stop,pman.y))
            psq = pman.get_sq()
            chl = [squares_all[psq]]
            for sq in default_graph[psq]:
                chl.append(squares_all[sq])
            chl.append(squares_all[(psq[0]+40)%(dx+40-upx),(psq[1]+40)%(dy+40-upy)])
            chl.append(squares_all[(psq[0]+40)%(dx+40-upx),(psq[1]-40)%(dy+40-upy)])
            chl.append(squares_all[(psq[0]-40)%(dx+40-upx),(psq[1]+40)%(dy+40-upy)])
            chl.append(squares_all[(psq[0]-40)%(dx+40-upx),(psq[1]-40)%(dy+40-upy)])
           
            for sq in chl:
                
                
                for b in sq.borders:
                    if test_rect.colliderect(b):
                        
                        return False
            return True
        if side=="right":
            test_rect=pman.image.get_rect(center =(pman.x+pman.v_stop,pman.y))
            psq = pman.get_sq()
            try:
                chl = [squares_all[psq]]
            except:
                print(pman.x,pman.y)
            for sq in default_graph[psq]:
                chl.append(squares_all[sq])
            chl.append(squares_all[(psq[0]+40)%(dx+40-upx),(psq[1]+40)%(dy+40-upy)])
            chl.append(squares_all[(psq[0]+40)%(dx+40-upx),(psq[1]-40)%(dy+40-upy)])
            chl.append(squares_all[(psq[0]-40)%(dx+40-upx),(psq[1]+40)%(dy+40-upy)])
            chl.append(squares_all[(psq[0]-40)%(dx+40-upx),(psq[1]-40)%(dy+40-upy)])
            for sq in chl:
                for b in sq.borders:
                    if test_rect.colliderect(b):
                        
                        return False
            return True
   
pman = PacMan(upx+40,upy,2)
b_gh = Ghost(cx-3*40,cy+3*40,"b",3)
r_gh = Ghost(cx+3*40,cy-3*40,"r",3)
p_gh = Ghost(cx+3*40,cy+3*40,"p",3)
o_gh = Ghost(cx-3*40,cy-3*40,"o",3)
bs = Button(950,710,"sound_off")
bp = Button(990,710,"pause")
hm = Button(910,710,"intro")
max_score = 0
#изменить границы квадрата
def change_borders(x,y,sides,nofood = True,append=False):
    sq1 = squares_all[(x,y)]
    if not(append):
        sq1.get_borders(sides)
        sq1.sides=sides
    else:
        sides = list(set(sq1.sides+sides))
        sq1.sides=sides
        sq1.get_borders(sides)
        
    if nofood:
        sq1.color = Black# убираем еду
    xsq = x
    ysq = y
    vn = (xsq,ysq)#текушая вершина
    #изменяем граф
    nv = ((xsq-40)%(dx+40-upx),ysq)
    if "left" in sides:
        if nv in game_graph[vn]:
            game_graph[vn].remove(nv)
            try:
                game_graph[nv].remove(vn)
            except:
                print(nv,vn,'l')
        
    elif not(append) and not(nv in game_graph[vn]):
        game_graph[vn].append(nv)
        game_graph[nv].append(vn)
    nv = ((xsq+40)%(dx+40-upx),ysq)
    if "right" in sides:
        if nv in game_graph[vn]:
            game_graph[vn].remove(nv)
            try:
                game_graph[nv].remove(vn)
            except:
                print(nv,vn,'r')
        
    elif not(append) and not(nv in game_graph[vn]):
        game_graph[vn].append(nv)
        game_graph[nv].append(vn)
    nv = (xsq,(ysq-40)%(dy+40-upy))
    if "up" in sides:
        if nv in game_graph[vn]:
            game_graph[vn].remove(nv)
            try:
                game_graph[nv].remove(vn)
            except:
                print(nv,vn,'u')
        
    elif not(append) and not(nv in game_graph[vn]):
        game_graph[vn].append(nv)
        game_graph[nv].append(vn)
    nv = (xsq,(ysq+40)%(dy+40-upy))
    if "down" in sides:
        if nv in game_graph[vn]:
            game_graph[vn].remove(nv)
            try:
                game_graph[nv].remove(vn)
            except:
                print(nv,vn,'d')
        
    elif not(append) and not(nv in game_graph[vn]):
        game_graph[vn].append(nv)
        game_graph[nv].append(vn)
            

        
#нарисовать квадрат по двум крайним точкам
def draw_rect(upx,upy,dx,dy):
    if upx>dx:
        upx,dx = dx,upx
    if upy>dy:
        upy,dy = dy,upy
    if upx==dx and upy==dy:
        change_borders(upx,upy,["up","down","right","left"])  
    elif upx==dx:
        change_borders(upx,upy,["up","right","left"])
        change_borders(upx,dy,["down","right","left"])
        for i in range(upy+40,dy,40):
            change_borders(upx,i,["left","right"])
    elif upy==dy:
        change_borders(upx,upy,["down","up","left"])
        change_borders(dx,upy,["down","up","right"])
        for i in range(upx+40,dx,40):
            change_borders(i,upy,["up","down"])
            
    else:
        change_borders(upx,upy,["up","left"])
        change_borders(upx,dy,["down","left"])
        change_borders(dx,upy,["up","right"])
        change_borders(dx,dy,["down","right"])
        for i in range(upx+40,dx,40):
            change_borders(i,upy,["up"])
            change_borders(i,dy,["down"])
        for i in range(upy+40,dy,40):
            change_borders(upx,i,["left"])
            change_borders(dx,i,["right"])
        
def maze(upx,upy,dx,dy,n):#доделать
    if abs(upx-dx)<=0 or abs(upy-dy)<=0:
        return None
        
    
    
    cx = upx+40*math.ceil((((dx-upx)/40)/2))
    cy = upy+40*math.ceil((((dy-upy)/40)/2))
    doors = []
    extr1=False
    extr2=False
    ch = random.sample([1,2,3,4],3)
    if 1 in ch:
        doors.append(random.choice([(i,cy) for i in range(upx,cx,40)]))
    if 2 in ch:
        tmp = random.choice([(i,cy) for i in range(cx,dx+1,40)])
        if tmp == (cx,cy):
            extr1 = True
        doors.append(tmp)
    if 3 in ch:
        doors.append(random.choice([(cx,j) for j in range(upy,cy,40)]))
    if 4 in ch:
        tmp = random.choice([(cx,j) for j in range(cy,dy+1,40)])
        if tmp == (cx,cy):
            extr2 = True
        doors.append(tmp)
    
    for i in range(upx,dx+1,40):
        if not((i,cy) in doors) and i!=cx:
            change_borders(i,cy,["up"],False,True)
    for j in range(upy,dy+1,40):
        if not((cx,j) in doors) and j!=cy:
            change_borders(cx,j,["left"],False,True)
    if (cx,cy) in doors:
        if not(extr1 and extr2):
            if extr1:
                change_borders(cx,cy,["left"],False,True)
            if extr2:
                change_borders(cx,cy,["up"],False,True)
    else:
        change_borders(cx,cy,["left","up"],False,True)
    
    
    
    maze(upx,upy,cx-40,cy-40,n+1)
    maze(cx,cy,dx,dy,n+1)
    maze(cx,upy,dx,cy-40,n+1)
    maze(upx,cy,cx-40,dy,n+1)
    
    
    
    
    
    
    
    
    
#границы - разные для разных уровней
def start_borders(n):#все обнуляется
    global max_score
    max_score = 0
    global game_graph
    game_graph = copy.deepcopy(default_graph)
    for sq in squares_all.values():
        sq.color = Red
        sq.pts =10
        sq.e = False
        sq.food = pg.Rect(sq.x,sq.y,5,5)
        sq.img = False#бонус
        sq.img_rect = False#бонус
        sq.sides=[]
        sq.borders = []
        sq.get_borders([])
    for gh in ghosts:
        gh.start_time = time.perf_counter()
        gh.image = gh.default_image
        gh.mode = "chase"
        gh.x,gh.y = gh.startx,gh.starty
        gh.last_sq=game_graph[(gh.x,gh.y)][0]
        gh.i=0
        gh.ghm=0
    pman.lives=3
    pman.x,pman.y = pman.startx,pman.starty
    pman.motion = "STOP"
    pman.pts=0
    if n==1:
        change_borders(upx,upy,["up","left"],False)#40 по x и y между клетками
        change_borders(dx,dy,["right","down"],False)
        change_borders(upx,dy,["down","left"],False)
        change_borders(dx,upy,["up","right"],False)
        for i in range(1,24):#верхняя граница
            if i == 12:
                continue
            change_borders(upx+i*40,upy,["up"],False)
        for i in range(1,24):#нижняя граница
            if i == 12:
                continue
            change_borders(upx+i*40,dy,["down"],False)
        for i in range(2,15):#левая граница
            if i%4:
                change_borders(upx,upy+i*40,["left"],False)
        for i in range(2,15):#правая граница
            if i%4:
                change_borders(dx,upy+i*40,["right"],False)
        #четверть лабиринта - затем отразить
        for j in [1,-1]:
            if j== 1:
                u = "up"
                d = "down"
            else:
                u = "down"
                d = "up"
            for i in [1,-1]:
                if i == 1:
                    l = "left"
                    r = "right"
                else:
                    r = "left"
                    l = "right"
                draw_rect(cx-i*12*40,cy-j*8*40,cx-i*12*40,cy-j*8*40)
                draw_rect(cx-i*10*40,cy-j*8*40,cx-i*10*40,cy-j*8*40)
                draw_rect(cx-i*8*40,cy-j*8*40,cx-i*8*40,cy-j*5*40)
                draw_rect(cx-i*40*4,cy-j*8*40,cx-i*40,cy-j*8*40)
                draw_rect(cx-i*6*40,cy-j*40*7,cx-i*6*40,cy-j*5*40)
                draw_rect(cx-i*6*40,cy-j*6*40,cx-i*4*40,cy-j*6*40)
                change_borders(cx-i*6*40,cy-j*6*40,[l])
                draw_rect(cx-i*12*40,cy-j*6*40,cx-i*10*40,cy-j*5*40)
                draw_rect(cx-i*10*40,cy-j*5*40,cx-i*10*40,cy-j*3*40)
                change_borders(cx-i*10*40,cy-j*5*40,[r])
                draw_rect(cx-i*12*40,cy-j*3*40,cx-i*12*40,cy-j*40)
                draw_rect(cx-i*12*40,cy-j*40,cx-i*10*40,cy-j*40)
                change_borders(cx-i*12*40,cy-j*40,[l,d])
                draw_rect(cx-i*8*40,cy-j*3*40,cx-i*8*40,cy-j*40)
                draw_rect(cx-i*8*40,cy-j*40,cx-i*6*40,cy-j*40)
                change_borders(cx-i*8*40,cy-j*40,[l,d])
                draw_rect(cx-i*2*40,cy-j*2*40,cx-i*40,cy-j*40)
                draw_rect(cx-i*6*40,cy-j*3*40,cx-i*4*40,cy-j*3*40)
                draw_rect(cx-i*4*40,cy-j*4*40,cx-i*4*40,cy-j*2*40)
                draw_rect(cx-i*4*40,cy-j*4*40,cx-i*40,cy-j*4*40)
                draw_rect(cx-i*2*40,cy-j*6*40,cx-i*2*40,cy-j*4*40)
                change_borders(cx-i*4*40,cy-j*3*40,[r])
                change_borders(cx-i*4*40,cy-j*4*40,[l,u])
                change_borders(cx-i*2*40,cy-j*4*40,[d])
       #центральная линия
            draw_rect(cx,cy-6*40,cx,cy-6*40)
            draw_rect(cx,cy+6*40,cx,cy+6*40)
            draw_rect(cx-4*40,cy,cx-4*40,cy)
            draw_rect(cx+4*40,cy,cx+4*40,cy)
        energy(5)#энерджайзер - 5 случайных клеток
    else:
        change_borders(upx,upy,["up","left"],False)#40 по x и y между клетками
        change_borders(dx,dy,["right","down"],False)
        change_borders(upx,dy,["down","left"],False)
        change_borders(dx,upy,["up","right"],False)
        for i in range(1,24):#верхняя граница
            change_borders(upx+i*40,upy,["up"],False)
        for i in range(1,24):#нижняя граница
            change_borders(upx+i*40,dy,["down"],False)
        for i in range(1,16):#левая граница
            
            change_borders(upx,upy+i*40,["left"],False)
        for i in range(1,16):#правая граница
            change_borders(dx,upy+i*40,["right"],False)
        maze(upx,upy,dx,dy,1)#генерация лабиринта
        energy(15)
        sqr = squares_all[(cx,cy)]
        sqr.img = flag
        sqr.img_rect = sqr.img.get_rect(center = (sqr.x,sqr.y))
    for sq in squares_all.values():
        if  sq.color != Black:
            max_score+=sq.pts
   
                    
                
                    
                
                
            
                
            
            
        
            
            
        

           
#прорисовка границ и еды - разная в зависимости от intro
def draw_borders(intro = False):
    if intro:
        for sq in squares_all.values():
            sq.draw_lines()
    else:
        for sq in squares_all.values():
            sq.draw_lines()
            sq.draw_food()
    
    
def energy(n):#энерджайзер
    squares = [sq for sq in squares_all.values() if sq.color != Black and sq.img!=flag]
    for sqr in random.sample(squares,n):
        sqr.food = pg.Rect(sqr.x,sqr.y,7,7)
        sqr.pts = 50
        sqr.e = True
        squares.remove(sqr)
    sqr = random.choice(squares)
    sqr.img = random.choice([cherry,strawberry,banana])
    sqr.img_rect = sqr.img.get_rect(center = (sqr.x,sqr.y))
    sqr.pts = 100
        
        

# игровое меню
def game_intro():
    gen_maze = 1
    intro =True
    #текст
    text(10, "A.K. 2019 ©",White,Black,dx-40,dy+40)
    start = text(30,"Start Game",Yellow,Black,cx-4*40,upy+14*40)
    e_maze = text(15,"Easy(classic pacman)",Yellow,Black,cx-6*40,upx+15*40)
    h_maze = text(15,"Hard(capture the flag)",Yellow,Black,cx-6*40,upx+16*40)
    #глаз за курсором
    r_gh_x,r_gh_y = upx+18*40,dy-5*40
    moving_eye(10,5,r_gh_x-9,r_gh_y-10)
    moving_eye(10,5,r_gh_x+9,r_gh_y-10)

    b_gh_x,b_gh_y = upx+14*40,dy-5*40
    moving_eye(10,5,b_gh_x-9,b_gh_y-10)
    moving_eye(10,5,b_gh_x+9,b_gh_y-10)

    o_gh_x,o_gh_y = upx+10*40,dy-5*40
    moving_eye(10,5,o_gh_x-9,o_gh_y-10)
    moving_eye(10,5,o_gh_x+9,o_gh_y-10)

    p_gh_x,p_gh_y = upx+6*40,dy-5*40
    moving_eye(10,5,p_gh_x-9,p_gh_y-10)
    moving_eye(10,5,p_gh_x+9,p_gh_y-10)
    
    
    while intro:
        DISPLAYSURF.fill(Black)
        #текст
        for t in texts:
            t.draw()
        
        DISPLAYSURF.blit(name, name.get_rect(center =(cx,cy-3*40)))
        #глаз за курсором
        DISPLAYSURF.blit(gh_r_logo, gh_r_logo.get_rect(center = (r_gh_x,r_gh_y)))
        DISPLAYSURF.blit(gh_b_logo, gh_b_logo.get_rect(center = (b_gh_x,b_gh_y)))
        DISPLAYSURF.blit(gh_o_logo, gh_o_logo.get_rect(center = (o_gh_x,o_gh_y)))
        DISPLAYSURF.blit(gh_p_logo, gh_p_logo.get_rect(center = (p_gh_x,p_gh_y)))

        if gen_maze==1:
            pg.draw.circle(DISPLAYSURF,Green,(e_maze.textRectObj[0]-7,e_maze.y),5)
        elif gen_maze==2:
            pg.draw.circle(DISPLAYSURF,Green,(h_maze.textRectObj[0]-7,h_maze.y),5)
        for e in eyes:
            e.draw()
            
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONUP:
                if start.textRectObj.collidepoint(pg.mouse.get_pos()):
                    intro = False
                    texts.clear()
                    start_borders(gen_maze)
                    global score
                    score = text(15,'Score: '+str(pman.pts),White, Black,upx+40, dy+45)   
                    text(15,'SHADOW',Red,Black,dx-3*40, dy+45)
                    text(15,'SPEEDY',Pink,Black,dx-6*40, dy+45)
                    text(15,'BASHFUL',Light_Blue,Black,dx-9*40, dy+45)
                    text(15,'POKEY',Orange,Black,dx-12*40, dy+45,)
                    game()
                if e_maze.textRectObj.collidepoint(pg.mouse.get_pos()):
                    gen_maze=1
                if h_maze.textRectObj.collidepoint(pg.mouse.get_pos()):
                    gen_maze=2
                
            

        
        pg.display.update()
        fpsClock.tick(FPS)
# запуск игры
def game():
    chase_time = 10
    scatter_time = 5
    frightened_time = 20
    global score
    gh_v =30
    running = True
    while running:
        #очищение экрана
        DISPLAYSURF.fill(Black)
         
        # вставить текст:
        score.text = 'Score: '+str(pman.pts)
        score.textSurfaceObj = score.fontObj.render(score.text, True, White, Black)
        for t in texts:
            t.draw()
        
       

        
    
        #жизни
        for i in range (pman.lives):
            DISPLAYSURF.blit(p_right, pg.Rect(dx-(20-i)*40,dy+30,20,20))
        

        #кнопка
        for b in buttons:
            b.show()
        #границы
        draw_borders()
       
        pman.show()
        for gh in ghosts:
            gh.show()
            
            if gh.rect.colliderect(pman.rect):#пэкман пойман - reset
                running = False
                if gh.mode!="frightened":
                    pman.lives -= 1
                    pman.x = pman.startx
                    pman.y = pman.starty
                    for gh in ghosts:
                        gh.x = gh.startx
                        gh.y = gh.starty
                    pman.motion = "STOP"
                    if pman.lives>-1:
                        running = True
                    else:
                        pg.mixer.music.stop()
                        texts.clear()
                        lose_page(pman.pts)
                elif gh.image!=d_gh:
                    pman.pts+=100
                    running = True
                    gh.image = d_gh
                    gh.move = astar.a(gh.get_sq(),(gh.startx,gh.starty),game_graph)
                else:
                    running = True
            
            
            
                
            
            if len(game_graph[gh.get_sq()])!=2 or gh.image == d_gh:#менять направление только на развилках
                gh.i = 0
                if gh.mode == "chase":
                    gh.move = astar.a(gh.get_sq(),gh.aim(),game_graph)
                    
                    if time.perf_counter() -  gh.start_time >= chase_time:
                        gh.mode = "scatter"
                        gh.start_time = time.perf_counter()
                if gh.mode == "scatter":
                    gh.move = astar.a(gh.get_sq(),gh.hide,game_graph)
                    if time.perf_counter() -  gh.start_time >= scatter_time:
                        gh.mode = "chase"
                        gh.start_time = time.perf_counter()
                if gh.image == d_gh:
                    gh.move = astar.a(gh.get_sq(),(gh.startx,gh.starty),game_graph)
                    if gh.get_sq() == (gh.startx,gh.starty):
                        gh.mode = "chase"
                        gh.image = gh.default_image
                        gh.start_time = time.perf_counter()
                        
                elif gh.mode == "frightened":
                    gh.move = [random.choice(game_graph[gh.get_sq()])]
                    if time.perf_counter() -  gh.start_time >= frightened_time:
                        gh.image = gh.default_image
                        gh.mode = "chase"
                        gh.start_time = time.perf_counter()
                            
                        
            else:
                gh.i=0
                if game_graph[gh.get_sq()][0] != gh.last_sq:
                    gh.move = [game_graph[gh.get_sq()][0]]
                else:
                    gh.move = [game_graph[gh.get_sq()][1]]
                
            if gh.move!=False and gh.i<len(gh.move):
                gh.ghm +=1
                if not(gh.ghm%gh_v):
                    gh.last_sq = gh.get_sq()
                    gh.x = gh.move[gh.i][0]
                    gh.y = gh.move[gh.i][1]
                    gh.i += 1
                    if gh.mode == "frightened" and gh.image!=d_gh:
                        if gh.image == gh_run_w:
                            gh.image = gh_run_b
                        else:
                            gh.image = gh_run_w
                    gh.ghm=(gh.ghm+1)%(gh_v)
            
        
            
                    
        pg.display.update()
        
        sq = squares_all[pman.get_sq()]
        if pman.rect.contains(sq.food):#если rect_еда внутри rect_pacman
            if sq.color != Black:
                sq.color = Black #сделать еду невидимой
                pman.pts += sq.pts#очки за 1 еду
                if sq.e:
                    for gh in ghosts:
                        if gh.image != d_gh:
                            gh.mode = "frightened"
                            gh.image =  gh_run_w
                            start_time = time.perf_counter()
                if sq.img == flag:
                    running=False
                    texts.clear()
                    win_page(pman.pts)
                if sq.img:
                    sq.img =False
            #проверка max_score
            if pman.pts>=max_score:
                running=False
                texts.clear()
                win_page(pman.pts)
        for event in pg.event.get():
            
            
            if event.type == QUIT:
                
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONUP:#нажатие, bs,bp - кнопки
                
                if bs.rect.collidepoint(pg.mouse.get_pos()):
                    if bs.sound:
                        pg.mixer.music.pause()
                        bs.image = sound_off
                        bs.sound = False
                    else:
                        pg.mixer.music.unpause()
                        bs.image = sound_on
                        bs.sound =True
                if bp.rect.collidepoint(pg.mouse.get_pos()):
                    bp.image = b_unpause
                    bp.show()
                    running = False
                    pause_menu()
                if hm.rect.collidepoint(pg.mouse.get_pos()):#доделать
                    running=False
                    texts.clear()
                    game_intro()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT and right_way("left"):
                    pman.x -= pman.v
                    pman.motion = "LEFT"
                    
                elif event.key == pg.K_RIGHT and right_way("right"):
                    pman.x += pman.v
                    pman.motion = "RIGHT"
                elif event.key == pg.K_UP and right_way("up"):
                    pman.y -= pman.v
                    pman.motion = "UP"
                elif event.key == pg.K_DOWN and right_way("down"):
                    pman.y += pman.v
                    pman.motion = "DOWN"
                elif event.key == pg.K_LSHIFT:#stop
                    pman.v=0
                elif event.key == pg.K_RSHIFT:#hack
                    pman.v+=1
                    
        if pman.motion == "LEFT" and right_way("left"):
            pman.x -= pman.v
            if pman.eat%fps_eat >= fps_eat//2:
                pman.image = p_left
                
            else:
                pman.image = p_left_eat
                
            if pman.x <= upx-16:
                pman.x = dx+16
            pman.eat = (pman.eat+1)%fps_eat#чередование картинок
        if pman.motion == "RIGHT" and right_way("right"):
            pman.x += pman.v
            if pman.eat%fps_eat >= fps_eat//2:
                pman.image =p_right
                
            else:
                pman.image = p_right_eat
                
            if pman.x >= dx+16:
                pman.x = upx-16
            pman.eat = (pman.eat+1)%fps_eat#чередование картинок
        if pman.motion == "UP" and right_way("up"):
            pman.y -= pman.v
            if pman.eat%fps_eat >= fps_eat//2:
                pman.image = p_up
                
            else:
                pman.image = p_up_eat
                
            if pman.y <= upy-16:
                pman.y = dy+16
            pman.eat = (pman.eat+1)%fps_eat#чередование картинок
        if pman.motion == "DOWN" and right_way("down"):
            pman.y += pman.v
            if pman.eat%fps_eat >= fps_eat//2:
                pman.image = p_down
                
                
            else:
                pman.image = p_down_eat
                
            if pman.y >= dy+16:
                pman.y = upy-16
            pman.eat = (pman.eat+1)%fps_eat#чередование картинок

            
            

                
        
        fpsClock.tick(FPS)

def pause_menu():
    running = True
    while running:
        bp.show()
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONUP:
                if bp.rect.collidepoint(pg.mouse.get_pos()):
                    bp.image = b_pause
                    running = False
                    game()
            if event.type == QUIT:
                pg.quit()
                sys.exit()
        pg.display.update()
        fpsClock.tick(FPS)
                    
def win_page(score):
    DISPLAYSURF.fill(Black)
    running = True
    text(40,'YOU WIN',Red,Black,cx, cy)
    text(20,'YOUR SCORE: '+str(score),Red,Black,cx,cy+2*40)
    
    while running:
        hm.show()
        for t in texts:
            t.draw()
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONUP:
                if hm.rect.collidepoint(pg.mouse.get_pos()):
                    texts.clear()
                    running = False
                    game_intro()
            if event.type == QUIT:
                pg.quit()
                sys.exit()
        pg.display.update()
        fpsClock.tick(FPS)
def lose_page(score):
    DISPLAYSURF.fill(Black)
    running = True
    text(40,'YOU LOSE',Red,Black,cx, cy)
    text(20,'YOUR SCORE: '+str(score),Red,Black,cx,cy+2*40)
    while running:
        hm.show()
        for t in texts:
            t.draw()
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONUP:
                if hm.rect.collidepoint(pg.mouse.get_pos()):
                    texts.clear()
                    running = False
                    game_intro()
            if event.type == QUIT:
                pg.quit()
                sys.exit()
        pg.display.update()
        fpsClock.tick(FPS)
       
game_intro()


import pygame as pg
import random



pg.init()
pg.display.set_caption('Tetris')

width,height = 600,900

DISPLAYSURF = pg.display.set_mode((width+120, height+40), 0, 32)
FPS = 50 # fps in second
fpsClock = pg.time.Clock()
squares={}
figures =[]
size_x =width//40+1
size_y =height//40+1
fig_types=[[(size_x//2,1),(size_x//2,0),(size_x//2,2),(size_x//2-1,2)],[(size_x//2,1),(size_x//2+1,0),(size_x//2,0),(size_x//2+1,1)],
           [(size_x//2,0),(size_x//2+1,0),(size_x//2+2,0),(size_x//2-1,0)],[(size_x//2,0),(size_x//2-1,0),(size_x//2,1),(size_x//2+1,1)],
           [(size_x//2,1),(size_x//2,0),(size_x//2+1,1),(size_x//2-1,1)],[(size_x//2,1),(size_x//2,0),(size_x//2-1,1),(size_x//2+1,0)],
           [(size_x//2,1),(size_x//2,0),(size_x//2,2),(size_x//2+1,2)]]
border=3#overload higher

class Square():
    def __init__(self,i,j,color):
        self.i = i
        self.j = j
        self.color = color
        self.emp = True#no figure
        squares.update({(i,j):self})
    def draw(self):
        pg.draw.rect(DISPLAYSURF,self.color,(self.i*40,self.j*40,40,40))
        
        

for i in range(1,size_x):
    for j in range(size_y):
        Square(i,j,(0,0,0))
        
class Figure():
    def __init__(self,body,color):
        self.body = body
        self.color = color
        figures.append(self)
    def move_right(self):
        self.body =[(x[0]+1,x[1]) for x in self.body]
    def move_left(self):
        self.body =[(x[0]-1,x[1]) for x in self.body]
    def move_down(self):
        self.body =[(x[0],x[1]+1) for x in self.body]
    def turn(self):
        os = self.body[0]
        self.body=[(-(x[1]-os[1])+os[0],(x[0]-os[0])+os[1])for x in self.body]
    def draw(self):#изменение цветов квадратов
        for x in self.body:
            squares[x].color = self.color
    def fill(self):#изменение заполненности квадратов - кроме текущей фигуры
        for x in self.body:
            squares[x].emp = False
            
            
        

def test(fig,sqs):
    
        
    for sq in fig:
        if not(sqs[sq].emp):
            #print(sq)
            return False
    return True

def draw_net():
    for i in range(1,size_x):
        for j in range(size_y):
            if j==border:
                pg.draw.line(DISPLAYSURF,(255,0,0),(i*40,j*40),((i+1)*40,j*40),3)
                pg.draw.line(DISPLAYSURF,(128,128,128),(i*40,j*40),(i*40,(j+1)*40),3)
            else:
                pg.draw.line(DISPLAYSURF,(128,128,128),(i*40,j*40),((i+1)*40,j*40),3)
                pg.draw.line(DISPLAYSURF,(128,128,128),(i*40,j*40),(i*40,(j+1)*40),3)
    pg.draw.line(DISPLAYSURF,(128,128,128),(size_x*40,0),(size_x*40,size_y*40),3)
    pg.draw.line(DISPLAYSURF,(128,128,128),(40,size_y*40),(size_x*40,size_y*40),3)


def game(pts):
    running = True
    cur_fig = False
    v=20#скорость падения - чем больше,тем медленнее
    fps = 0#частота
    motion = 'STOP'
    pts=0
    while running:
        DISPLAYSURF.fill((0,0,128))
        
        for sq in squares.values():
            sq.color =  (255,255,255)
            sq.emp = True
        for f in figures:
            f.draw()
            if f!=cur_fig:
                f.fill()
        for sq in squares.values():
            sq.draw()
        draw_net() 
        if not(cur_fig):  
            cur_fig = Figure(random.choice(fig_types),random.choices(range(10,245),k=3))
       
        
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    if  min([x[0] for x in cur_fig.body])-1>0 and test([(x[0]-1,x[1]) for x in cur_fig.body],squares):
                        motion = 'LEFT'
            
                if event.key == pg.K_RIGHT:
                    if  max([x[0] for x in cur_fig.body])+1<(size_x) and test([(x[0]+1,x[1]) for x in cur_fig.body],squares):
                        motion = 'RIGHT'
                if event.key == pg.K_DOWN:
                    if  max([x[1] for x in cur_fig.body])+1<(size_y) and test([(x[0],x[1]+1) for x in cur_fig.body],squares):
                        motion = 'DOWN'
                if event.key == pg.K_UP:
                    if max([-(x[1]-cur_fig.body[0][1])+cur_fig.body[0][0] for x in cur_fig.body[1:]])<size_x and min([-(x[1]-cur_fig.body[0][1])+cur_fig.body[0][0] for x in cur_fig.body[1:]])>0 and max([x[0]-cur_fig.body[0][0]+cur_fig.body[0][1] for x in cur_fig.body[1:]])<size_y and min([x[0]-cur_fig.body[0][0]+cur_fig.body[0][1] for x in cur_fig.body[1:]])>0 and  test([(-(x[1]-cur_fig.body[0][1])+cur_fig.body[0][0],(x[0]-cur_fig.body[0][0])+cur_fig.body[0][1]) for x in cur_fig.body],squares):
                        cur_fig.turn()
            if event.type == pg.KEYUP:
                if event.key in [pg.K_LEFT, pg.K_RIGHT,pg.K_DOWN,pg.K_UP]:
                    motion='STOP'
           
        
        if not(fps%4):# v_left= v_right = v_down =4      
            if motion == 'LEFT' and  min([x[0] for x in cur_fig.body])-1>0 and test([(x[0]-1,x[1]) for x in cur_fig.body],squares):
                cur_fig.move_left()
            elif motion == 'RIGHT' and max([x[0] for x in cur_fig.body])+1<(size_x) and test([(x[0]+1,x[1]) for x in cur_fig.body],squares):
                cur_fig.move_right()
            elif motion == 'DOWN' and max([x[1] for x in cur_fig.body])+1<(size_y) and test([(x[0],x[1]+1) for x in cur_fig.body],squares):
                cur_fig.move_down()
           
            

        
        if max([x[1] for x in cur_fig.body])+1<(size_y) and test([(x[0],x[1]+1) for x in cur_fig.body],squares):
                if not(fps%v):
                    cur_fig.move_down()
                    
               
        else:#clear lines
            cur_fig.fill()
            y_min =min([x[1] for x in cur_fig.body])
            y_max=max([x[1] for x in cur_fig.body])
            for y in range(y_min,y_max+1):
                s=0
                for x in range(1,size_x):
                    if not(squares[(x,y)].emp):
                        s+=1
                    else:
                        continue
                if s==size_x-1:#full line
                    pts+=s
                    
                    for f in figures:
                        r=[]
                        
                        for sq in f.body:
                            if sq[1]!=y:
                                if sq[1]>y:
                                    r.append((sq[0],sq[1]))
                                else:
                                    r.append((sq[0],sq[1]+1))
                            
                            f.body=r
            if min([x[1] for x in cur_fig.body])<=1:
                running = False
                #pg.quit()
            cur_fig=False

            
        fps=(fps+1)%v
        DISPLAYSURF.blit(pg.font.SysFont('Comic Sans MS', 20).render('{0}'.format(pts), False, (255, 0, 0)),(width+70,height//2))
        pg.display.update()
        fpsClock.tick(FPS)


game(0)



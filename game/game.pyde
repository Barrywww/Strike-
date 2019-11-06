"""
Created on Wed Nov 6 22:36:16 2019
@author: Barry Wang
"""
from random import *
import time
add_library('minim')
class Balls():
    def __init__(self,x,y,vx,vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
    def update(self):
        fill(255)
        self.s = ellipse(self.x,self.y,5,5)
        self.x -= self.vx * 3
        self.y -= self.vy * 3
class Bricks():
    def __init__(self):
        self.x = randrange(25,975)
        self.y = 0
        self.vy = 5
    def update(self):
        fill(255)
        rectMode(CENTER)
        self.r = rect(self.x,self.y,25,25)
        self.y += self.vy * 0.3
deg = 90   
score = 0  
weapon = 10
hp = 5
start = False
dead = False
def setup():
    frameRate(60)
    global ball_lst,brick_lst
    size(1000,1000)
    background(0)
    ball_lst = []
    brick_lst = []
    angle = 0
    global count
    count = 0
    global bgl
    bgl = []
    textSize(100)
    textAlign(CENTER)
    text("Strike!",500,400)
    textSize(30)
    text("Press SPACEBAR to shoot, LEFT&RIGHT to rotate",500,800)
    for i in range(100):
        bgl.append((randrange(1000),randrange(1000)))
    for i in bgl:
        stroke(255)
        strokeWeight(1)
        point(i[0],i[1])
    minim = Minim(this)
    # rectMode(CENTER)
    # noFill()
    # rect(500,600,250,80)
    textSize(40)
    fill(255)
    text("-Start-",500,610)
    text("-Exit-",500,710)
    global shoot, hit, over, bgm
    shoot = minim.loadSample("shoot.mp3")
    hit = minim.loadSample("boom.mp3")
    bgm = minim.loadFile("funky.mp3")
    over = minim.loadSample("over.mp3")
    bgm.loop()
    noLoop()
    # os.system("pause")
    
def draw():
    global ball_lst
    global l_x,l_y
    global count
    global score, weapon, hp, dead,start
    if not start:
        return
    background(0)
    textSize(30)
    textAlign(CENTER)
    text("Score:{}".format(score),930,50)
    text("Weapon:{}".format(weapon),890,950)
    text("Health Point:{}".format(hp),120,950)
    for i in bgl:
        stroke(255)
        strokeWeight(1)
        point(i[0],i[1])
    # for i in range(100):
    #     fill(255)
    #     ellipse(randrange(1000),randrange(1000),1,1)
    fill(255)
    ellipse(500,965,50,50)
    fill(0)
    strokeWeight(5)
    stroke(255)
    l_x = 500 + cos(radians((-deg))) * 65
    l_y = 965 + sin(radians(-deg)) * 65
    c = 0
    l = line(500, 965, l_x, l_y);
    for j in brick_lst:
        j.update()
        if j.y > 1000:
            brick_lst.remove(j)
            hp -= 1
    for i in ball_lst:
        i.update()
        for j in brick_lst:
            if dist(j.x,j.y,i.x,i.y) <= 25:
                ball_lst.remove(i)
                brick_lst.remove(j)
                score += 1
                hit.trigger()
                weapon += 2
                continue
        if i.x<0 or i.x >1000 or i.y<0 or i.y>1000:
             ball_lst.remove(i)
    if int(time.ctime()[17:19]) % 3  != 0:
        count = 0
    if int(time.ctime()[17:19]) % 3  == 0 and count == 0:
        b = Bricks()
        brick_lst.append(b)
        if int(time.ctime()[17:19]) % 3  == 0:
            count = 1
    if (weapon <= 0 and len(ball_lst)<=0) or hp<=0:
        dead = True
        textSize(80)
        fill(255,0,0)
        text("You Died",500,500)
        over.trigger()
        noLoop()
        rectMode(CENTER)
        fill(255,0,0)
        rect(500,600,250,80)
        rect(500,740,250,80)
        textSize(30)
        fill(255)
        text("Restart",500,610)
        text("Exit",500,750)
        bgm.close()

def keyPressed():
    global deg
    global l_x,l_y
    global weapon
    if start:
        if (keyCode == LEFT):
            deg += 5
        if (keyCode == RIGHT):
            deg -= 5
        if (key == " ") and weapon > 0:
            b = Balls(l_x,l_y,5*cos(radians(180-deg)),5*sin(radians(180-deg)))
            ball_lst.append(b)
            weapon -=1
            shoot.trigger()
def mousePressed():
    global dead, deg, score, weapon, hp, bgm,start
    if  dead:
        if (250<=mouseX<=750 and 560<=mouseY<=640):
            dead = False
            deg = 90   
            score = 0  
            weapon = 10
            hp = 5
            setup()
            loop() 
        if (250<=mouseX<=750 and 700<=mouseY<=780):
            exit()
    if not start:
        if (250<=mouseX<=750 and 560<=mouseY<=640):
            start = True
            loop()  
        if (250<=mouseX<=750 and 680<=mouseY<=740):
            exit()

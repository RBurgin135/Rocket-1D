#Rocket that lands itself
global g
g = 1
import pygame
from pygame import FULLSCREEN
import random
pygame.font.init()
import math
import Neural_Networking as Networking
import time

#window setup
import ctypes
user32 = ctypes.windll.user32
global scr_width
global scr_height
scr_width = user32.GetSystemMetrics(0)
scr_height = user32.GetSystemMetrics(1)
window = pygame.display.set_mode((scr_width,scr_height),FULLSCREEN)
pygame.display.set_caption("Rocket 3.0")


#======
class Rocket:
    def __init__(self, Alt, Overide):
        #Rocket values
        self.fuel = 100
        self.Alt = Alt
        self.thrust = 0


        #pygame content
        self.On = pygame.image.load("Rocket on.png")
        self.Off = pygame.image.load("Rocket off.png")
        self.Broken = pygame.image.load("Rocket no-fuel.png")
        self.image = self.Off
        self.X = (scr_width/2)
        self.Y = G.Y - self.Alt - self.image.get_height()/2
        self.blitX = self.X - self.image.get_width()/2
        self.blitY = self.Y - self.image.get_height()/2
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.crash = False
        self.active = False
        self.SUCCESS = False
        

        #mass values
        self.R_m = 10
        self.F_m = self.fuel * 0.03
        self.Total_m = self.R_m + self.F_m

        #SUVAT values
        self.u = 0
        self.a = 0
        self.s = 0

        if Overide == False:
            self.Nn = Networking.NeuralNet()

    def Active(self):
        if self.fuel > 0:
            self.thrust = -25
            self.fuel -=1
            self.image = self.On
            self.active = True
        else:
            self.image = self.Broken
           
    def Calculate(self):
        #find updated mass
        self.F_m = self.fuel * 0.02
        self.Total_m = self.R_m + self.F_m

        #find resultant force in axis (F=ma)       
        Resultant_F = (g*self.Total_m) + self.thrust

        self.a = 0
        if Resultant_F != 0:
            self.a =  Resultant_F / self.Total_m

        #find displacement on axis (s = ut- 1/2 at^2)
        self.s = self.u - 0.5*self.a

        #crash and success query
        if (self.Alt - self.s) <=0:
            if (self.crash == False) and (self.u > 10):
                self.crash = True
            if self.crash == False and (self.blitX > P.X and (self.blitX+self.width) < (P.X+P.width)):
                self.SUCCESS = True
            
            self.s = 0
            self.u = 0
            self.deg = 0

        self.blitY += self.s
        self.Alt -= self.s

        #show rocket
        window.blit(self.image,(self.blitX , self.blitY))

    def Reset(self):
        #find velocity used in next Calculate (v = u + at)
        self.u = self.u + self.a

        #reset values
        self.thrust = 0
        self.image = self.Off
    

        
#======
class Ground:
    def __init__(self):
        self.X = -5000
        self.Y = scr_height- 50
        self.rect_width = 10000 
        self.rect_height = 50

        self.details = self.X, self.Y, self.rect_width, self.rect_height
        self.rect = pygame.Rect(self.details)
        
    def Show(self):
        self.details = self.X, self.Y, self.rect_width, self.rect_height
        self.rect = pygame.draw.rect(window,(211,211,211),self.details)
        
#======
class Pad:
    def __init__(self):
        self.X = scr_width/2-100
        self.Y = G.Y
        self.width = 200
        self.height = 25
        self.details = self.X, self.Y, self.width, self.height
        self.colour = (255,195,77)
        self.text = "<LANDING>"
    
    def Show(self):        
        self.Y = G.Y
        
        self.details = self.X, self.Y, self.width, self.height
        self.rect = pygame.draw.rect(window,self.colour,self.details)

        SubFont = pygame.font.SysFont('', 25)
        Text = SubFont.render(self.text, False, (255,255,255))
        window.blit(Text,(self.X+60,self.Y+2))

def Input(Pop):
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            pass
    if keys[pygame.K_SPACE]:
        for i in range(0,len(Pop)):
            Pop[i].Active()
        
def Background():
    Star = pygame.image.load("Star.png")
    window.fill((0,0,0))
    for x in range(0,50):
        for y in range(0,100):
            if y % 2 == 0:
                window.blit(Star,(G.X+200+200* x, G.Y-50-200*y))
            else:
                window.blit(Star,(G.X+350+200* x, G.Y-50-200*y))

def AI(Pop):
    for i in range(0,len(Pop)):
        result = Pop[i].Nn.Forward(Pop[i].Alt, Pop[i].u, Pop[i].a, Pop[i].fuel)
        if result > 0.5:
            Pop[i].Active()

def Diagnostics(Pop):
    Y = scr_height-40
    for i in range(0,len(Pop)):
        #state indicator
        X = 10+40*i
        details = X, Y, 20, 20
        if Pop[i].image == Pop[i].On:
            pygame.draw.rect(window,(237,28,36),details)
        elif Pop[i].image == Pop[i].Off:
            pygame.draw.rect(window,(153,217,234),details)
        else:
            pygame.draw.rect(window,(255,127,39),details)
         
        #fuel gauge
        if Pop[i].fuel > 0:
            details = (X, Y+21, Pop[i].fuel/4, 5)
            pygame.draw.rect(window,(255,127,39),details)
def GenNo(Num):
    SubFont = pygame.font.SysFont('', 100)
    Text = SubFont.render("GEN "+str(Num), False, (255,255,255))
    window.blit(Text,(0,0))

def GenerationMngmnt(Pop, GenNumber):
    GenTest = True
    for i in range(0, len(Pop)):
        if Pop[i].crash == False and Pop[i].SUCCESS == False:
            GenTest = False
    if GenTest == True:
        time.sleep(0.5)
        GenNumber += 1
        
        NewNets = Networking.Review(Pop)

        #new gen
        StartAltitude = random.randint(2500,5000)
        for i in range(0,len(NewNets)):
            Pop[i].Nn = NewNets[i]
            Pop[i].__init__(StartAltitude, True)

        NewRockets = []
        for i in range(0, len(Pop) - len(NewNets)):
            NewRockets.append(Rocket(StartAltitude, False))
            Pop.pop(len(NewNets))
    return GenNumber



G = Ground()
P = Pad()
Pop = []
StartAltitude = random.randint(2500,5000)
for i in range(0,20):
    Pop.append(Rocket(StartAltitude, False))
GenNumber = 1

RUN = True
while RUN:
    pygame.time.delay(10)
    Input(Pop)
    AI(Pop)         

    Background()

    for i in range(0,len(Pop)):
        Pop[i].Calculate()

    GenNo(GenNumber)
    G.Show()
    P.Show()
    Diagnostics(Pop)

    pygame.display.update()
    for i in range(0, len(Pop)):
        Pop[i].Reset()
    
    #generation managment
    GenNumber = GenerationMngmnt(Pop, GenNumber)
pygame.quit()

        

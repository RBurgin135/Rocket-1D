#Rocket that lands itself
global g
g = 1
global PopSize
PopSize = 200
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

#Objects====
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
        self.explode = pygame.image.load("Rocket explode.png")
        self.rubble = pygame.image.load("Rocket rubble.png")
        self.delay = 0
        self.image = self.Off
        self.X = (scr_width/2)
        self.Y = G.Y - self.Alt - self.image.get_height()/2
        self.blitX = self.X - self.image.get_width()/2
        self.blitY = self.Y - self.image.get_height()/2
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        

        #testing values
        self.crash = False
        self.SUCCESS = False
        self.tested = False
        self.testU = 0

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
        if (self.Alt - self.s) <= 0:
            if (self.crash == False) and (self.u > 25):
                self.crash = True
                self.tested = True
                self.testU = self.u
                self.image = self.explode
            if self.crash == False and (self.blitX > P.X and (self.blitX+self.width) < (P.X+P.width)):
                self.SUCCESS = True
                self.tested = True
                self.testU = self.u
            
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
        if self.image == self.explode:
            self.delay += 1
            if self.delay == 10:
                self.image = self.rubble
        elif self.image == self.rubble:
            pass
        else:
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

#Functions====
def Input(Pop):
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            pass
    if keys[pygame.K_SPACE]:
        for i in range(0,len(Pop)):
            Pop[i].Active()
        
def Background(Num):
    #Stars
    Star = pygame.image.load("Star.png")
    window.fill((0,0,0))
    for x in range(0,50):
        for y in range(0,100):
            if y % 2 == 0:
                window.blit(Star,(G.X+200+200* x, G.Y-50-200*y))
            else:
                window.blit(Star,(G.X+350+200* x, G.Y-50-200*y))
    
    #Gen number
    SubFont = pygame.font.SysFont('', 100)
    Text = SubFont.render("GEN "+str(Num), False, (255,255,255))
    window.blit(Text,(0,0))

def AI(Pop):
    for i in range(0,len(Pop)):
        if Pop[i].tested == False:
            Inputs = [Pop[i].Alt, Pop[i].a,  Pop[i].u, Pop[i].fuel]
            result = Pop[i].Nn.Forward(Inputs)
            if result[0] > 0.4:
                Pop[i].Active()

def Diagnostics(Pop):
    Y = scr_height-40
    for i in range(0,len(Pop)):
        X = 10+40*i
        details = X, Y, 20, 20
        if Pop[i].tested == False: 
            #state indicator
            if Pop[i].image == Pop[i].On:
                pygame.draw.rect(window,(237,28,36),details)
            elif Pop[i].image == Pop[i].Off:
                pygame.draw.rect(window,(153,217,234),details)
            else:
                pygame.draw.rect(window,(255,127,39),details)
            
            #fuel gauge
            #if Pop[i].fuel > 0:
            #    details = (X, Y+21, Pop[i].fuel/4, 5)
            #    pygame.draw.rect(window,(255,127,39),details)

            #Altimeter
            #details = (X-6, Y+20-Pop[i].Alt/15, 5, Pop[i].Alt/15)
            #pygame.draw.rect(window,(255,255,127),details)
        else:
            if Pop[i].SUCCESS == True:
                pygame.draw.rect(window,(76,166,76),details)
            else:
                pygame.draw.rect(window,(166,166,166),details)

def GenerationMngmnt(Pop, GenNumber):
    GenTest = True
    for i in range(0, PopSize):
        if Pop[i].tested == False:
            GenTest = False

    if GenTest == True:
        #Prep for next Gen
        time.sleep(0.5)
        GenNumber += 1
        
        NewNets = Networking.Review(Pop)

        #new gen reset rockets
        StartAltitude = random.randint(2500,5000)
        for i in range(0,len(NewNets)):
            Pop[i].Nn = NewNets[i]
            Pop[i].__init__(StartAltitude, True)

    return GenNumber, Pop

def NNDiag(Pop):
    Net = Pop[0].Nn
    ICenters = []
    HCenters = []
    OCenters = []

    #draws circles
    for x in range(0, 3):
        for y in range(0, len(Net.Layers[x])):
            pygame.draw.circle(window, (166,166,166), (1200+200*x,50+y*70), 30, 0)
            if x == 0:
                ICenters.append((1200+200*x,50+y*70))
            elif x == 1:
                HCenters.append((1200+200*x,50+y*70))
            elif x == 2:
                OCenters.append((1200+200*x,50+y*70))

    #draws lines
    CombinedCenters = [ICenters,HCenters,OCenters]
    for L in range(0,len(CombinedCenters)-1):
        for O in range(0, len(CombinedCenters[L])):
            for D in range(0, len(CombinedCenters[L+1])):
                if Net.Layers[L+1][D].weight[O] > 0:
                    colour = (173,216,230)
                else:
                    colour = (128,0,0)
                width = int(round(abs(Net.Layers[L+1][D].weight[O])*5))
                if width == 0:
                    width = 1
                pygame.draw.line(window, colour, CombinedCenters[L][O], CombinedCenters[L+1][D], width)

def Control(Pop, GenNumber):
    #end button
    details = scr_width-50, 0, 50, 50
    pygame.draw.rect(window,(255,0,0),details)
    #load button
    details = scr_width-100, 0, 50, 50
    pygame.draw.rect(window,(0,0,255),details)
    #save button
    details = scr_width-150, 0, 50, 50
    pygame.draw.rect(window,(0,255,0),details)

    RUN = True
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            Mx, My = pygame.mouse.get_pos()
            if Mx > scr_width-50 and Mx < scr_width and My < 50:
                RUN = False
            if Mx > scr_width-100 and Mx < scr_width-50 and My < 50:
                Pop, GenNumber = Networking.Read(Pop)
            if Mx > scr_width-150 and Mx < scr_width-100 and My < 50:
                Networking.Write(GenNumber, Pop)
    return RUN, Pop, GenNumber


G = Ground()
P = Pad()
Pop = []
StartAltitude = random.randint(2500,5000)
for i in range(0,PopSize):
    Pop.append(Rocket(StartAltitude, False))
GenNumber = 1

RUN = True
while RUN:
    pygame.time.delay(1)
    Input(Pop)
    AI(Pop)         

    Background(GenNumber)

    for i in range(0,PopSize):
        Pop[i].Calculate()

    G.Show()
    P.Show()
    Diagnostics(Pop)
    #NNDiag(Pop)
    RUN, Pop, GenNumber = Control(Pop, GenNumber)

    pygame.display.update()
    for i in range(0, PopSize):
        Pop[i].Reset()
    
    #generation managment
    GenNumber, Pop = GenerationMngmnt(Pop, GenNumber)

pygame.quit()

        

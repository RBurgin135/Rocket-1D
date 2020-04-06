#Rocket that lands itself
global g
g = 1
import pygame
from pygame import FULLSCREEN
import random
pygame.font.init()
import math
import Neural_Networking as Networking

#window setup
import ctypes
user32 = ctypes.windll.user32
global scr_width
global scr_height
scr_width = user32.GetSystemMetrics(0)
scr_height = user32.GetSystemMetrics(1)
window = pygame.display.set_mode((scr_width,scr_height),FULLSCREEN)
pygame.display.set_caption("Rocket 2.0")


#======
class Rocket:
    def __init__(self):
        #pygame content
        self.On = pygame.image.load("Rocket on.png")
        self.Off = pygame.image.load("Rocket off.png")
        self.Broken = pygame.image.load("Rocket no-fuel.png")
        self.image = self.Off
        self.X = (scr_width/2)
        self.Y = (scr_height/2)
        self.blitX = self.X - self.image.get_width()/2
        self.blitY = self.Y - self.image.get_height()/2
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.crash = False
        self.SUCCESS = False

        self.fuel = 200
        self.Alt = random.randint(2500,5000)
        self.thrust = 0

        #mass values
        self.R_m = 10
        self.F_m = self.fuel * 0.03
        self.Total_m = self.R_m + self.F_m

        #SUVAT values
        self.u = 0
        self.a = g
        self.s = 0

    def Active(self):
        if R.fuel > 0:
            self.thrust = -25
            R.fuel -=1
            R.image = R.On
        else:
            R.image = R.Broken
           
    def Calculate(self):
        #find updated mass
        self.F_m = self.fuel * 0.02
        self.Total_m = self.R_m + self.F_m

        #find resultant force in axis (F=ma)       
        Resultant_F = (g*self.Total_m) + self.thrust

        self.a = 0
        if Resultant_F != 0:
            self.a =  Resultant_F / R.Total_m

        #find displacement on axis (s = ut- 1/2 at^2)
        self.s = self.u - 0.5*self.a

        #crash and success query
        if (self.Alt - self.s) <=0:
            if (self.crash == False) and (self.u > 10):
                if self.SUCCESS == False :
                    P.text = "__FAILURE__"
                    P.colour = (200,0,0)
                self.crash = True
            if self.crash == False and (self.blitX > P.X and (self.blitX+self.width) < (P.X+P.width)):
                self.SUCCESS = True
                P.text = "!!SUCCESS!!"
                P.colour = (0,200,0)
            
            self.s = 0
            self.u = 0
            self.deg = 0

        G.Y -= self.s
        self.Alt -= self.s

    def Reset(self):
        #find velocity used in next Calculate (v = u + at)
        self.u = self.u + self.a

        #reset values
        self.thrust = 0
        self.image = self.Off
        
    def Show(self):
        #show all values
        SubFont = pygame.font.SysFont('', 40)
        values = ["Fuel: "+str(self.fuel), "Thrust: "+str(self.thrust), "Mass: "+str(self.Total_m), "Altitude: "+str(self.Alt), "Crash: "+ str(self.crash), "Vel: "+str(R.u), "Acc : "+str(R.a), "Success: "+str(R.SUCCESS), "Resultant: "+str((g*self.Total_m) + self.thrust)]
        for i in range (0,len(values)):
            Value_text = SubFont.render(values[i], False, (255,255,255))
            window.blit(Value_text,(scr_width-500,100+(35*i)))

        #show rocket
        window.blit(self.image,(self.blitX , self.blitY))
    
        
#======
class Ground:
    def __init__(self):
        self.X = R.X-5000
        self.Y = R.Y + R.height/2 + R.Alt
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
        self.X = R.X -R.width*3
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

def Input():
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            pass
    if keys[pygame.K_SPACE]:
        R.Active()
        
def Background():
    Star = pygame.image.load("Star.png")
    window.fill((0,0,0))
    for x in range(0,50):
        for y in range(0,100):
            if y % 2 == 0:
                window.blit(Star,(G.X+200* x, G.Y-50-200*y))
            else:
                window.blit(Star,(G.X+150+200* x, G.Y-50-200*y))

def AI():
    result = Nn.Forward(R.Alt, R.u, R.a, R.fuel)
    if result > 0.5:
        E.Active()

#Nn = Networking.NeuralNet()

R = Rocket()
G = Ground()
P = Pad()

RUN = True
while RUN:
    pygame.time.delay(10)
    Input()
    #AI()         

    Background()

    R.Calculate()
    
    R.Show()
    G.Show()
    P.Show()

    pygame.display.update()
    R.Reset()
pygame.quit()

        

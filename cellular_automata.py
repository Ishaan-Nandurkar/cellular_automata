import pygame
import sys
import random
from math import sqrt
import math 
from numpy import sign
import numpy as np
# Grid dimensions (width and height in number of cells)
WIDTH = 1000
HEIGHT = 1000
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set the title of the window
pygame.display.set_caption('Cellular Automata')
clock = pygame.time.Clock()
# redions = []
# greenions = []
# blueions = []
particles= [] 
def dist(pos1,pos2):
    x1,y1 = pos1
    x2,y2 = pos2
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)

def s_sqrt(value):
    return math.copysign((abs(value)**(1/2)), value)

class Particle:
    def __init__(self,x,y,colour,screen,mass,charge):
        self.pos = np.array([x,y],dtype=float)
        self.vel = np.array([0,0],dtype=float)
        self.accel = np.array([0,0],dtype=float)
        self.colour = colour
        self.size = 5
        self.phase = 1+1j
        self.phase_vec = np.array([0,0],dtype=float)
        self.mass = mass
        self.charge = charge
        
    def draw(self):
        pygame.draw.rect(screen,self.colour,(self.pos[0],self.pos[1],self.size,self.size))
    def update(self):
        #get phase vector
        self.phase*= 0.1j
        
        self.phase_vec = np.array([self.phase.real,self.phase.imag],dtype=float)
        

        for elem in particles:
            if elem is not self:
                vec = (elem.pos - self.pos)
                dist = np.linalg.norm(vec)
                direction = vec/dist
                force = (100*self.mass*elem.mass*direction)/((dist)**2)
                force = np.clip(force,-0.05,0.05)
            
                #self.accel += -np.dot(force,self.phase_vec) * force *100
                self.accel+=(force/self.mass)*-self.charge*elem.charge

        self.vel += self.accel

        self.pos += self.vel


        self.accel = np.array([0,0],dtype=float)


for i in range(5):
     particles.append(Particle(60*i,60*i,RED,screen,1,1))

particles.append(Particle(700,700,RED,screen,1,1))

#blueions.append(Blueion(200,200,screen))

particles.append(Particle(600,400,GREEN,screen,100,-1))

particles.append(Particle(400,400,BLUE,screen,1,10))
# particles.append(Particle(400,600,GREEN,screen,100))
# particles.append(Particle(400,400,GREEN,screen,100))
# particles.append(Particle(400,200,GREEN,screen,100))
# particles.append(Particle(200,400,GREEN,screen,100))

# Main loops
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    clock.tick(FPS)

    # Clear the screen
    screen.fill(BLACK)

    for elem in particles:
            elem.update()
            elem.draw()


    

    # Update the display
    pygame.display.flip()
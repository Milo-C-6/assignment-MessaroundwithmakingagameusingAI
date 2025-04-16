'''
old main.py before i decided to remake it so it actually\ goes along with the assignment better,
I suppose its just here for if I need to get anything or something
'''

import pygame as pg
import sys 
import numpy
from data.bomb import Bomb

# Initialize Pygame  
pg.init()  
  
# Constants  
WIDTH, HEIGHT = 600, 800  
FPS = 60  
  
# Colors  
WHITE = (255, 255, 255)  
BLACK = (0, 0, 0)  

bombs = [Bomb()]

# Setup the screen  
screen = pg.display.set_mode((WIDTH, HEIGHT))  
pg.display.set_caption('My Pygame Template')  
  
# Clock for controlling FPS  
clock = pg.time.Clock()


def render():
    screen.fill(WHITE)
    pg.draw.rect(screen,(92, 64, 51),(275,650,50,50)) #sling shot, rn

    for bomb in bombs:
        pg.draw.circle(screen,(0,0,0),bomb.pos,13)
    

# Game loop  
running = True  
while running:  
    for event in pg.event.get():  
        if event.type == pg.QUIT:  
            running = False  

        if event.type == pg.MOUSEBUTTONDOWN:
            if pg.mouse.get_pressed()[2]:
                print(pg.mouse.get_pos())
            
        if pg.mouse.get_pressed()[0] and pg.mouse.get_pos()[1]>=650 and pg.mouse.get_pos()[0] > 100 and pg.mouse.get_pos()[0] < 500:
            bombs[-1].pos = pg.mouse.get_pos()

        if event.type == pg.MOUSEBUTTONUP and (300,650) == (300,650):
            bombs[-1].velocity = numpy.divide(numpy.subtract((300,650), pg.mouse.get_pos()),(3,8))

    render()

    for bomb in bombs:
        bomb.update()
    # Update the display  
    pg.display.flip()  
  
    # Cap the frame rate  
    clock.tick(FPS)  
  
pg.quit()  
sys.exit()  

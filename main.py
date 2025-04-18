'''
Milo Cummings
stupid pygame game inspired by mario 64 ds minigames and silly gifs me and my buddies send to eachother
'''

import pygame  
import sys  
import random
import numpy
from data.resourceType import ResourceType
from data.bullet import Bullet

# setup Pygame stuff
pygame.init()  
width, height = 750, 800 
screen = pygame.display.set_mode((width, height))  
pygame.display.set_caption('car defenders')
clock = pygame.time.Clock()

# Define colors  
BLACK = (0, 0, 0)  
WHITE = (255, 255, 255)  

# Load assets
resources = {}
assetDirs = ("bullet.png","enemy.png","life.png","rip.png","explosion.png")
for i,key in enumerate(ResourceType):
    # so far only images need to be loaded, but later i'll need to add support for audio and that stuff
    resources[key] = pygame.image.load("data/images/"+assetDirs[i]).convert_alpha()

# Enemy settings  
enemy_width, enemy_height = 64, 42  
enemy_speed = 0.5
enemies = [(width/2,-enemy_height,0)] # [(100 + i * 60, 50, 0) for i in range(1)]  
  
# Other stuff
bullets = [Bullet()]  
  
# Game loop  
running = True  
while running:
    clock.tick(60)
    
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            running = False  
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[2]:
                print(pygame.mouse.get_pos())
            
        if pygame.mouse.get_pressed()[0] and pygame.mouse.get_pos()[1]>=500:
            bullets[-1].rect.center = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONUP:
            bullets[-1].velocity = numpy.divide(numpy.subtract((375,564), pygame.mouse.get_pos()),(8,8))
            bullets.append(Bullet())
    # Update bullets  
    for bullet in bullets:
        bullet.update()
        bullet.texture = pygame.transform.rotate(resources[ResourceType.IMAGE_BULLET], bullet.rotation)
        bullet.rect = bullet.texture.get_rect(center = bullet.rect.center) 
    bullets = [bullet for bullet in bullets if bullet.rect.bottom > 0 or bullet.rect.x > width or bullet.rect.x < 0]  #ohhh mah goodness its that simple???? I remember needing to do this before and having some complicated method that used only one for loop. I suppose mine might've been a bit more optimised though since it used one for loop, idk!!!!
  
    # Enemy logic

    #Add Enemies
    if random.randint(0,100)==0:
        enemies.append((random.randint(50,700), -enemy_height, 0))

    #Move Enemies, and check if they're colliding with a life or a bullet
    bulletRects = tuple(bullet.rect for bullet in bullets)
    for idx, (ex, ey, ed) in enumerate(enemies): # oooh enumerate, i've never seen this before, pretty cool! 
        ey += enemy_speed
        if ed == 0:
            if random.randint(0,70) == 0: # Chance of swaying
                ed = random.randint(45,120)
                if random.randint(0,1) == 0: # Left or right
                    ed *= -1
        else:
            if ed > 0:
                ed -= 1
                if ed <= 120:
                    ex += 1
                else: # whenever a brick gets hit by a racket, the ed value goes super high, so this checks if its super high, and then decides to do the fling
                    ex += 25
                    ey -= 25
            else:
                ed += 1
                if ed >= -120:
                    ex -= 1
                else:
                    ex -= 25
                    ey -= 25

        if ex < 0:
            ex += 1
        elif ex > width-enemy_width:
            ex -= 1
        collideId = pygame.Rect(ex,ey,enemy_width,enemy_height).collidelist(bulletRects)
        if collideId != -1:
            if tuple(bullets[collideId].velocity) != (0,0): #I'm not completely sure why but if I don't include the tuple() thing it gives me some cryptic value error
                if bullets[collideId].velocity[0]>=0:
                    enemies[idx] = (ex, ey, 800)
                else:
                    enemies[idx] = (ex, ey, -800)
                continue
        if ey > height-95 and ex:
            for i in range(4):
                if ex > 75+156.25*i and ex < 170+156.25*i and playerLives[i][0]==1:
                    ey = height+500 # will delete the brick
                    playerLives[i] = (0,playerLives[i][1],playerLives[i][2],playerLives[i][3],playerLives[i][4]) #this sucks
                    continue
        enemies[idx] = (ex, ey, ed)
    #Clear enemies not in frame
    enemies = [enemy for enemy in enemies if enemy[1]<height+enemy_height]

    # Drawing  
    screen.fill(BLACK)  
    pygame.draw.rect(screen,WHITE,pygame.Rect(300,500,30,30))
    # draw the lives
    for i,(status,frame,goAFrameForward,expldFrame,goAFrameForward2) in enumerate(playerLives):
        if status == 1:
            img = resources[ResourceType.IMAGE_LIFE]
        else:
            img = resources[ResourceType.IMAGE_RIP]
            if expldFrame < 16 and goAFrameForward2:
                expldFrame += 1
                goAFrameForward2=False
            else:
                goAFrameForward2=True
            if frame==48:
                playerLives[i] = (status, 0, False, expldFrame,goAFrameForward2)
            elif goAFrameForward:
                playerLives[i] = (status, frame+1, False, expldFrame,goAFrameForward2)
            else:
                playerLives[i] = (status, frame, True, expldFrame,goAFrameForward2)
        screen.blit(img, pygame.Rect(75+156.25*i,702,96,95),pygame.Rect(100*frame,0,100,100))
        if expldFrame < 16 and expldFrame != -1: #it pains me to have the same if statement twice
            screen.blit(resources[ResourceType.IMAGE_EXPLOSION], pygame.Rect(75+156.25*i,702,96,95),pygame.Rect(80*expldFrame,0,80,113))
    #draw other boring stuff
    for ex, ey, ed in enemies:  
        screen.blit(resources[ResourceType.IMAGE_ENEMY], (ex, ey))
    for bullet in bullets:
        screen.blit(bullet.texture, bullet.rect)
    if bullets[-1].rect.y >= 450:
        pygame.draw.line(screen,WHITE,(347,500),(bullets[-1].rect.centerx,bullets[-1].rect.bottom))
        pygame.draw.line(screen,WHITE,(403,500),(bullets[-1].rect.centerx,bullets[-1].rect.bottom))
    pygame.display.flip()  
  
# Quit Pygame  
pygame.quit()  
sys.exit()  

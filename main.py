'''
Milo Cummings
stupid pygame game inspired by mario 64 ds minigames and silly gifs me and my buddies send to eachother
'''

import pygame  
import sys  
import random
from data.resourceType import ResourceType

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

# Player settings  
player_width, player_height = 50, 30  
player_x, player_y = width // 2, height - 60  
player_speed = 5  
playerLives = [(1,0,False,-1,False) for i in range(4)]

# Enemy settings  
enemy_width, enemy_height = 40, 30  
enemy_speed = 0.5
enemies = [(width/2,-enemy_height,0)] # [(100 + i * 60, 50, 0) for i in range(1)]  
  
# Bullet settings  
bullet_width, bullet_height = 56,128
bullet_speed = 3
bullets = []  
  
# Game loop  
running = True  
while running:
    clock.tick(60)
    
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            running = False  
        if event.type == pygame.KEYDOWN:  
            if event.key == pygame.K_SPACE:  
                bullets.append([pygame.Rect(player_x + player_width // 2, player_y, bullet_width, bullet_height), 0, resources[ResourceType.IMAGE_BULLET]])  
  
    # Move bullets  
    for bullet in bullets:
        bullet[0].y -= bullet_speed
        bullet[1] += 1
        bullet[2] = pygame.transform.rotate(resources[ResourceType.IMAGE_BULLET], bullet[1])
        bullet[0] = bullet[2].get_rect(center = bullet[0].center) 
    bullets = [bullet for bullet in bullets if bullet[1] > 0]  #ohhh mah goodness its that simple???? I remember needing to do this before and having some complicated method that used only one for loop. I suppose mine might've been a bit more optimised though since it used one for loop, idk!!!!
  
    # Enemy logic

    #Add Enemies
    if random.randint(0,100)==0:
        enemies.append((random.randint(50,700), -enemy_height, 0))

    #Move Enemies, and check if they're colliding with a life
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
                ex += 1
            else:
                ed += 1
                ex -= 1

        if ex < 0:
            ex += 1
        elif ex > width-enemy_width:
            ex -= 1

        if ey > height-95 and ex:
            for i in range(4):
                if ex > 75+156.25*i and ex < 170+156.25*i and playerLives[i][0]==1:
                    ey = height+500 # will delete the brick
                    playerLives[i] = (0,playerLives[i][1],playerLives[i][2],playerLives[i][3],playerLives[i][4]) #this sucks
                    break
        enemies[idx] = (ex, ey, ed)
    #Clear enemies not in frame
    enemies = [enemy for enemy in enemies if enemy[1]<height+enemy_height]

    # Drawing  
    screen.fill(BLACK)  
    pygame.draw.rect(screen, WHITE, (player_x, player_y, player_width, player_height))
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
    for ex, ey, ed in enemies:  
        screen.blit(resources[ResourceType.IMAGE_ENEMY], (ex, ey))
    for bullet in bullets:
        screen.blit(bullet[2], bullet[0])
    pygame.display.flip()  
  
# Quit Pygame  
pygame.quit()  
sys.exit()  

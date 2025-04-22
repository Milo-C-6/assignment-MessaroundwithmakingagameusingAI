'''
Milo Cummings
stupid pygame game inspired by mario 64 ds minigames and silly gifs me and my buddies send to eachother
'''
# TODO: Add more art stuff, maybe a main menu screen too, thatd be sick. also some audio, I dislike how silent it is
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
assetDirs = ("bullet.png","enemy.png","life.png","rip.png","explosion.png","slingshot.png","logo.png","explode.mp3","hit.mp3")
for i,key in enumerate(ResourceType):
    if str(key)[13:18]=="IMAGE":
        resources[key] = pygame.image.load("data/images/"+assetDirs[i]).convert_alpha()
    else: #only other resource is a sound
        resources[key] = pygame.mixer.Sound("data/sounds/"+assetDirs[i])

# Enemy settings  
enemyWidth, enemyHeight = 64, 42  
enemySpeed = 1
enemies = [(width/2,-enemyHeight,0)] # [(100 + i * 60, 50, 0) for i in range(1)]  
  
# Score stuff
coolText = pygame.font.SysFont('Arial', 30)
score = 0
hitMarkers = [] #((posX,posY),amount,lifetime)

# Main menu
inMainMenu = True 
mainMenuFrame = 0
frameTick = 0

# Other stuff
playerLives = [(1,0,False,-1,False) for i in range(4)]
livesPos = (75, 231.25, 387.5, 543.75)
bullets = [Bullet()]  
bulletOffsetPos = (0,0)

# it felt a little wrong putting the main menu with the rest of the game loop so here it is here.
#honestly if I were to rewrite this, I'd probably have a lot of this code here seperated into classes in dif .py files
def mainMenu():
    # Update
    global frameTick # I'd use pygame.time.get_ticks() instead but its like weird. I can't really explain it, just try it yourself, replace frameTick with pygame.time.get_ticks() and you'll see.
    global mainMenuFrame # oh main if only I had made this in a class, I wouldn't have to make these stupid global stuff
    frameTick += 1
    if frameTick%3==0:
        mainMenuFrame+=1
        if mainMenuFrame==8:
            mainMenuFrame=0
    #Draw
    screen.fill(BLACK)
    screen.blit(resources[ResourceType.IMAGE_LOGO],(33,200),pygame.Rect(0,77*mainMenuFrame,684,77))
    command = coolText.render("CLICK TO START",True,WHITE)
    if frameTick%4!=0:
        screen.blit(command,command.get_rect(center=(width/2,600)))
    pygame.display.flip()


# Game loop  
running = True  
while running:
    clock.tick(60)
    
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            running = False  
        if event.type == pygame.MOUSEBUTTONDOWN:
            if inMainMenu:
                pygame.mixer.Sound.play(resources[ResourceType.SOUND_EXPLODE])
                inMainMenu = False
            if pygame.mouse.get_pressed()[0]:
                bulletOffsetPos = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[2]:
                print(pygame.mouse.get_pos())
        if len(bullets) > 0:
            newCenter = numpy.subtract((375,564),numpy.subtract(bulletOffsetPos,pygame.mouse.get_pos()))
            if pygame.mouse.get_pressed()[0] and newCenter[1]>=500 and newCenter[0]>=40 and newCenter[0]<=width-40 and tuple(bullets[-1].velocity) == (0,0):
                bullets[-1].rect.center = newCenter

            if event.type == pygame.MOUSEBUTTONUP and tuple(bullets[-1].velocity) == (0,0):
                bullets[-1].velocity = numpy.divide(numpy.subtract((375,564), bullets[-1].rect.center),(8,8))
    if inMainMenu:
        mainMenu()
        continue

    if 1 not in tuple(life[0] for life in playerLives):
        endText = coolText.render(f"Game end",False,WHITE)
        endScore = coolText.render(f"Score: {score}",False,WHITE)
        screen.blit(endText,endText.get_rect(center=(width/2,height/2)))
        screen.blit(endScore,endScore.get_rect(center=(width/2,height/2+80)))
        pygame.display.update()
        continue

    # Update bullets
    if len(bullets) == 0 or (tuple(bullets[-1].velocity) != (0,0) and bullets[-1].rect.y < 433):
        bullets.append(Bullet())
    offsetI = 0  
    for i,bullet in enumerate(bullets):
        bullet.update()
        if tuple(bullet.velocity) != (0,0):
            bullet.rotation += 30
        bullet.texture = pygame.transform.rotate(resources[ResourceType.IMAGE_BULLET], bullet.rotation)
        bullet.rect = bullet.texture.get_rect(center = bullet.rect.center) 
        if bullet.rect.bottom < 0 or bullet.rect.x > width or bullet.rect.x < 0 or bullet.rect.y > height:
            score += bullet.multiplier*100
            bullets.pop(i+offsetI)
            offsetI -= 1  
    # Enemy logic

    #Add Enemies
    enemySpeed = min(9,1+score/1000)
    if random.randint(0,max(10,int(120-score/40)))==0:
        enemies.append((random.randint(50,700), -enemyHeight, 0))

    #Move Enemies, and check if they're colliding with a life or a bullet
    bulletRects = tuple(bullet.rect for bullet in bullets)
    for idx, (ex, ey, ed) in enumerate(enemies): # oooh enumerate, i've never seen this before, pretty cool! 
        ey += enemySpeed
        if ed == 0:
            if ey < 500:
                if random.randint(0,70) == 0: # Chance of swaying
                    ed = random.randint(45,120)
                    if random.randint(0,1) == 0: # Left or right
                        ed *= -1
            else: # if its lower than 500 itll seek on specifc lives lives
                distances = tuple(abs(pos-ex) for pos in livesPos)
                id = distances.index(min(distances))
                if ex > livesPos[id]:
                    ed = -1
                else:
                    ed = 1

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
        elif ex > width-enemyWidth:
            ex -= 1
        collideId = pygame.Rect(ex,ey,enemyWidth,enemyHeight).collidelist(bulletRects)
        if collideId != -1:
            if tuple(bullets[collideId].velocity) != (0,0): #I'm not completely sure why but if I don't include the tuple() thing it gives me some cryptic value error
                if not abs(ed) > 120:
                    bullets[collideId].multiplier += 1
                    hitMarkers.append(((ex,ey),100*bullets[collideId].multiplier,30)) #((posX,posY),amount,lifetime)
                    pygame.mixer.Sound.play(resources[ResourceType.SOUND_HIT])
                if bullets[collideId].velocity[0]>=0: #racket collideing
                    enemies[idx] = (ex, ey, 800)
                    bullets[collideId].velocity = [-15,bullets[collideId].velocity[1]] 
                else:
                    enemies[idx] = (ex, ey, -800)
                    bullets[collideId].velocity = [15,bullets[collideId].velocity[1]] 
                continue
        if ey > height-95 and ex:
            for i in range(4):
                if ex > 75+156.25*i and ex < 170+156.25*i and playerLives[i][0]==1:
                    pygame.mixer.Sound.play(resources[ResourceType.SOUND_EXPLODE])
                    ey = height+500 # will delete the brick
                    playerLives[i] = (0,playerLives[i][1],playerLives[i][2],playerLives[i][3],playerLives[i][4]) #this sucks
                    continue
        enemies[idx] = (ex, ey, ed)
    #Clear enemies not in frame
    enemies = [enemy for enemy in enemies if enemy[1]<height+enemyHeight] #ohhh mah goodness its that simple???? I remember needing to do this before and having some complicated method that used only one for loop. I suppose mine might've been a bit more optimised though since it used one for loop, idk!!!!
    # Hit marker logic
    for i,marker in enumerate(hitMarkers):
        hitMarkers[i] = ((marker[0][0],marker[0][1]-1),marker[1],marker[2]-1)
    hitMarkers = [marker for marker in hitMarkers if marker[2] > 0]
    # Drawing  
    screen.fill(BLACK)  
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
    screen.blit(resources[ResourceType.IMAGE_SLINGSHOT], (345,490))
    for ex, ey, ed in enemies:  
        screen.blit(resources[ResourceType.IMAGE_ENEMY], (ex, ey))
    for bullet in bullets:
        screen.blit(bullet.texture, bullet.rect)
    if len(bullets) > 0 and bullets[-1].rect.y >= 435:
        pygame.draw.line(screen,WHITE,(347,500),(bullets[-1].rect.centerx,bullets[-1].rect.bottom))
        pygame.draw.line(screen,WHITE,(403,500),(bullets[-1].rect.centerx,bullets[-1].rect.bottom))
    #draw score
    for marker in hitMarkers:
        screen.blit(coolText.render(str(marker[1]),True,WHITE),marker[0])
    screen.blit(coolText.render(f"Score: {score}",True,WHITE),(0,0))
    pygame.display.flip()  
    
# Quit Pygame  
pygame.quit()  
sys.exit()  

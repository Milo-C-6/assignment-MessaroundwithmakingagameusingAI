import pygame
import numpy

class Bullet:
    def __init__(self):
        #pygame.Rect(player_x + player_width // 2, player_y, bullet_width, bullet_height)
        self.rect = pygame.Rect(347,500,56,128)
        self.velocity = (0,0)
        self.rotation = 0
        self.texture = pygame.Surface((0,0))
        self.multiplier = 0

    def update(self):
        self.rect.move_ip(self.velocity)
        if tuple(self.velocity) != (0,0): self.velocity = numpy.add(self.velocity, (0,0.2)) # maybe I should add documentation because I have no clue what I wrote here
        # ohhh this is the code to make it slowly fall, lets fix that
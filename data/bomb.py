import pygame as pg
import numpy

class Bomb:
    def __init__(self):
        self.pos = (300,650)
        self.velocity = (0,0)

    def update(self):
        self.pos = numpy.add(self.pos,self.velocity)
        if self.velocity[1] != 0: self.velocity = numpy.add(self.velocity, (0,0.2))
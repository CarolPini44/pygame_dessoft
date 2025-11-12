import pygame
import os 
import sys

GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

PISTA_X = {
    'verde': 100,
    'vermelha': 200,
    'amarela': 300,
    'azul': 400,
}

class NotaCaindo(pygame.sprite.Sprite):
    def __init__(self, img, pos_x, timing):

        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = -60 - (150 * (timing/1000))
        self.speedy = 5
        self.speedx = 0

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > 715:
            self.kill()

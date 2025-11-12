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

class NotaJulgamento(pygame.sprite.Sprite):
    def __init__(self, img, pos_x):

        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = 550
        self.speedy = 0
        self.speedx = 0

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx

class FeedbackVisual(pygame.sprite.Sprite):
    def _init_(self, image, x, y, duration_ms=200):
        pygame.sprite.Sprite._init_(self)
        
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = x + 60 
        self.rect.bottom = y 
        
        self.duration_ms = duration_ms
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        elapsed_time = pygame.time.get_ticks() - self.spawn_time        
        if elapsed_time > self.duration_ms:
            self.kill()        
        self.rect.y -= 3
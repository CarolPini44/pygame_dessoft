import os
import pygame
import sys
import random

INICIO = 1
MENU = 2
GAME = 3
FINALIZAR = 4
FEXO = 5

def inicial(tela):
    clock = pygame.time.Clock()

    #funcao que carrega imagens
    cache_imagens = {}
    def carrega_imagens(imagem):
        if imagem not in cache_imagens:
            try:
                caminho = os.path.join(os.path.dirname(__file__), imagem)
                cache_imagens[imagem] = pygame.image.load(caminho).convert_alpha()
            except pygame.error:
                print('erro ao tentar ler imagem: {0}' .format(imagem))
                sys.exit()
        return cache_imagens[imagem]

    caminho_imagem = os.path.join('imagens', "tela_inicial2.png")
    fundo = pygame.image.load(caminho_imagem)
    fundo2 = pygame.transform.scale(fundo, (600,700))

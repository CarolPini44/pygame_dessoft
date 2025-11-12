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

    #funcao carrega sons
    cache_sons = {}
    def carrega_sons(som):
        if som not in cache_sons:
            try:
                caminho = os.path.join(os.path.dirname(__file__), som)
                cache_sons[som] = pygame.mixer.Sound(caminho)
            except:
                print('erro ao tentar ler arquivo de som: {0}' .format(som))
                sys.exit()
        return cache_sons[som]

    arquivo = os.path.join('sons', 'My_Chemical_Romance_Helena_8-Bit.mp3')
    caminho = os.path.join(os.path.dirname(__file__), arquivo)
    pygame.mixer.music.load(caminho)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.8)    

    som_acao = carrega_sons(arquivo)

    game = True

    #loop principal
    while game:

        clock.tick(60)
        eventos = pygame.event.get()

        for evento in eventos:
            if evento.type == pygame.QUIT or evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
                pygame.mixer.stop()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    pygame.mixer.music.stop()
                    som_acao.play()
            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_SPACE:
                    som_acao.stop()
                    modulo = MENU
                    game = False           

        tela.fill((0,0,0))
        tela.blit(fundo2, (0,0))
        pygame.display.update()

    return modulo

import pygame 
import os 
import sys
import time
from assets import NotaCaindo, NotaJulgamento

INICIO = 1
MENU = 2
GAME = 3
FINALIZAR = 4
FEXO = 5

WIDTH = 600
HEIGHT = 700
FPS = 30
TEMPO_PREPARACAO_MS = 5000 
TEMPO_QUEDA_MS = 2067

PISTA_X = {
    'azul': 100,
    'vermelho': 200,
    'verde': 300,
    'amarelo': 400
}

PISTA_KEYS = {
    pygame.K_a: 'azul',
    pygame.K_s: 'vermelho',
    pygame.K_k: 'verde',
    pygame.K_l: 'amarelo'
}


def jogo(window):
    
    clock = pygame.time.Clock()
    
    pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Hero Rock Fox - Jogo")


    assets = {}
    ret_width, ret_height = 120, 100
    CENTRO_PISTA_OFFSET = ret_width // 2
    
    caminho_fonte = os.path.join('assets','04B_30__.ttf')
    assets["fonte1"] = pygame.font.Font(caminho_fonte, 24)
    assets["fonte2"] = pygame.font.Font(caminho_fonte, 16)

    
    try:
        assets["sAzul"] = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'sprite_botaoazul.png')).convert_alpha(), (ret_width, ret_height))
        assets["sVerm"] = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'sprite_botaovermelho.png')).convert_alpha(), (ret_width, ret_height))
        assets["sVerd"] = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'sprite_botaoverde.png')).convert_alpha(), (ret_width, ret_height))
        assets["sAMAR"] = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'sprite_botaoamarelo.png')).convert_alpha(), (ret_width, ret_height))
        assets["sBran"] = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'sprite_botaobranco.png')).convert_alpha(), (ret_width, ret_height))
        assets["fundo2"] = pygame.transform.scale(pygame.image.load(os.path.join('imagens', "menu_selecao.png")).convert(), (WIDTH, HEIGHT))
    except Exception as e:
        print(f"Erro ao carregar imagens/fundo: {e}")
        return (FEXO, 0)

    try:
        caminho_musica = os.path.join('sons', 'Decode _8Bit.mp3')
        pygame.mixer.music.load(caminho_musica)
        pygame.mixer.music.set_volume(0.7)
        music_duration_ms = int(pygame.mixer.Sound(caminho_musica).get_length() * 1000)
    except Exception as e:
        print(f"Erro ao carregar música: {e}")
        music_duration_ms = 60000

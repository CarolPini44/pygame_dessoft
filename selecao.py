import os
import pygame
import sys
from start import inicial # Assume que 'start.py' contém a função 'inicial'

# === CONSTANTES DE ESTADO (IMPORTADAS DO MAIN) ===
INICIO = 1
MENU = 2
GAME = 3
FINALIZAR = 4
FEXO = 5

# --- Funções de Cache (Carregamento de Assets) ---

cache_imagens = {}
def carrega_imagens(imagem):
    if imagem not in cache_imagens:
        try:
            # Caminho corrigido para usar o diretório atual do script
            caminho = os.path.join(os.path.dirname(os.path.abspath(__file__)), imagem)
            cache_imagens[imagem] = pygame.image.load(caminho).convert_alpha()
        except pygame.error:
            print('Erro ao tentar ler imagem: {0}' .format(imagem))
            sys.exit()
    return cache_imagens[imagem]

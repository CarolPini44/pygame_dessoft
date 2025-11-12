import os
import pygame
import sys
import random
from start import inicial
from selecao import menu_de_selecao
from jogo_decode import jogo
from jogo_idontloveyou import jogo2
from jogo_blackparade import jogo3
from final import final

INICIO = 1
MENU = 2
GAME = 3
FINALIZAR = 4
FEXO = 5
ESTADO = INICIO
musica_selecionada = None

GAME_FUNCTIONS = {
    "Decode": jogo,
    'IDontLoveYou': jogo2,
    'BlackParade': jogo3,
}

# Defina a variável global para o score (necessário para a tela FINALIZAR)
final_score = 0 

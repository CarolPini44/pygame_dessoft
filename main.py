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

def main():
    global ESTADO, musica_selecionada, final_score
    pygame.init()
    if not pygame.mixer.get_init():
          pygame.mixer.init() 

    surf = pygame.display.set_mode((600,700))
    pygame.display.set_caption("Hero Rock Fox")
   
    #Loop Principal
    while ESTADO != FEXO:
        
        if ESTADO == INICIO:
            try:
                ESTADO = inicial(surf)
            except Exception as e:
                print(f"Erro tela inicial: {e}")
                ESTADO = FEXO
        elif ESTADO == MENU:
            try:
                ESTADO, musica_selecionada = menu_de_selecao(surf)
            except Exception as e:
                print(f'Erro menu de seleção: {e}')
                ESTADO = FEXO
        elif ESTADO == GAME:
            if musica_selecionada not in GAME_FUNCTIONS:
                print(f"ERRO: Nenhuma função de partida mapeada para: {musica_selecionada}")
                ESTADO = MENU
                continue
            
            game_function = GAME_FUNCTIONS[musica_selecionada]
            estado_saida = MENU
            score_obtido = 0
            try:
                estado_saida, score_obtido = game_function(surf)
            except Exception as e:
                print(f'Erro no jogo: {e}')
                estado_saida = FEXO
            final_score = score_obtido
            ESTADO = estado_saida
        elif ESTADO == FINALIZAR:
            try:
                ESTADO = final(surf, final_score)
            except Exception as e: 
                print(f'Erro na tela final: {e}')
                ESTADO = FEXO
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()

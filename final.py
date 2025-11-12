import pygame
import os

INICIO = 1
MENU = 2
GAME = 3
FINALIZAR = 4
FEXO = 5

def final(window, SCORE):

    clock = pygame.time.Clock()
    FPS = 30
    WIDTH = 600
    CENTRO_X = WIDTH // 2

    pygame.display.set_caption('Hero Rock Fox')

    caminho_fonte = os.path.join('assets','04B_30__.ttf')
    fonte = pygame.font.Font(caminho_fonte, 24)
    fonte2 = pygame.font.Font(caminho_fonte, 36)

    score_num = fonte2.render('{0}!!'.format(SCORE), True, (255, 255, 0))
    score_text = fonte.render('Sua pontuacao final:', True, (255, 255, 0))

    end_text = fonte.render('espaco para sair', True, (255, 255, 0))
    esc_text = fonte.render('esc para menu', True, (255, 255, 0))

    caminho_imagem = os.path.join('imagens', "tela_final.png")
    fundo = pygame.image.load(caminho_imagem).convert_alpha()
    fundo2 = pygame.transform.scale(fundo, (600,700))

    rodando = True

    while rodando:

        clock.tick(FPS)

        eventos = pygame.event.get()

        for evento in eventos:
            if evento. type == pygame.QUIT:
                estado = FEXO
                rodando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    estado = FEXO
                    rodando = False
                if evento.key == pygame.K_ESCAPE:
                    estado = INICIO
                    rodando = False

        window.fill((0, 0, 0))
        window.blit(fundo2, (0 , 0))
        # 1. Título do Score
        pos_x_score_text = CENTRO_X - (score_text.get_width() // 2)
        window.blit(score_text, (pos_x_score_text, 150))

        # 2. Número do Score
        pos_x_score_num = CENTRO_X - (score_num.get_width() // 2)
        window.blit(score_num, (pos_x_score_num, 200))
        
        # 3. Instrução ESC
        pos_x_esc_text = CENTRO_X - (esc_text.get_width() // 2)
        window.blit(esc_text, (pos_x_esc_text, 600))
        
        # 4. Instrução SPACE
        pos_x_end_text = CENTRO_X - (end_text.get_width() // 2)
        window.blit(end_text, (pos_x_end_text, 650))

        pygame.display.update()

    return estado

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

cache_sons = {}
def carrega_sons(som):
    if som not in cache_sons:
        try:
            caminho = os.path.join(os.path.dirname(os.path.abspath(__file__)), som)
            cache_sons[som] = pygame.mixer.Sound(caminho)
        except:
            print('Erro ao tentar ler arquivo de som: {0}' .format(som))
            sys.exit()
    return cache_sons[som]

def menu_de_selecao(tela):
    clock = pygame.time.Clock()

    opcoes_musica = [
        {"nome": "Decode - Paramore", 
         "nome_do_jogo": "Decode",
         "caminho": os.path.join('sons', 'Decode _8Bit.mp3'),
         "preview": None},
        {"nome": "Welcome to the Black Parade - MCR", 
         "nome_do_jogo": "BlackParade",
         "caminho": os.path.join('sons', 'My_Chemical_Romance_-_Welcome_to_the_Black_Parade_8-bit.mp3'),
         "preview": None},
        {"nome": "I Dont Love You - MCR", 
         "nome_do_jogo": "IDontLoveYou",
         "caminho": os.path.join('sons', 'I_Dont_Love_You.mp3'),
         "preview": None},
    ]

    for opcao in opcoes_musica:
        opcao['preview'] = carrega_sons(opcao['caminho'])
        opcao['preview'].set_volume(0.5)

    try:
        caminho_fonte = os.path.join('assets','04B_30__.ttf')
        caminho_fonte2 = os.path.join('assets','04B_19__.ttf')
        fonte = pygame.font.Font(caminho_fonte, 18)
        fonte_menu = pygame.font.Font(caminho_fonte, 24)
        fonte2 = pygame.font.Font(caminho_fonte2, 20)
    except:
        fonte = pygame.font.Font(None, 24)
        fonte_menu = pygame.font.Font(None, 30)
        fonte2 = pygame.font.Font(None, 16)
        
    caminho_imagem = os.path.join('imagens', "menu_selecao.png")
    fundo = pygame.image.load(caminho_imagem)
    fundo2 = pygame.transform.scale(fundo, (600,700))

    indice_sel = 0
    last_preview = -1
    game = True

    if opcoes_musica[0]['preview']:
        opcoes_musica[0]['preview'].play(loops=0)
        last_preview = 0

    while game:
        clock.tick(60)
        eventos = pygame.event.get()
        largura, altura = tela.get_size()
        
        for evento in eventos:
            if evento.type == pygame.QUIT:
                pygame.mixer.stop()
                return FEXO, None
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pygame.mixer.stop()
                    return INICIO, None
                
                ind_n = indice_sel
                if evento.key == pygame.K_UP:
                    ind_n = (indice_sel - 1) % len(opcoes_musica)
                elif evento.key == pygame.K_DOWN:
                    ind_n = (indice_sel + 1) % len(opcoes_musica)

                if ind_n != indice_sel:
                    # Para o preview anterior
                    if last_preview != -1 and opcoes_musica[last_preview]['preview']:
                        opcoes_musica[last_preview]['preview'].stop()

                    indice_sel = ind_n

                    if opcoes_musica[indice_sel]['preview']:
                        opcoes_musica[indice_sel]['preview'].play(loops=0)
                        last_preview = indice_sel
                
                elif evento.key == pygame.K_SPACE:
                    if last_preview != -1 and opcoes_musica[last_preview]['preview']:
                        opcoes_musica[last_preview]['preview'].stop()

                    nome_do_jogo = opcoes_musica[indice_sel]['nome_do_jogo']
                    return GAME, nome_do_jogo 
            else:
                pass

        tela.fill((0,0,0))
        tela.blit(fundo2, (0,0))

        titulo = fonte_menu.render('Selecione a musica', True, (252,75,8))
        pygame.display.set_caption("Hero Rock Fox - Menu de seleção")

        tela.blit(titulo, (largura/2 - titulo.get_width()/2, 50))

        y_pos = 150

        for i, opcao in enumerate(opcoes_musica):
            cor = (127,127,127)

            if i == indice_sel:
                cor = (255,255,0)

            escrita = fonte.render(opcao['nome'], True, cor)
            tela.blit(escrita, (largura/2 - escrita.get_width()/2, y_pos))
            y_pos += 60

        
        instrucao_ctrl = fonte2.render('-Use SETAS (cima/baixo) para selecionar a musica', True, (252, 255,0))
        instrucao_ctrl2 = fonte2.render('-Use ESPACO para iniciar o jogo', True, (252, 255,0))
        instrucao_ctrl3 = fonte2.render('-Utilize as teclas "A" para azul,', True, (252, 255,0))
        instrucao_ctrl4 = fonte2.render('"S" para vermelho, "K" para verde', True, (252,255,0))
        instrucao_ctrl5 = fonte2.render('e "L" para amarelo', True, (255,255,0))
        instrucao_saida = fonte2.render('-ESC para voltar', True, (255, 255, 0))
        rodape_y = altura - 120

        tela.blit(instrucao_ctrl, (largura/2 - instrucao_ctrl.get_width()/2, rodape_y - 100))
        tela.blit(instrucao_ctrl2, (largura/2 - instrucao_ctrl.get_width()/2, rodape_y - 80))
        tela.blit(instrucao_ctrl3, (largura/2 - instrucao_ctrl.get_width()/2, rodape_y - 60))
        tela.blit(instrucao_ctrl4, (largura/2 - instrucao_ctrl.get_width()/2, rodape_y - 40))
        tela.blit(instrucao_ctrl5, (largura/2 - instrucao_ctrl.get_width()/2, rodape_y - 20))
        tela.blit(instrucao_saida, (largura/2 - instrucao_saida.get_width()/2, rodape_y))

        pygame.display.update()
        
    return MENU, None
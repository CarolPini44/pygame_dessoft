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


def jogo3(window):
    
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
        caminho_musica = os.path.join('sons', 'My_Chemical_Romance_-_Welcome_to_the_Black_Parade_8-bit.mp3')
        pygame.mixer.music.load(caminho_musica)
        pygame.mixer.music.set_volume(0.7)
        music_duration_ms = int(pygame.mixer.Sound(caminho_musica).get_length() * 1000)
    except Exception as e:
        print(f"Erro ao carregar música: {e}")
        music_duration_ms = 60000

    amarelo = [
    (0.408, 0.562), (1.951, 2.152), (3.599, 3.712), (4.975, 5.198), (6.233, 6.452),
    (6.993, 7.156), (8.480, 8.580), (9.925, 10.071), (12.298, 12.463), (13.719, 13.824),
    (15.083, 15.317), (16.618, 16.718), (18.011, 18.150), (19.437, 19.581), (20.317, 20.436),
    (20.880, 21.083), (22.304, 22.554), (23.727, 23.925), (25.191, 25.388), (25.438, 25.538),
    (26.692, 26.822), (28.123, 28.331), (29.496, 29.764), (33.812, 33.997), (35.261, 35.441),
    (36.697, 36.885), (38.187, 38.392), (39.656, 39.842), (41.014, 41.279), (42.462, 42.629),
    (43.995, 44.210), (45.406, 45.606), (46.888, 47.119), (48.328, 48.510), (49.765, 49.911),
    (50.646, 50.831),
]

    verde = [
    (0.927, 1.058), (1.833, 1.987), (4.677, 4.925), (6.186, 6.306), (7.637, 7.801),
    (8.990, 9.176), (10.490, 10.590), (11.893, 12.136), (14.829, 15.005), (15.053, 15.280),
    (16.255, 16.404), (17.712, 17.812), (19.146, 19.269), (20.559, 20.733), (23.433, 23.658),
    (24.880, 25.033), (29.203, 29.416), (30.583, 30.820), (32.021, 32.257), (33.234, 33.426),
    (33.519, 33.709), (34.984, 35.088), (36.423, 36.541), (37.496, 37.674), (37.808, 37.953),
    (38.981, 39.148), (39.264, 39.380), (42.170, 42.280), (43.614, 43.753), (44.985, 45.230),
    (46.489, 46.636), (47.904, 48.094), (49.356, 49.552), (50.538, 50.738), (51.012, 51.124),
    (53.988, 54.152),
]

    azul = [
    (0.062, 0.253), (1.537, 1.750), (3.045, 3.160), (4.414, 4.617), (5.924, 6.061),
    (7.285, 7.521), (8.809, 8.965), (10.178, 10.331), (13.026, 13.244), (14.552, 14.714),
    (15.940, 16.185), (17.351, 17.540), (17.922, 18.145), (18.803, 19.019), (21.749, 21.942),
    (21.992, 22.181), (23.148, 23.377), (24.637, 24.767), (25.990, 26.159), (26.286, 26.526),
    (27.439, 27.645), (27.721, 27.940), (28.852, 29.070), (30.349, 30.510), (30.992, 31.190),
    (31.818, 31.978), (34.680, 34.840), (36.070, 36.301), (40.471, 40.579), (40.677, 40.901),
    (41.873, 42.083), (43.310, 43.537), (44.714, 44.901), (46.173, 46.364), (47.647, 47.784),
    (49.087, 49.284),
]

    vermelho = [
    (0.650, 0.901), (2.167, 2.359), (3.279, 3.448), (3.538, 3.710), (5.051, 5.218),
    (6.420, 6.685), (7.926, 8.094), (9.371, 9.533), (10.761, 10.906), (11.625, 11.765),
    (12.201, 12.415), (13.311, 13.520), (13.623, 13.802), (16.596, 16.748), (19.442, 19.552),
    (20.895, 21.008), (22.293, 22.515), (23.785, 23.885), (26.661, 26.833), (28.045, 28.218),
    (29.445, 29.668), (30.916, 31.079), (32.433, 32.589), (32.639, 32.739), (33.857, 33.975),
    (35.215, 35.431), (36.649, 36.862), (38.153, 38.298), (39.560, 39.739), (41.059, 41.159),
    (42.498, 42.653), (43.906, 44.103), (45.282, 45.564), (46.755, 46.948), (48.221, 48.448),
    (49.627, 49.843), (51.159, 51.259), (52.558, 52.680), (55.428, 55.543), (56.824, 57.088),
    (58.262, 58.456), (59.900, 60.000),
]

    chart_data = {
        'amarelo': amarelo,
        'verde': verde,
        'azul': azul,
        'vermelho': vermelho
    }
    
    SCORE = 0
    mult = 1
    game = True
    
    all_sprites = pygame.sprite.Group()
    nota_sprites = pygame.sprite.Group()
    judgment_sprites = pygame.sprite.Group()
    
    key_press_time = {'azul': 0, 'vermelho': 0, 'verde': 0, 'amarelo': 0}
    hit_windows = {'azul': [], 'vermelho': [], 'verde': [], 'amarelo': []}
    
    judgment_sprites.add(NotaJulgamento(assets["sBran"], PISTA_X['azul']))
    judgment_sprites.add(NotaJulgamento(assets["sBran"], PISTA_X['vermelho']))
    judgment_sprites.add(NotaJulgamento(assets["sBran"], PISTA_X['verde']))
    judgment_sprites.add(NotaJulgamento(assets["sBran"], PISTA_X['amarelo']))
    all_sprites.add(judgment_sprites)

    asset_map = {
        'azul': assets["sAzul"], 'vermelho': assets["sVerm"], 
        'verde': assets["sVerd"], 'amarelo': assets["sAMAR"]
    }

    for color, notes in chart_data.items():
        img_asset = asset_map[color]
        x_pos = PISTA_X[color]
        
        for t_inicio, t_fim in notes:
            t_acerto_ms = int(t_inicio * 1000)
            
            y_start = t_acerto_ms - TEMPO_QUEDA_MS
            
            note = NotaCaindo(img_asset, x_pos, y_start)
            nota_sprites.add(note)
            
            hit_windows[color].append([t_acerto_ms - 200, t_acerto_ms, t_acerto_ms + 350])

    all_sprites.add(nota_sprites)


    
    timer_start = pygame.time.get_ticks()
    delay_time = (TEMPO_PREPARACAO_MS - (pygame.time.get_ticks() - timer_start)) / 1000
    if delay_time > 0:
        time.sleep(delay_time)
        
    pygame.mixer.music.play(loops=0) # Toca uma vez, não em loop (-1)

    while game:
        clock.tick(FPS)
        timer = pygame.time.get_ticks() - timer_start

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.mixer.music.stop()
                return (FEXO, SCORE)

            if evento.type == pygame.KEYDOWN:
                if evento.key in PISTA_KEYS:
                    pista_color = PISTA_KEYS[evento.key]
                    key_press_time[pista_color] = timer
                    
                    for button in judgment_sprites:
                        if PISTA_X[pista_color] == button.rect.x:
                            button.rect.y -= 10 
                            
                if evento.key == pygame.K_SPACE: 
                    pygame.mixer.music.stop()
                    return (FINALIZAR, SCORE)

            if evento.type == pygame.KEYUP:
                if evento.key in PISTA_KEYS:
                    pista_color = PISTA_KEYS[evento.key]
                    for button in judgment_sprites:
                        if PISTA_X[pista_color] == button.rect.x:
                            button.rect.y += 10

        for color, windows in hit_windows.items():
            if windows:
                window_data = windows[0] # Janela da próxima nota
                t_press = key_press_time[color]
                
                # Verifica se a nota já passou do tempo limite da janela
                if timer >= window_data[2] + 15:
                    is_hit = False
                    
                    
                    if t_press >= window_data[0] and t_press <= window_data[2]:
                        SCORE += 50 * mult # Acerto básico
                        is_hit = True
                        
                        
                        if abs(t_press - window_data[1]) < 50:
                            SCORE += 50 * mult 
                    
                    windows.pop(0)
                    if is_hit:
                        key_press_time[color] = 0

        if timer >= music_duration_ms + 5000: # 5s após o fim da música
            return (FINALIZAR, SCORE)

        all_sprites.update() 
        
        window.fill((0, 0, 0))
        window.blit(assets["fundo2"], (0, 0))

        linhas_x = list(PISTA_X.values()) 
        
        # Desenha as linhas de pista
        for x in linhas_x:
            x_centralizado = x + CENTRO_PISTA_OFFSET
            pygame.draw.line(window, (180, 180, 180), (x_centralizado, -100), (x_centralizado, 700), 5)


        
        # Desenha o Placar
        score_num = assets["fonte1"].render(f'{SCORE}', True, (252, 75, 8))
        score_text = assets["fonte2"].render('pontos:', True, (252, 75, 8))
        window.blit(score_num, (20, 100))
        window.blit(score_text, (20, 50))

        # Desenha a mensagem de saída
        if timer >= music_duration_ms - 2000 and int(timer / 1000) % 2 == 0:
            exit_text = assets["fonte2"].render('pressione espaco para ver resultado final', True, (252, 75, 8))
            window.blit(exit_text, (45, 10))

        all_sprites.draw(window)
        pygame.display.update()

    return(FINALIZAR, SCORE)

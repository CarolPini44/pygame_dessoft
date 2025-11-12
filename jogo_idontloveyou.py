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


def jogo2(window):
    
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
        caminho_musica = os.path.join('sons', 'I_Dont_Love_You.mp3')
        pygame.mixer.music.load(caminho_musica)
        pygame.mixer.music.set_volume(1)
        music_duration_ms = int(pygame.mixer.Sound(caminho_musica).get_length() * 1000)
    except Exception as e:
        print(f"Erro ao carregar música: {e}")
        music_duration_ms = 60000

    amarelo = [
    (0.380, 0.627), (3.520, 3.686), (4.947, 5.086), (6.195, 6.378),
    (6.428, 6.548), (7.069, 7.189), (9.944, 10.064), (12.197, 12.350),
    (13.723, 13.918), (15.208, 15.370), (16.631, 16.751), (18.013, 18.247),
    (19.413, 19.620), (20.599, 20.734), (20.924, 21.108), (21.731, 21.896),
    (22.366, 22.486), (23.799, 23.965), (25.184, 25.395), (26.628, 26.900),
    (27.681, 27.952), (28.126, 28.246), (29.515, 29.758), (30.625, 30.748),
    (30.918, 31.205), (35.309, 35.511), (36.700, 36.920), (39.570, 39.750),
    (41.094, 41.245), (42.535, 42.670), (44.032, 44.181), (45.530, 45.650),
    (46.899, 47.116), (48.391, 48.511), (49.732, 49.985), (51.036, 51.260),]


    verde = [
    (0.913, 1.066), (1.805, 2.017), (2.067, 2.187), (3.322, 3.455),
    (7.578, 7.751), (8.972, 9.130), (9.401, 9.521), (10.491, 10.671),
    (11.966, 12.117), (13.341, 13.465), (14.798, 15.008), (16.221, 16.358),
    (17.642, 17.793), (19.163, 19.339), (21.978, 22.106), (23.401, 23.668),
    (24.903, 25.023), (26.264, 26.489), (30.966, 31.169), (32.082, 32.303),
    (33.799, 34.098), (34.955, 35.185), (36.440, 36.596), (37.847, 38.030),
    (39.246, 39.464), (40.682, 40.936), (42.133, 42.285), (43.519, 43.693),
    (45.028, 45.212), (45.275, 45.502), (46.391, 46.669), (47.838, 48.019),
    (49.274, 49.496), (50.531, 50.651), (50.701, 50.821), (50.982, 51.129),
]

    azul = [
    (0.118, 0.305), (0.641, 0.902), (1.591, 1.794), (3.001, 3.134),
    (4.426, 4.597), (5.813, 6.072), (7.290, 7.478), (8.801, 8.921),
    (10.211, 10.390), (11.568, 11.842), (13.112, 13.232), (14.467, 14.695),
    (15.900, 16.086), (17.385, 17.622), (18.771, 19.053), (20.320, 20.440),
    (23.082, 23.273), (24.625, 24.745), (26.017, 26.207), (27.521, 27.706),
    (28.863, 29.020), (29.224, 29.427), (30.335, 30.590), (31.830, 31.950),
    (33.258, 33.442), (34.710, 34.873), (36.108, 36.247), (37.510, 37.668),
    (39.033, 39.153), (40.414, 40.557), (41.877, 42.119), (43.324, 43.444),
    (44.761, 44.989), (46.140, 46.320), (47.691, 47.811), (49.142, 49.270),
]

    vermelho = [
    (2.149, 2.294), (3.547, 3.784), (4.646, 4.934), (4.994, 5.167),
    (6.408, 6.660), (7.894, 8.140), (8.401, 8.628), (10.797, 10.969),
    (12.164, 12.405), (13.661, 13.789), (15.079, 15.220), (16.504, 16.690),
    (17.971, 18.166), (19.392, 19.668), (20.903, 21.044), (22.324, 22.488),
    (23.800, 23.920), (25.233, 25.353), (26.675, 26.834), (28.012, 28.209),
    (29.459, 29.658), (32.381, 32.525), (32.575, 32.695), (33.453, 33.684),
    (33.877, 33.997), (35.279, 35.486), (36.636, 36.857), (38.088, 38.387),
    (38.437, 38.557), (39.533, 39.752), (41.049, 41.209), (42.406, 42.702),
    (43.927, 44.047), (46.787, 46.950), (48.156, 48.381), (49.721, 49.906),
    (52.565, 52.743), (53.960, 54.168), (55.472, 55.666), (56.895, 57.100),
    (58.263, 58.433), (59.880, 60.000),
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

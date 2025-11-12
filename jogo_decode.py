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

    amarelo = [
    (0.420, 0.590), (2.010, 2.188), (3.540, 3.708), (4.980, 5.150),
    (6.220, 6.395), (7.010, 7.190), (8.430, 8.610), (9.890, 10.060),
    (12.240, 12.410), (13.700, 13.880), (15.140, 15.320), (16.580, 16.760),
    (18.020, 18.200), (19.460, 19.640), (20.900, 21.080), (22.340, 22.520),
    (23.780, 23.960), (25.220, 25.400), (26.660, 26.840), (28.100, 28.280),
    (29.540, 29.720), (30.980, 31.160), (32.420, 32.600), (33.860, 34.040),
    (35.300, 35.480), (36.740, 36.920), (38.180, 38.360), (39.620, 39.800),
    (41.060, 41.240), (42.500, 42.680), (44.020, 44.200), (45.460, 45.640),
    (46.900, 47.080), (48.340, 48.520), (49.780, 49.960), (50.600, 50.780)
    ]

    verde = [
    (0.900, 1.070), (1.840, 2.010), (3.260, 3.430), (4.700, 4.880),
    (6.160, 6.340), (7.600, 7.780), (9.020, 9.200), (10.460, 10.640),
    (11.900, 12.080), (13.340, 13.520), (14.780, 14.960), (16.220, 16.400),
    (17.660, 17.840), (19.100, 19.280), (20.540, 20.720), (21.980, 22.160),
    (23.420, 23.600), (24.860, 25.040), (26.300, 26.480), (27.740, 27.920),
    (29.180, 29.360), (30.620, 30.800), (32.060, 32.240), (33.500, 33.680),
    (34.940, 35.120), (36.380, 36.560), (37.820, 38.000), (39.260, 39.440),
    (40.700, 40.880), (42.140, 42.320), (43.580, 43.760), (45.020, 45.200),
    (46.460, 46.640), (47.900, 48.080), (49.340, 49.520), (50.980, 51.160)
    ]

    azul = [
    (0.120, 0.300), (1.560, 1.740), (2.990, 3.170), (4.430, 4.610),
    (5.870, 6.050), (7.310, 7.490), (8.750, 8.930), (10.190, 10.370),
    (11.630, 11.810), (13.070, 13.250), (14.510, 14.690), (15.950, 16.130),
    (17.390, 17.570), (18.830, 19.010), (20.270, 20.450), (21.710, 21.890),
    (23.150, 23.330), (24.590, 24.770), (26.030, 26.210), (27.470, 27.650),
    (28.910, 29.090), (30.350, 30.530), (31.790, 31.970), (33.230, 33.410),
    (34.670, 34.850), (36.110, 36.290), (37.550, 37.730), (39.000, 39.180),
    (40.440, 40.620), (41.880, 42.060), (43.320, 43.500), (44.760, 44.940),
    (46.200, 46.380), (47.640, 47.820), (49.080, 49.260), (50.520, 50.700)
    ]

    vermelho = [
    (0.700, 0.880), (2.140, 2.320), (3.580, 3.760), (5.020, 5.200),
    (6.460, 6.640), (7.900, 8.080), (9.340, 9.520), (10.780, 10.960),
    (12.220, 12.400), (13.660, 13.840), (15.100, 15.280), (16.540, 16.720),
    (17.980, 18.160), (19.420, 19.600), (20.860, 21.040), (22.300, 22.480),
    (23.740, 23.920), (25.180, 25.360), (26.620, 26.800), (28.060, 28.240),
    (29.500, 29.680), (30.940, 31.120), (32.380, 32.560), (33.820, 34.000),
    (35.260, 35.440), (36.700, 36.880), (38.140, 38.320), (39.580, 39.760),
    (41.020, 41.200), (42.460, 42.640), (43.900, 44.080), (45.340, 45.520),
    (46.780, 46.960), (48.220, 48.400), (49.660, 49.840), (51.100, 51.280),
    (52.540, 52.720), (53.980, 54.160), (55.420, 55.600), (56.860, 57.040),
    (58.300, 58.480),

    (59.820, 60.000)
    ]

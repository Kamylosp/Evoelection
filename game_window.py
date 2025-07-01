import pygame
import csv

initial_money = 15
initial_cc = 0

players = []

def draw_players_area(screen, num_players):
    largura = screen.get_width()
    altura_total = screen.get_height() // 2  # metade da tela

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (230, 230, 230)
    FONT = pygame.font.SysFont("Arial", 24)

    try:
        player_icon = pygame.image.load("player_icon.png")
        player_icon = pygame.transform.scale(player_icon, (50, 50))
    except:
        player_icon = None

    altura_bloco = altura_total // num_players

    for i in range(num_players):
        y_top = i * altura_bloco
        cor_fundo = (245, 245, 245) if i % 2 == 0 else (220, 220, 220)
        pygame.draw.rect(screen, cor_fundo, pygame.Rect(0, y_top, largura, altura_bloco))

        padding = 20
        x_icon = padding
        x_nome = x_icon + 60
        x_cc = largura // 2
        x_dinheiro = largura - 250

        if player_icon:
            screen.blit(player_icon, (x_icon, y_top + altura_bloco // 2 - 25))

        nome = f"Player {i+1}"
        texto_nome = FONT.render(nome, True, BLACK)
        screen.blit(texto_nome, (x_nome, y_top + altura_bloco // 2 - texto_nome.get_height() // 2))

        cc_texto = FONT.render(f"CC: {players[i][1]}", True, BLACK)
        screen.blit(cc_texto, (x_cc, y_top + altura_bloco // 2 - cc_texto.get_height() // 2))

        dinheiro_texto = FONT.render(f"$: {players[i][0]} millions", True, BLACK)
        screen.blit(dinheiro_texto, (x_dinheiro, y_top + altura_bloco // 2 - dinheiro_texto.get_height() // 2))


def draw_button(screen, rect, text, font, text_color, bg_color, active=False):
    border_radius = 8
    pygame.draw.rect(screen, bg_color, rect, border_radius=border_radius)
    if active:
        # Desenha borda para botão ativo
        pygame.draw.rect(screen, (255, 215, 0), rect, 4, border_radius=border_radius)  # dourado
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


def calculate_carbon_credits(matriz, round, code):

    print(round, code)

    coef = 1 - (round-1)*0.05

    return int(matriz[int(code[1:])-1][3]) * coef


def open_action_file(caminho_arquivo = "actions_file.csv"):
    matriz = []
    with open(caminho_arquivo, newline='', encoding='utf-8') as csvfile:
        leitor = csv.reader(csvfile)
        for linha in leitor:
            matriz.append(linha)
    return matriz

def open_news_file(caminho_arquivo = "news_file.csv"):
    matriz = []
    with open(caminho_arquivo, newline='', encoding='utf-8') as csvfile:
        leitor = csv.reader(csvfile)
        for linha in leitor:
            matriz.append(linha)
    return matriz


def init_players (num_players):
    for i in range(num_players):
        players.append([initial_money, initial_cc])


def show_game(screen, num_players=2):
    pygame.font.init()
    clock = pygame.time.Clock()
    running = True

    init_players(num_players)

    matrix_actions = open_action_file()
    matrix_news = open_news_file()

    FONT = pygame.font.SysFont("Arial", 24)
    FONT_SMALL = pygame.font.SysFont("Arial", 20)

    largura = screen.get_width()
    altura = screen.get_height()

    # Área de ação: metade inferior da tela
    action_area_top = altura // 2
    action_area_height = altura - action_area_top

    # Estados da UI
    player_ativo = 0
    round_num = 1
    input_acao = ""
    input_active = False

    # Botões player
    btn_players = []
    largura_btn_player = 100
    altura_btn_player = 40
    espacamento_players = 10
    total_width_players = (largura_btn_player + espacamento_players) * num_players - espacamento_players
    start_x_players = (largura - total_width_players) // 2
    y_players = action_area_top + 20

    for i in range(num_players):
        rect = pygame.Rect(start_x_players + i * (largura_btn_player + espacamento_players), y_players, largura_btn_player, altura_btn_player)
        btn_players.append(rect)

    # Botões round
    btn_round_minus = pygame.Rect(largura//2 - 120, y_players + 60, 50, 40)
    btn_round_plus = pygame.Rect(largura//2 + 70, y_players + 60, 50, 40)
    rect_round_value = pygame.Rect(largura//2 - 30, y_players + 60, 100, 40)

    btn_round_minus.centerx = largura//2 - 100
    btn_round_plus.centerx = largura//2 + 100
    rect_round_value.centerx = largura//2

    # Caixa de texto para ação
    caixa_acao = pygame.Rect(largura//2 - 150, y_players + 120, 300, 40)

    # Botão realizar ação
    btn_acao = pygame.Rect(largura//2 - 125, y_players + 180, 250, 50)

    mostrar_aviso = False  # estado do aviso
    mensagem_aviso = ""    # texto a ser exibido no aviso

    money = 1000
    cc = 10
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "sair"

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"
                elif mostrar_aviso and event.key == pygame.K_SPACE:
                    mostrar_aviso = False  # fecha o aviso

                if input_active and not mostrar_aviso:
                    if event.key == pygame.K_BACKSPACE:
                        input_acao = input_acao[:-1]
                    elif event.key == pygame.K_RETURN:
                        mensagem_aviso = f"You spent ${money} for {cc} C.C."
                        mostrar_aviso = True
                        input_acao = ""
                    else:
                        if len(input_acao) < 20 and event.unicode.isprintable():
                            input_acao += event.unicode

            elif event.type == pygame.MOUSEBUTTONDOWN and not mostrar_aviso:
                mouse_pos = event.pos

                for i, btn in enumerate(btn_players):
                    if btn.collidepoint(mouse_pos):
                        player_ativo = i

                if btn_round_minus.collidepoint(mouse_pos) and round_num > 1:
                    round_num -= 1
                elif btn_round_plus.collidepoint(mouse_pos) and round_num < 10:
                    round_num += 1

                if caixa_acao.collidepoint(mouse_pos):
                    input_active = True
                else:
                    input_active = False

                if btn_acao.collidepoint(mouse_pos):
                    try:
                        if input_acao[0] == 'a' or input_acao[0] == 'A':
                            consequence_CC = calculate_carbon_credits(matrix_actions, round_num, input_acao)

                            list = matrix_actions[int(input_acao[1:]) - 1][2].split(' ')
                            cost = int(list[0])

                            if (players[player_ativo][0] >= cost):
                                players[player_ativo][0] -= cost
                                players[player_ativo][1] += consequence_CC

                                mensagem_aviso = f"You spent ${int(cost)} millions for {consequence_CC} C.C."
                                mostrar_aviso = True
                            input_acao = ""

                        elif input_acao[0] == 'n' or input_acao[0] == 'N':

                            value = int(matrix_news[int(input_acao[1:])-1][2])
                            cc = int(matrix_news[int(input_acao[1:])-1][3])

                            players[player_ativo][0] += value
                            players[player_ativo][1] += cc

                            mensagem_aviso = f"You won ${value} millions and {cc} C.C."
                            mostrar_aviso = True
                            input_acao = ""
                    
                    except:
                        input_acao = ""

        screen.fill((255, 255, 255))
        draw_players_area(screen, num_players)

        pygame.draw.rect(screen, (240, 240, 240), (0, action_area_top, largura, action_area_height))

        for i, btn in enumerate(btn_players):
            ativo = (i == player_ativo)
            cor_fundo = (100, 150, 255) if ativo else (200, 200, 200)
            cor_texto = (255, 255, 255) if ativo else (0, 0, 0)
            draw_button(screen, btn, f"Player {i+1}", FONT_SMALL, cor_texto, cor_fundo, active=ativo)

        draw_button(screen, btn_round_minus, "-", FONT_SMALL, (0,0,0), (200,200,200))
        draw_button(screen, btn_round_plus, "+", FONT_SMALL, (0,0,0), (200,200,200))
        pygame.draw.rect(screen, (220, 220, 220), rect_round_value, border_radius=8)
        texto_round = FONT_SMALL.render(f"Round: {round_num}", True, (0,0,0))
        texto_rect = texto_round.get_rect(center=rect_round_value.center)
        screen.blit(texto_round, texto_rect)

        cor_caixa = (255, 255, 255) if input_active else (230, 230, 230)
        pygame.draw.rect(screen, cor_caixa, caixa_acao, border_radius=8)
        pygame.draw.rect(screen, (0,0,0), caixa_acao, 2, border_radius=8)
        texto_input = FONT_SMALL.render(input_acao if input_acao != "" else "Code...", True, (0,0,0))
        screen.blit(texto_input, (caixa_acao.x + 10, caixa_acao.y + 8))

        draw_button(screen, btn_acao, "Do action", FONT, (255,255,255), (0, 150, 0))

        # Se aviso estiver ativo
        if mostrar_aviso:
            aviso_rect = pygame.Rect(largura//2 - 300, altura//2 - 100, 600, 200)
            pygame.draw.rect(screen, (255, 255, 200), aviso_rect, border_radius=12)
            pygame.draw.rect(screen, (0, 0, 0), aviso_rect, 3, border_radius=12)

            texto_aviso1 = FONT.render(mensagem_aviso, True, (0, 0, 0))
            texto_aviso2 = FONT_SMALL.render("Press [ESPACE] to continuate", True, (80, 80, 80))

            screen.blit(texto_aviso1, (aviso_rect.centerx - texto_aviso1.get_width()//2, aviso_rect.y + 20))
            screen.blit(texto_aviso2, (aviso_rect.centerx - texto_aviso2.get_width()//2, aviso_rect.y + 70))

        pygame.display.flip()
        clock.tick(60)


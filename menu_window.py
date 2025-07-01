import pygame

num_min_players = 2
num_max_players = 6

def draw_button(screen, rect, texto, fonte, cor_texto, cor_fundo):
    pygame.draw.rect(screen, cor_fundo, rect, border_radius=8)
    texto_surface = fonte.render(texto, True, cor_texto)
    texto_rect = texto_surface.get_rect(center=rect.center)
    screen.blit(texto_surface, texto_rect)


def show_menu(screen):
    font_title = pygame.font.SysFont("Arial", 60, bold=True)
    font_text = pygame.font.SysFont("Arial", 28)
    font_button = pygame.font.SysFont("Arial", 24)

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (100, 150, 255)
    GREEN = (0, 180, 0)
    RED = (180, 0, 0)
    GRAY = (200, 200, 200)

    num_players = 2  # valor inicial mínimo

    # Botões
    btn_menos = pygame.Rect(250, 380, 50, 40)
    btn_mais = pygame.Rect(500, 380, 50, 40)
    btn_sair = pygame.Rect(320, 440, 160, 40)
    btn_jogar = pygame.Rect(320, 500, 160, 40)
    btn_creditos = pygame.Rect(320, 560, 160, 40)  # Novo botão

    btn_menos.centerx = screen.get_width() // 2 - 90
    btn_mais.centerx = screen.get_width() // 2 + 90
    btn_sair.centerx = screen.get_width() // 2
    btn_jogar.centerx = screen.get_width() // 2
    btn_creditos.centerx = screen.get_width() // 2  # Centraliza botão de créditos

    # Carrega imagem
    try:
        logo = pygame.image.load("icon.png")
        logo = pygame.transform.scale(logo, (120, 120))
    except:
        logo = None

    while True:
        screen.fill(WHITE)

        # Logo
        if logo:
            screen.blit(logo, (screen.get_width()//2 - logo.get_width()//2, 20))

        # Nome do jogo
        titulo = font_title.render("Evoelection", True, BLACK)
        screen.blit(titulo, (screen.get_width()//2 - titulo.get_width()//2, 160))

        # Caixa: número de jogadores
        label = font_text.render("Number of Players:", True, BLACK)
        screen.blit(label, (screen.get_width()//2 - label.get_width()//2, 260))

        caixa_valor = pygame.Rect(0, 300, 200, 50)
        caixa_valor.centerx = screen.get_width() // 2
        pygame.draw.rect(screen, GRAY, caixa_valor, border_radius=8)
        valor_txt = font_text.render(str(num_players), True, BLACK)
        screen.blit(valor_txt, (caixa_valor.centerx - valor_txt.get_width()//2, caixa_valor.centery - valor_txt.get_height()//2))

        # Botões
        draw_button(screen, btn_menos, "-", font_button, BLACK, GRAY)
        draw_button(screen, btn_mais, "+", font_button, BLACK, GRAY)
        draw_button(screen, btn_sair, "Exit", font_button, WHITE, RED)
        draw_button(screen, btn_jogar, "Start Game", font_button, WHITE, GREEN)
        draw_button(screen, btn_creditos, "Credits", font_button, WHITE, BLUE)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "sair", 0

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if btn_menos.collidepoint(event.pos) and num_players > num_min_players:
                    num_players -= 1
                elif btn_mais.collidepoint(event.pos) and num_players < num_max_players:
                    num_players += 1
                elif btn_sair.collidepoint(event.pos):
                    return "sair", 0
                elif btn_jogar.collidepoint(event.pos):
                    return "jogo", num_players
                elif btn_creditos.collidepoint(event.pos):
                    return "credits", 0  # Retorna "credits" ao clicar no botão

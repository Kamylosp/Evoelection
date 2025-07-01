import pygame
import os

def show_credits(screen):
    font = pygame.font.SysFont("Arial", 28)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Carrega imagem
    try:
        image = pygame.image.load("icon.png")
        image = pygame.transform.scale(image, (150, 150))
    except:
        image = None  # se não carregar, apenas ignora

    # Texto de créditos
    linhas_creditos = [
        "Thank you for playing!",
        "Developed by Stefan Schnell, Kamylo Porto, Paulo Schelbauer",
        "and Ricardo Marin during the SustainED",
        "Summer School 2025 - Neuburg",
        "",
        "Press ESC to return to menu."
    ]

    while True:
        screen.fill(WHITE)

        y = 100
        for linha in linhas_creditos:
            texto = font.render(linha, True, BLACK)
            screen.blit(texto, (screen.get_width()//2 - texto.get_width()//2, y))
            y += 40

        if image:
            screen.blit(image, (screen.get_width()//2 - image.get_width()//2, y + 20))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "sair"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"

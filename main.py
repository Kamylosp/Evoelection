import pygame
import sys
from menu_window import show_menu
from game_window import show_game
from credits_window import show_credits

# Inicializa o Pygame
pygame.init()
WIDTH, HEIGHT = 1366, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Evoelection")

clock = pygame.time.Clock()

STATE_MENU = "menu"
STATE_JOGO = "jogo"
STATE_CREDITS = "credits"
estado_atual = STATE_MENU

num_players = 2

running = True
while running:
    if estado_atual == STATE_MENU:
        estado_atual, num_players = show_menu(screen)
    elif estado_atual == STATE_JOGO:
        estado_atual = show_game(screen, num_players)
    elif estado_atual == STATE_CREDITS:
        estado_atual = show_credits(screen)
    elif estado_atual == "sair":
        running = False

    clock.tick(60)

pygame.quit()
sys.exit()


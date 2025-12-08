import pygame
import sys
from snake.scenes.intro import Menu
from snake.settings import Settings

pygame.init()
cfg = Settings()
screen = pygame.display.set_mode((cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game Pro")

if __name__ == "__main__":
    mn = Menu(screen)  
    mn.bg_Menu()
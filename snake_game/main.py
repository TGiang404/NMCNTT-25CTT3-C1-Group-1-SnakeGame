import pygame
import sys
from snake.core.env_snake import Play
from snake.scenes.intro import Menu
screen = pygame.display.set_mode((1000, 650))

if __name__ == "__main__":
    mn = Menu(screen)  
    while True:    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
             pygame.quit()
             sys.exit()
        mn.bg_Menu() 
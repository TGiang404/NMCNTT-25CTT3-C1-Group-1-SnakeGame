import pygame
from snake.core.env_snake import Play
pygame.init
class Button:
    def __init__(self, screen,  Name, pos,  rect, radius = 10):
        self.screen = screen
        self.Name = Name
        self.rect = pygame.Rect(rect)
        self.pos = pos
        self.radius = radius

    def draw(self):
        font = pygame.font.Font(None, 50)  
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, (0, 255, 0), self.rect, self.radius)
            text = font.render(self.Name, True, (0, 255, 0))
            text_rect = text.get_rect(centerx = self.screen.get_width() // 2)
            text_rect.y = self.pos

            self.screen.blit(text, text_rect)
        else:
            pygame.draw.rect(self.screen, (255, 255, 255), self.rect, self.radius)
            text = font.render(self.Name, True, (255, 255, 255))
            text_rect = text.get_rect(centerx = self.screen.get_width() // 2)
            text_rect.y = self.pos
            self.screen.blit(text, text_rect)

    def Click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                return True
        return False
    
class Menu:
    def __init__(self, screen):
        self.screen = screen

    def bg_Menu(self):
        bg_menu = pygame.image.load("assets/images/menu_bg.png")
        bg_menu = pygame.transform.scale(bg_menu, (1000, 650))
        self.screen.blit(bg_menu, (0, 0))
        Human_Mode = Button(self.screen, "Human Mode", 150, (350, 130, 300, 73))
        AI_Mode = Button(self.screen, "AI Mode", 230, (350, 210, 300, 73))
        Option = Button(self.screen, "Option", 310, (350, 290, 300, 73))
        Exit =  Button(self.screen, "Exit", 390, (350, 370, 300, 73))
        Human_Mode.draw()
        AI_Mode.draw()
        Option.draw()
        Exit.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if Human_Mode.Click(event) == True:
                game = Play(self.screen)
                game.Play_Game()
        pygame.display.flip()

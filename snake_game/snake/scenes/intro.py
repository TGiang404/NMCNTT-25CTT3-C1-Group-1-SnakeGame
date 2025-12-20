import pygame
import sys
from snake.core.env_snake import Play
from snake.settings import Settings


pygame.init()

class Button:
    def __init__(self, screen, Name, pos_y, rect_args, radius=10):
        self.screen = screen
        self.Name = Name
        self.rect = pygame.Rect(rect_args) 
        self.pos_y = pos_y
        self.radius = radius
        self.cfg = Settings()

    def draw(self):
        font = pygame.font.Font(None, 45) 
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, self.cfg.TEXT_COLOR, self.rect, border_radius=self.radius)
            text_color = (0, 0, 0)
        else:
            pygame.draw.rect(self.screen, self.cfg.TEXT_COLOR, self.rect, width=3, border_radius=self.radius)
            text_color = self.cfg.TEXT_COLOR

        text = font.render(self.Name, True, text_color)
        text_rect = text.get_rect(center=self.rect.center)
        self.screen.blit(text, text_rect)

    def Click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    return True
        return False

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.cfg = Settings()
        self.center_x = self.cfg.SCREEN_WIDTH // 2
    def ai_menu_run(self):
        running = True
        btn_w = 400
        btn_h = 60
        btn_x = self.center_x - (btn_w // 2)
        gap = 80
        start_y = 250
        from snake.rl.train_dqn import train
        while running:
            self.screen.fill((15, 15, 30)) 
            font_title = pygame.font.SysFont("Consolas", 60, bold=True)
            title = font_title.render("AI MODE SELECTION", True, self.cfg.TEXT_COLOR)
            title_rect = title.get_rect(center=(self.center_x, 100))
            self.screen.blit(title, title_rect)
            btn_Train = Button(self.screen, "Train New Model", 0, (btn_x, start_y, btn_w, btn_h))
            btn_Watch = Button(self.screen, "Watch Best AI", 0, (btn_x, start_y + gap, btn_w, btn_h))
            btn_Back  = Button(self.screen, "Back", 0, (btn_x, start_y + gap * 2, btn_w, btn_h))
            btn_Train.draw()
            btn_Watch.draw()
            btn_Back.draw()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if btn_Train.Click(event):
                    train(training_mode=True)
                if btn_Watch.Click(event):
                    train(training_mode=False)
                if btn_Back.Click(event):
                    running = False 
                    pygame.event.clear()
    def options_run(self):
        running = True
        btn_w = 400
        btn_h = 60
        btn_x = self.center_x - (btn_w // 2)
        
        gap = 80
        start_y = 150

        while running:
            self.screen.fill((10, 10, 10)) 
            font_title = pygame.font.SysFont("Consolas", 60, bold=True)
            title = font_title.render("SETTINGS", True, self.cfg.TEXT_COLOR)
            title_rect = title.get_rect(center=(self.center_x, 70))
            self.screen.blit(title, title_rect)

            txt_diff = f"Speed: {self.cfg.DIFFICULTY_NAME}"
            btn_Diff = Button(self.screen, txt_diff, 0, (btn_x, start_y, btn_w, btn_h))

            curr_snake = self.cfg.SNAKE_THEMES[self.cfg.snake_idx]["name"]
            txt_snake = f"Snake Color: {curr_snake}"
            btn_Snake = Button(self.screen, txt_snake, 0, (btn_x, start_y + gap, btn_w, btn_h))

            curr_bg = self.cfg.BG_THEMES[self.cfg.bg_idx]["name"]
            txt_bg = f"BG Color: {curr_bg}"
            btn_Bg = Button(self.screen, txt_bg, 0, (btn_x, start_y + gap*2, btn_w, btn_h))

            curr_food = self.cfg.FOOD_THEMES[self.cfg.food_idx]["name"]
            txt_food = f"Food Color: {curr_food}"
            btn_Food = Button(self.screen, txt_food, 0, (btn_x, start_y + gap*3, btn_w, btn_h))
            btn_Back = Button(self.screen, "Back to Menu", 0, (btn_x, start_y + gap*4 + 40, btn_w, btn_h))
            
            btn_Diff.draw()
            btn_Snake.draw()
            btn_Bg.draw()
            btn_Food.draw()
            btn_Back.draw()

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                
                if btn_Diff.Click(event):
                    if self.cfg.DIFFICULTY_NAME == "Normal":
                        self.cfg.FPS = 25; self.cfg.DIFFICULTY_NAME = "Hard"
                    elif self.cfg.DIFFICULTY_NAME == "Hard":
                        self.cfg.FPS = 5; self.cfg.DIFFICULTY_NAME = "Easy"
                    else:
                        self.cfg.FPS = 10; self.cfg.DIFFICULTY_NAME = "Normal"

                if btn_Snake.Click(event):
                    self.cfg.next_snake_color()
                if btn_Bg.Click(event):
                    self.cfg.next_bg_color()
                if btn_Food.Click(event):
                    self.cfg.next_food_color()
                
                if btn_Back.Click(event):
                    running = False 
                    pygame.event.clear() 

    def bg_Menu(self):
        try:
            bg_img = pygame.image.load("assets/images/menu_bg.png")
            bg_img = pygame.transform.scale(bg_img, (self.cfg.SCREEN_WIDTH, self.cfg.SCREEN_HEIGHT))
        except:
            bg_img = None
        btn_w = 300
        btn_h = 70
        btn_x = self.center_x - (btn_w // 2)

        while True:
            if bg_img: self.screen.blit(bg_img, (0, 0))
            else: self.screen.fill((0,0,0))
            
            font_title = pygame.font.SysFont("Consolas", 80, bold=True)
            title_surface = font_title.render("SNAKE GAME", True, self.cfg.TEXT_COLOR)
            title_rect = title_surface.get_rect(center=(self.center_x, 100))
            self.screen.blit(title_surface, title_rect)
            btn_Human = Button(self.screen, "Start Game", 0, (btn_x, 250, btn_w, btn_h))
            btn_AI = Button(self.screen, "AI Auto", 0, (btn_x, 350, btn_w, btn_h))
            btn_Option = Button(self.screen, "Settings", 0, (btn_x, 450, btn_w, btn_h))
            btn_Exit = Button(self.screen, "Exit", 0, (btn_x, 550, btn_w, btn_h))
            
            btn_Human.draw()
            btn_AI.draw()
            btn_Option.draw()
            btn_Exit.draw()

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                
                if btn_Human.Click(event):
                    game = Play(self.screen)
                    game.Play_Game()
                    pygame.mouse.set_pos((self.cfg.SCREEN_WIDTH, self.cfg.SCREEN_HEIGHT))
                    pygame.event.clear()
                
                if btn_AI.Click(event):
                    self.ai_menu_run()
                if btn_Option.Click(event):
                    self.options_run()
                if btn_Exit.Click(event):
                    pygame.quit(); sys.exit()
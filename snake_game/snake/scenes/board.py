import pygame
import sys
from snake.settings import Settings 

pygame.init()

class Graphic:
    def __init__(self, screen, Vec, xi, yi):
        self.screen = screen
        self.xi = xi
        self.yi = yi
        self.Vec = Vec
        self.cfg = Settings() 

    def display_Item(self):
        x = self.xi * self.cfg.GRID_SIZE + self.cfg.GRID_SIZE // 2
        y = self.yi * self.cfg.GRID_SIZE + self.cfg.GRID_SIZE // 2
        pygame.draw.circle(self.screen, self.cfg.FOOD_COLOR, (x, y), self.cfg.GRID_SIZE // 2 - 5)

    def display_Table(self):
        self.screen.fill(self.cfg.BG_COLOR)
        # Vẽ lưới
        for x in range(0, self.cfg.SCREEN_WIDTH, self.cfg.GRID_SIZE):
            pygame.draw.line(self.screen, self.cfg.GRID_COLOR, (x, 0), (x, self.cfg.SCREEN_HEIGHT))
        for y in range(0, self.cfg.SCREEN_HEIGHT, self.cfg.GRID_SIZE):
            pygame.draw.line(self.screen, self.cfg.GRID_COLOR, (0, y), (self.cfg.SCREEN_WIDTH, y))
        start_x = self.cfg.GRID_SIZE
        start_y = self.cfg.GRID_SIZE
        width = (self.cfg.GRID_WIDTH - 2) * self.cfg.GRID_SIZE
        height = (self.cfg.GRID_HEIGHT - 2) * self.cfg.GRID_SIZE
        
        border_rect = pygame.Rect(start_x, start_y, width, height) 
        pygame.draw.rect(self.screen, self.cfg.BORDER_COLOR, border_rect, 5)

    def display_Snake(self):
        for i, pos in enumerate(self.Vec):
            x = pos[0] * self.cfg.GRID_SIZE
            y = pos[1] * self.cfg.GRID_SIZE
            
            center_x = x + self.cfg.GRID_SIZE // 2
            center_y = y + self.cfg.GRID_SIZE // 2
            radius = self.cfg.GRID_SIZE // 2 - 2

            if i == 0:
                pygame.draw.circle(self.screen, self.cfg.SNAKE_HEAD_COLOR, (center_x, center_y), radius)
                # Vẽ mắt rắn
                pygame.draw.circle(self.screen, (0,0,0), (center_x - 8, center_y - 8), 4)
                pygame.draw.circle(self.screen, (0,0,0), (center_x + 8, center_y - 8), 4)
            else:
                pygame.draw.circle(self.screen, self.cfg.SNAKE_BODY_COLOR, (center_x, center_y), radius)

    def display_Score(self):
        font = pygame.font.SysFont("Consolas", 30, bold=True)
        score_value = len(self.Vec) - 3
        score_surf = font.render(f"Score: {score_value}", True, self.cfg.TEXT_COLOR)
        self.screen.blit(score_surf, (5, 5))

    def display_EndGame(self):
        font_title = pygame.font.SysFont("Consolas", 60, bold=True)
        font_msg = pygame.font.SysFont("Consolas", 30, bold=True) 
        font_score = pygame.font.SysFont("Consolas", 30, bold=True)
        width = self.cfg.SCREEN_WIDTH
        height = self.cfg.SCREEN_HEIGHT
        
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200)) 
        self.screen.blit(overlay, (0, 0))

        title_surf = font_title.render("GAME OVER", True, (255, 80, 80))
        title_rect = title_surf.get_rect(center=(width // 2, height // 2 - 50))

        score_surf = font_score.render(f"YOUR SCORE: {len(self.Vec) - 3}", True, (255, 255, 102))
        score_rect = score_surf.get_rect(center=(width // 2 - 15, height // 2 + 10))

        msg_surf = font_msg.render("Press ESC to return to menu", True, self.cfg.TEXT_COLOR)
        msg_rect = msg_surf.get_rect(center=(width // 2, height // 2 + 60))

        self.screen.blit(title_surf, title_rect)
        self.screen.blit(score_surf, score_rect)
        self.screen.blit(msg_surf, msg_rect)
        pygame.display.flip()

    def display_Game(self):
        self.display_Table() 
        self.display_Item()  
        self.display_Snake()
        self.display_Score()
        pygame.display.flip()




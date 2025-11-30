import pygame
import sys

pygame.init()

pygame.display.set_caption("Snake")

class Graphic:
    def __init__(self, screen, Vec, xi, yi ):
        self.screen = screen
        self.xi = xi
        self.yi = yi
        self.Vec = Vec

    def display_Item(self):
        pygame.draw.circle(self.screen, (255, 200, 0), (self.xi * 50 + 25, self.yi * 50 + 25), 10)


    def display_Table(self):
            bg = pygame.image.load("assets/images/background.png")
            bg = pygame.transform.scale(bg, (1000, 650))
            self.screen.blit(bg, (0, 0))
            for i in range(1, 20):
                pygame.draw.line(self.screen, (0,0,0), (50 * i, 50), (50 * i, 600))
            for i in range(1, 13):
                pygame.draw.line(self.screen, (0,0,0), (50, 50 * i), (950, 50 * i))
                
    def display_Snake(self):
            for i in range(len(self.Vec)):
                x = 50 * self.Vec[i][0]
                y = 50 * self.Vec[i][1]
                RED = (255,0,0)
                GREEN = (0, 250, 154)
                if i == 0:
                    pygame.draw.circle(self.screen, RED, (x + 25, y + 25), 20)
                else:
                    pygame.draw.circle(self.screen, GREEN, (x + 25, y + 25), 20)

    def display_EndGame(self):
        font_title = pygame.font.SysFont("Consolas", 60, bold=True)
        #font_msg = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 20)
        font_msg = pygame.font.SysFont("Consolas", 60, bold=True)
        width = 1000
        height = 650
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        # Tiêu đề
        title_surf = font_title.render("GAME OVER", True, (255, 80, 80))
        title_rect = title_surf.get_rect(center=(width // 2,
                                                height // 2 - 40))

        # Nội dung
        msg_surf = font_msg.render("Press ESC to return to menu", True, (255, 255, 255))
        msg_rect = msg_surf.get_rect(center=(width // 2,
                                            height // 2 + 50))

        # Khung hộp
        box_rect = title_rect.union(msg_rect).inflate(60, 40)
        pygame.draw.rect(self.screen, (0, 0, 0), box_rect, border_radius=12)
        pygame.draw.rect(self.screen, (255, 80, 80), box_rect, width=3, border_radius=12)

        # Vẽ chữ
        self.screen.blit(title_surf, title_rect)
        self.screen.blit(msg_surf, msg_rect)
        pygame.display.flip()

        
    def display_Game(self):
        self.screen.fill((255, 255, 255))
        self.display_Table()
        self.display_Item()
        self.display_Snake()
        pygame.display.flip()




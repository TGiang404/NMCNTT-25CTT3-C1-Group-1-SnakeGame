import pygame
from .intro import SceneBase, MenuScene, try_load_font 
from ..core.env_snake import SnakeGame

class GameScene(SceneBase):
    def __init__(self, app, mode="human"):
        super().__init__(app) 
        self.game = SnakeGame(app.cfg, mode)
        self.cell_size = app.cfg.cell_size
        self.hud_h = app.cfg.hud_h
        self.font_score = try_load_font(24) 
        self.background_image = self.app.images.get("game_bg")
    def handle(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.app.change_scene(MenuScene(self.app))
            elif not self.game.game_over and self.game.mode == "human":
                if event.key in (pygame.K_UP, pygame.K_w):
                    self.game.turn((0, -1))
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    self.game.turn((0, 1))
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    self.game.turn((-1, 0))
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    self.game.turn((1, 0))

    def draw_grid(self, screen):
        color = self.cfg.grid_line
        # 1. Vẽ các đường dọc
        for x in range(self.cfg.grid_w):
            px = x * self.cell_size
            pygame.draw.line(screen, color, (px, self.hud_h), (px, self.cfg.height))
        # 2. Vẽ các đường ngang
        for y in range(self.cfg.grid_h):
            py = self.hud_h + y * self.cell_size
            # Vẽ từ trái sang phải
            pygame.draw.line(screen, color, (0, py), (self.cfg.width, py))

    def update(self):
        self.game.update()

    def draw(self, screen):
        if self.background_image:
            screen.blit(self.background_image, (0, 0))
        else:
            screen.fill(self.cfg.bg_color)
           
        self.draw_grid(screen)
        hud_surface = pygame.Surface((self.cfg.width, self.hud_h), pygame.SRCALPHA)
        hud_surface.fill((20, 20, 30, 200)) 
        screen.blit(hud_surface, (0,0))
        
        pygame.draw.line(screen, (120, 255, 120), (0, self.hud_h - 2), (self.cfg.width, self.hud_h - 2), 3)
        # Điểm số
        score_text = self.font_score.render(f"Score: {self.game.score}", True, (255, 255, 255))
        screen.blit(score_text, (20, 20))
        # 3. Vẽ Mồi
        fx, fy = self.game.food
        food_rect = (fx * self.cell_size, self.hud_h + fy * self.cell_size, self.cell_size, self.cell_size)
        pygame.draw.rect(screen, self.cfg.food_color, food_rect, border_radius=8)
        # 4. Vẽ Rắn
        for i, (sx, sy) in enumerate(self.game.snake):
            color = self.cfg.head_color() if i == 0 else self.cfg.body_color()
            snake_rect = (sx * self.cell_size, self.hud_h + sy * self.cell_size, self.cell_size, self.cell_size)
            pygame.draw.rect(screen, color, snake_rect, border_radius=12)
        # 5. Màn hình Game Over
        if self.game.game_over:
            overlay = pygame.Surface((self.cfg.width, self.cfg.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180)) 
            screen.blit(overlay, (0,0))
            
            # Thông báo
            title_surf = self.font_title.render("GAME OVER", True, (255, 80, 80))
            title_rect = title_surf.get_rect(center=(self.cfg.width//2, self.cfg.height//2 - 40))
            
            msg_surf = self.font_msg.render("Press ESC to return to menu", True, (255, 255, 255))
            msg_rect = msg_surf.get_rect(center=(self.cfg.width//2, self.cfg.height//2 + 50))
            
            # Khung hộp thoại
            box_rect = title_rect.union(msg_rect).inflate(60, 40)
            pygame.draw.rect(screen, (0,0,0), box_rect, border_radius=12)
            pygame.draw.rect(screen, (255, 80, 80), box_rect, width=3, border_radius=12)
            
            screen.blit(title_surf, title_rect)
            screen.blit(msg_surf, msg_rect)
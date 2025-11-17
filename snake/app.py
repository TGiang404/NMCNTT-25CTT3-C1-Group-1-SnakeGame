import pygame
import os
from pathlib import Path
from .settings import Config, BOARD_PRESETS
from .scenes.intro import MenuScene
from .scenes.board import GameScene 

class App:
    def __init__(self):
        # Point to the parent directory of 'snake'
        self.base_dir = Path(__file__).resolve().parent.parent 
        
        default_size_key = "28x20"
        gw, gh = BOARD_PRESETS.get(default_size_key, (28, 20)) 
        
        self.cfg = Config(grid_w=gw, grid_h=gh)

        pygame.init()
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        self.screen = pygame.display.set_mode((self.cfg.width, self.cfg.height))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()

        self.images = self.load_images()
        
        self.scene = MenuScene(self)

    def load_images(self):
        """Hàm để tải ảnh từ assets"""
        imgs = {}
        
        try:
            bg_path = self.base_dir / "assets" / "images" / "menu_bg.png"
            # Check if file exists before loading to avoid crash if missing
            if os.path.exists(bg_path):
                bg_img = pygame.image.load(bg_path).convert_alpha()
                imgs["menu_bg"] = pygame.transform.scale(bg_img, (self.cfg.width, self.cfg.height))
            else:
                imgs["menu_bg"] = None
        except Exception as e:
            print(f"Không thể tải ảnh menu_bg.png: {e}")
            imgs["menu_bg"] = None
            
        try:
            game_bg_path = self.base_dir / "assets" / "images" / "background.png"
            if os.path.exists(game_bg_path):
                game_bg_img = pygame.image.load(game_bg_path).convert() 
                imgs["game_bg"] = pygame.transform.scale(game_bg_img, (self.cfg.width, self.cfg.height))
            else:
                imgs["game_bg"] = None
        except Exception as e:
            print(f"Không thể tải ảnh background.png: {e}")
            imgs["game_bg"] = None 
            
        return imgs
    
    def change_scene(self, scene):
        self.scene = scene

    def start_game(self, mode):
        self.scene = GameScene(self, mode)

    def run(self):
        """Vòng lặp game chính (Game Loop)"""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    if hasattr(self.scene, 'handle'):
                        self.scene.handle(event)

            if hasattr(self.scene, 'update'):
                self.scene.update()
            
            if hasattr(self.scene, 'draw'):
                self.scene.draw(self.screen)
                
            pygame.display.flip()
            self.clock.tick(self.cfg.fps_base())

        pygame.quit()
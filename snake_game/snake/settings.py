import pygame

class Settings:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
            cls._instance.init_settings()
        return cls._instance

    def init_settings(self):
        self.SCREEN_WIDTH = 1200 
        self.SCREEN_HEIGHT = 800
        self.GRID_SIZE = 40 
        self.GRID_WIDTH = self.SCREEN_WIDTH // self.GRID_SIZE
        self.GRID_HEIGHT = self.SCREEN_HEIGHT // self.GRID_SIZE
        self.FPS = 15 
        self.DIFFICULTY_NAME = "Normal"
        self.TEXT_COLOR = (0, 255, 0)       
        self.TEXT_HOVER_COLOR = (255, 255, 255) 
        self.BORDER_COLOR = (255, 0, 0)
        self.SNAKE_THEMES = [
            {"name": "Green",  "head": (0, 255, 0),     "body": (50, 205, 50)},
            {"name": "Blue",   "head": (0, 191, 255),   "body": (65, 105, 225)},
            {"name": "Purple", "head": (255, 0, 255),   "body": (148, 0, 211)},
            {"name": "Yellow", "head": (255, 215, 0),   "body": (218, 165, 32)},
        ]
        self.snake_idx = 0 
        # 2. Danh sách màu Nền
        self.BG_THEMES = [
            {"name": "Dark",   "color": (30, 30, 30),   "grid": (50, 50, 50)},
            {"name": "Black",  "color": (0, 0, 0),      "grid": (40, 40, 40)},
            {"name": "Blue",   "color": (10, 10, 40),   "grid": (30, 30, 70)},
            {"name": "Gray",   "color": (128, 128, 128),"grid": (160, 160, 160)},
        ]
        self.bg_idx = 0
        # 3. Danh sách màu Mồi
        self.FOOD_THEMES = [
            {"name": "Red",    "color": (255, 69, 0)},
            {"name": "Gold",   "color": (255, 215, 0)},
            {"name": "Blue",   "color": (0, 255, 255)},
            {"name": "Pink",   "color": (255, 105, 180)},
        ]
        self.food_idx = 0
        self.update_colors()

    def update_colors(self):
        snake_theme = self.SNAKE_THEMES[self.snake_idx]
        self.SNAKE_HEAD_COLOR = snake_theme["head"]
        self.SNAKE_BODY_COLOR = snake_theme["body"]

        bg_theme = self.BG_THEMES[self.bg_idx]
        self.BG_COLOR = bg_theme["color"]
        self.GRID_COLOR = bg_theme["grid"]

        food_theme = self.FOOD_THEMES[self.food_idx]
        self.FOOD_COLOR = food_theme["color"]

    def next_snake_color(self):
        self.snake_idx = (self.snake_idx + 1) % len(self.SNAKE_THEMES)
        self.update_colors()

    def next_bg_color(self):
        self.bg_idx = (self.bg_idx + 1) % len(self.BG_THEMES)
        self.update_colors()

    def next_food_color(self):
        self.food_idx = (self.food_idx + 1) % len(self.FOOD_THEMES)
        self.update_colors()
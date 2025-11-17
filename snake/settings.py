from dataclasses import dataclass
from typing import Tuple, Dict

Color = Tuple[int, int, int]

PALETTE: Dict[str, Color] = {
    "White": (245, 245, 245),
    "Black": (15, 18, 25),
    "Lime": (120, 255, 120),
    "Green": (0, 200, 140),
    "Teal": (0, 180, 200),
    "Cyan": (0, 220, 255),
    "Blue": (60, 130, 250),
    "Purple": (160, 120, 255),
    "Magenta": (255, 60, 200),
    "Red": (255, 80, 90),
    "Orange": (255, 140, 70),
    "Yellow": (255, 215, 80),
}

# Difficulty speeds
DIFFICULTY_SPEED = {
    "Easy": 6,
    "Normal": 10,
    "Hard": 14,
    "Extreme": 18
}

BOARD_PRESETS = {
    "28x20": (28, 20),      
    "36x24": (36, 24),      
    "40x30": (40, 30),       
}

@dataclass
class Config:
    cell_size: int = 28
    grid_w: int = 28  
    grid_h: int = 20  
    hud_h: int = 72   
    
    bg_color: Color = (18, 22, 32)
    grid_line: Color = (32, 38, 48)
    text_color: Color = (230, 234, 244)
    food_color: Color = (255, 215, 80)
    head_color_name: str = "Lime"
    body_color_name: str = "Teal"
    difficulty: str = "Normal"
    ai_speed: str = "1x"
    show_grid: bool = False

    @property
    def width(self) -> int:
        return self.grid_w * self.cell_size

    @property
    def height(self) -> int:
        return self.hud_h + self.grid_h * self.cell_size

    def head_color(self) -> Color:
        return PALETTE.get(self.head_color_name, (120, 255, 120))

    def body_color(self) -> Color:
        return PALETTE.get(self.body_color_name, (0, 180, 200))

    def fps_base(self) -> int:
        return DIFFICULTY_SPEED.get(self.difficulty, 10)

    def ai_multiplier(self) -> int:
        return {"1x": 1, "2x": 2, "5x": 5, "10x": 10}.get(self.ai_speed, 1)
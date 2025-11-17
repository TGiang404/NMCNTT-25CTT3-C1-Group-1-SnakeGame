import random
import pygame
from typing import List, Tuple

Vec = Tuple[int, int]

class SnakeGame:
    def __init__(self, cfg, mode="human"):
        self.cfg = cfg
        self.mode = mode
        self.reset()

    def reset(self):
        self.direction = (1, 0)
        cx, cy = self.cfg.grid_w // 2, self.cfg.grid_h // 2
        self.snake = [(cx, cy), (cx-1, cy), (cx-2, cy)]
        self.score = 0
        self.game_over = False
        self.spawn_food()

    def spawn_food(self):
        while True:
            x = random.randint(0, self.cfg.grid_w - 1)
            y = random.randint(0, self.cfg.grid_h - 1)
            if (x, y) not in self.snake:
                self.food = (x, y)
                break

    def turn(self, d: Vec):
        # Không cho quay đầu 180 độ
        if (self.direction[0] + d[0] != 0) or (self.direction[1] + d[1] != 0):
            self.direction = d

    def update(self):
        if self.game_over: return

        head = self.snake[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        # Kiểm tra va chạm tường
        if not (0 <= new_head[0] < self.cfg.grid_w and 0 <= new_head[1] < self.cfg.grid_h):
            self.game_over = True
            return
        # Kiểm tra cắn vào thân
        if new_head in self.snake:
            self.game_over = True
            return

        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.score += 1
            self.spawn_food()
        else:
            self.snake.pop()
import pygame
import random
import sys
import math
import numpy as np
from snake.scenes.board import Graphic
from snake.settings import Settings

class Play:
    def __init__(self, screen, Vec = [], Huong = 1, xi = -1, yi = -1):
        self.screen = screen
        self.cfg = Settings()
        self.limit_x = self.cfg.GRID_WIDTH - 2
        self.limit_y = self.cfg.GRID_HEIGHT - 2
        self.Vec = []
        self.Vec.append((4,1))
        self.Vec.append((3,1))
        self.Vec.append((2,1))
        self.Huong = 1
        self.xi = -1
        self.yi = -1

    def reset_Game(self):
        self.Vec = []
        self.Vec.append((3,1))
        self.Vec.append((2,1))
        self.Vec.append((1,1))
        self.Huong = 1

    def is_Collision(self, flag=None):
        if flag is None:
            flag = self.Vec[0]
        x, y = flag
        if x > self.limit_x or x < 1 or y > self.limit_y or y < 1:
            return True
        if flag in self.Vec[1]:
            return True
        return False
    

    def AI_move(self, action):
        head_x, head_y = self.Vec[0]
        old_distance = math.sqrt((head_x - self.xi)**2 + (head_y - self.yi)**2)

        clock_wise = [1, 4, 2, 3]
        idx = clock_wise.index(self.Huong)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]
        else: 
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]

        self.Huong = new_dir

        current_head_x = self.Vec[0][0]
        current_head_y = self.Vec[0][1]
        
        Pos_Head_new = (0,0)
        if self.Huong == 1: Pos_Head_new = (current_head_x + 1, current_head_y)
        elif self.Huong == 2: Pos_Head_new = (current_head_x - 1, current_head_y)
        elif self.Huong == 3: Pos_Head_new = (current_head_x, current_head_y - 1)
        elif self.Huong == 4: Pos_Head_new = (current_head_x, current_head_y + 1)

        self.Vec.insert(0, Pos_Head_new)
    
        new_head_x, new_head_y = self.Vec[0]
        new_distance = math.sqrt((new_head_x - self.xi)**2 + (new_head_y - self.yi)**2)

        reward = 0
        game_over = False
        
       
        if self.is_Collision() or len(self.Vec) > 100:
            game_over = True
            reward = -10 
            return reward, game_over, len(self.Vec) - 3

        if self.Vec[0] == (self.xi, self.yi):
            reward = 10 
            self.xi, self.yi = self.Take_random_pos()
            while (self.xi, self.yi) in self.Vec:
                 self.xi, self.yi = self.Take_random_pos()
        else:
            self.Vec.pop()
            if new_distance < old_distance:
                reward = 1  
            else:
                reward = -1.5
            
        GRAPHIC = Graphic(self.screen, self.Vec, self.xi, self.yi)
        GRAPHIC.display_Game()
        return reward, game_over, len(self.Vec) - 3

    def Update_Pos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_w or event.key == pygame.K_UP) and self.Huong != 4:
                    self.Huong = 3
                elif (event.key == pygame.K_s or event.key == pygame.K_DOWN) and self.Huong != 3:
                    self.Huong = 4
                elif (event.key == pygame.K_a or event.key == pygame.K_LEFT) and self.Huong != 1:
                    self.Huong = 2
                elif (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and self.Huong != 2:
                    self.Huong = 1

        current_head_x = self.Vec[0][0]
        current_head_y = self.Vec[0][1]
        
        Pos_Head_new = (0, 0)
        if self.Huong == 1: Pos_Head_new = (current_head_x + 1, current_head_y)
        elif self.Huong == 2: Pos_Head_new = (current_head_x - 1, current_head_y)
        elif self.Huong == 3: Pos_Head_new = (current_head_x, current_head_y - 1)
        elif self.Huong == 4: Pos_Head_new = (current_head_x, current_head_y + 1)

        self.Vec.insert(0, Pos_Head_new)
        self.Vec.pop()

    def End_Game(self):
        if (self.Vec[0][0] > self.limit_x): return True
        if (self.Vec[0][0] < 1): return True
        if (self.Vec[0][1] < 1): return True
        if (self.Vec[0][1] > self.limit_y): return True

        for i in range(len(self.Vec)):
            for j in range(i + 1, len(self.Vec)):
                if (self.Vec[i] == self.Vec[j]):
                    return True
        return False
    
    def Take_random_pos(self):
        x = random.randint(1, self.limit_x)
        y = random.randint(1, self.limit_y)
        return (x, y)

    def Take_Item_pos(self):
        x, y = self.Take_random_pos()
        for i in range(len(self.Vec)):
            if x == self.Vec[i][0] and y == self.Vec[i][1]:
                return self.Take_Item_pos()
        return (x, y)

    def Play_Game(self):
        running = True
        clock = pygame.time.Clock()
        self.reset_Game()
        self.xi, self.yi = self.Take_Item_pos()
        while running:
            current_speed = self.cfg.FPS + (len(self.Vec) // 5) 
            clock.tick(current_speed)
            GRAPHIC = Graphic(self.screen, self.Vec, self.xi, self.yi)
            self.Update_Pos()
            if not self.End_Game():
                GRAPHIC.display_Game()
            else:
                while True:
                    GRAPHIC.display_EndGame()
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                return
                        if event.type == pygame.QUIT: 
                            pygame.quit(); sys.exit()

            if self.Vec[0][0] == self.xi and self.Vec[0][1] == self.yi:
                self.Vec.append((self.xi, self.yi))
                self.xi, self.yi = self.Take_random_pos()
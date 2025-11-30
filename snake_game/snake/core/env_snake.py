import pygame
import random
import sys
from snake.scenes.board import Graphic
class Play:
    def __init__(self, screen, Vec = [], Huong = 1, xi = -1, yi = -1):
        self.screen = screen
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

    def Update_Pos(self):
        Pos_Head_new = (0, 0)

        if self.Huong == 1:
            Pos_Head_new = (self.Vec[0][0] + 1, self.Vec[0][1])
        else:
            if self.Huong == 2:
                Pos_Head_new = (self.Vec[0][0] - 1, self.Vec[0][1])
            else:
                if self.Huong == 3:
                    Pos_Head_new = (self.Vec[0][0], self.Vec[0][1] - 1)
                else:
                    Pos_Head_new = (self.Vec[0][0], self.Vec[0][1] + 1)

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    if self.Huong == 1:
                        Pos_Head_new = (self.Vec[0][0], self.Vec[0][1] - 1)
                        self.Huong = 3
                    else:
                        if self.Huong == 2:
                            Pos_Head_new = (self.Vec[0][0], self.Vec[0][1] + 1)
                            self.Huong = 4
                        else:
                            if self.Huong == 3:
                                Pos_Head_new = (self.Vec[0][0] - 1, self.Vec[0][1])
                                self.Huong = 2
                            else:
                                Pos_Head_new = (self.Vec[0][0] + 1, self.Vec[0][1])
                                self.Huong = 1
                elif event.key == pygame.K_d:
                    if self.Huong == 1:
                        Pos_Head_new = (self.Vec[0][0], self.Vec[0][1] + 1)
                        self.Huong = 4
                    else:
                        if self.Huong == 2:
                            Pos_Head_new = (self.Vec[0][0], self.Vec[0][1] - 1)
                            self.Huong = 3
                        else:
                            if self.Huong == 3:
                                Pos_Head_new = (self.Vec[0][0] + 1, self.Vec[0][1])
                                self.Huong = 1
                            else:
                                Pos_Head_new = (self.Vec[0][0] - 1, self.Vec[0][1])
                                self.Huong = 2

        self.Vec.insert(0, Pos_Head_new)
        self.Vec.pop()

    def End_Game(self):
        if (self.Vec[0][0] > 18): return True
        if (self.Vec[0][0] < 1): return True
        if (self.Vec[0][1] < 1): return True
        if (self.Vec[0][1] > 11): return True

        for i in range(len(self.Vec)):
            for j in range(i + 1, len(self.Vec)):
                if (self.Vec[i] == self.Vec[j]):
                    return True

        return False
    
    def Take_random_pos(self):
        x = random.randint(1, 18)
        y = random.randint(1, 11)
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
            clock.tick(1.5 + len(self.Vec) // 15)

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

            if self.Vec[0][0] == self.xi and self.Vec[0][1] == self.yi:
                self.Vec.append((self.xi, self.yi))
                self.xi, self.yi = self.Take_random_pos()
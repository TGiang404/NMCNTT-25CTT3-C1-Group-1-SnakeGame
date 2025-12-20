import torch
import random
import numpy as np
from snake.core.env_snake import Play 
from collections import deque
from snake.rl.dqn_model import Linear_QNet, QTrainer
from snake.rl.memory import ReplayMemory

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # Randomness (sẽ giảm dần)
        self.gamma = 0.9 # Discount rate (< 1)
        self.memory = ReplayMemory(MAX_MEMORY)
        self.model = Linear_QNet(11, 256, 3) 
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        head = game.Vec[0]
        point_l = (head[0] - 1, head[1])
        point_r = (head[0] + 1, head[1])
        point_u = (head[0], head[1] - 1)
        point_d = (head[0], head[1] + 1)
        dir_r = game.Huong == 1
        dir_l = game.Huong == 2
        dir_u = game.Huong == 3
        dir_d = game.Huong == 4

        state = [
            (dir_r and game.is_Collision(point_r)) or 
            (dir_l and game.is_Collision(point_l)) or 
            (dir_u and game.is_Collision(point_u)) or 
            (dir_d and game.is_Collision(point_d)),

            # 2. Nguy hiểm bên phải (Right)
            (dir_u and game.is_Collision(point_r)) or 
            (dir_d and game.is_Collision(point_l)) or 
            (dir_l and game.is_Collision(point_u)) or 
            (dir_r and game.is_Collision(point_d)),

            # 3. Nguy hiểm bên trái (Left)
            (dir_d and game.is_Collision(point_r)) or 
            (dir_u and game.is_Collision(point_l)) or 
            (dir_r and game.is_Collision(point_u)) or 
            (dir_l and game.is_Collision(point_d)),
            
            # 4. Hướng di chuyển
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            # 5. Vị trí mồi (Food location)
            game.xi < head[0],  # Food Left
            game.xi > head[0],  # Food Right
            game.yi < head[1],  # Food Up
            game.yi > head[1]   # Food Down
        ]
        
        return np.array(state, dtype=int)

    def get_action(self, state):
        self.epsilon = 80 - self.n_games
        final_move = [0, 0, 0]
        
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
            
        return final_move

    def remember(self, state, action, reward, next_state, done):
        self.memory.add(state, action, reward, next_state, done)

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = self.memory.sample(BATCH_SIZE)
        else:
            mini_sample = self.memory.memory
            
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)
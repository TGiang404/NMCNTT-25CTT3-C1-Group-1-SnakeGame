import random
from collections import deque

class ReplayMemory:
    def __init__(self, max_len=100_000):
        self.memory = deque(maxlen=max_len)

    def add(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        if len(self.memory) < batch_size:
            return list(self.memory)
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)
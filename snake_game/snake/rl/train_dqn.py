import pygame
import sys
import torch
import os
from snake.rl.agent_dqn import Agent
from snake.core.env_snake import Play
from snake.settings import Settings

def train(training_mode=True):
    TRAINING_MODE = training_mode 
    
    pygame.init()
    cfg = Settings()
    screen = pygame.display.get_surface()
    if screen is None:
        screen = pygame.display.set_mode((cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT))
        
    caption = f"Snake AI - {cfg.DIFFICULTY_NAME} Mode"
    pygame.display.set_caption(caption)
    
    game = Play(screen)
    agent = Agent()
    clock = pygame.time.Clock() 

    if not TRAINING_MODE:
        caption += " (WATCHING)"
    pygame.display.set_caption(caption)
    
    game = Play(screen)
    agent = Agent()
    clock = pygame.time.Clock()

    if TRAINING_MODE:
        print(f"--- ĐANG HUẤN LUYỆN: {cfg.DIFFICULTY_NAME} (FPS Gốc: {cfg.FPS}) ---")
        record = 0
    else:
        print(f"--- ĐANG XEM AI CHƠI: {cfg.DIFFICULTY_NAME} ---")
        model_path = './model/model.pth'
        if os.path.exists(model_path):
            agent.model.load_state_dict(torch.load(model_path))
            agent.model.eval()
            agent.n_games = 100
        else:
            print("LỖI: Không tìm thấy model.pth! Vui lòng Train trước.")
            return 

    while True:
        score = len(game.Vec) - 3
        current_speed = cfg.FPS + (score // 5)
        
        if TRAINING_MODE:
            clock.tick(current_speed * 2) 
        else:
            # Chế độ xem biểu diễn: chạy đúng tốc độ thực tế
            clock.tick(current_speed)

        # 1. Lấy trạng thái hiện tại
        state_old = agent.get_state(game)

        # 2. Dự đoán nước đi
        final_move = agent.get_action(state_old)

        # 3. Thực hiện nước đi
        reward, done, score = game.AI_move(final_move)
        
        # 4. Lấy trạng thái mới
        state_new = agent.get_state(game)

        if TRAINING_MODE:
            agent.train_short_memory(state_old, final_move, reward, state_new, done)
            agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            game.reset_Game()
            agent.n_games += 1
            
            if TRAINING_MODE:
                agent.train_long_memory()
                if score > record:
                    record = score
                    agent.model.save()
                print(f'Game: {agent.n_games}, Score: {score}, Record: {record}, Mode: {cfg.DIFFICULTY_NAME}')
            else:
                print(f'Test Score: {score}')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

if __name__ == '__main__':
    train()
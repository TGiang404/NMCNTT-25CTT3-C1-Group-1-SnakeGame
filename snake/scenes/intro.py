import pygame
from ..settings import Config


def try_load_font(size=20):
    
    try:

        return pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", size)
    except:

        return pygame.font.SysFont("Consolas", size, bold=True)

class Button:
    def __init__(self, rect, text, on_click, font_size=22): 
        self.rect = rect
        self.text = text
        self.on_click = on_click
        self.font = try_load_font(font_size) 
        self.hover = False

    def handle(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.on_click()

    def draw(self, surface):

        bg_color = (70, 80, 100) if self.hover else (40, 45, 60)
        border_color = (120, 255, 120) if self.hover else (100, 110, 140) 
        text_color = (255, 255, 255)

        pygame.draw.rect(surface, (20, 20, 25), self.rect.inflate(4,4), border_radius=12) 
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=12)
        pygame.draw.rect(surface, border_color, self.rect, width=3, border_radius=12) 
       
        txt = self.font.render(self.text, True, text_color)
        surface.blit(txt, txt.get_rect(center=self.rect.center))


class SceneBase:
    def __init__(self, app):
        self.app = app
        self.cfg = app.cfg
        self.font_title = try_load_font(65) 

        self.font_msg = try_load_font(18)   

    def handle(self, event): pass
    def update(self): pass
    def draw(self, screen): pass

class MenuScene(SceneBase):
    def __init__(self, app):
        super().__init__(app)
        
        btn_w, btn_h = 400, 65   
        spacing = 90            
        
        cx = self.cfg.width // 2
        cy = self.cfg.hud_h + 60 

        self.message = ""
        self.message_timer = 0

        def show_dev_msg():
            self.message = "This feature is currently developing"
            self.message_timer = pygame.time.get_ticks()
        font_size_btn = 24
        self.buttons = [
            Button(pygame.Rect(cx - btn_w//2, cy, btn_w, btn_h), "Play (Human)", 
                   lambda: self.app.start_game("human"), font_size_btn),
            
            Button(pygame.Rect(cx - btn_w//2, cy + spacing, btn_w, btn_h), "AI Mode", 
                   show_dev_msg, font_size_btn),
            
            Button(pygame.Rect(cx - btn_w//2, cy + spacing*2, btn_w, btn_h), "Options", 
                   show_dev_msg, font_size_btn),
            
            Button(pygame.Rect(cx - btn_w//2, cy + spacing*3, btn_w, btn_h), "Exit", 
                   lambda: pygame.event.post(pygame.event.Event(pygame.QUIT)), font_size_btn),
        ]

        self.background_image = self.app.images.get("menu_bg")
        if self.background_image:
            self.background_image = pygame.transform.scale(self.background_image, (self.cfg.width, self.cfg.height))

    def handle(self, event):
        for b in self.buttons: b.handle(event)

    def update(self):
        if self.message and pygame.time.get_ticks() - self.message_timer > 2000:
            self.message = ""

    def draw(self, screen):
        # 1. Vẽ nền
        if self.background_image:
            screen.blit(self.background_image, (0, 0))
        else:
            screen.fill(self.cfg.bg_color)

        title_text = "SNAKE"
        title_shadow = self.font_title.render(title_text, True, (0, 0, 0))
        screen.blit(title_shadow, title_shadow.get_rect(center=(self.cfg.width//2 + 4, 70 + 4)))
        title = self.font_title.render(title_text, True, (120, 255, 120))
        screen.blit(title, title.get_rect(center=(self.cfg.width//2, 70)))
        for b in self.buttons: b.draw(screen)
        if self.message:
            msg_surf = self.font_msg.render(self.message, True, (255, 255, 80)) 
            bg_rect = msg_surf.get_rect(center=(self.cfg.width//2, self.cfg.height - 40))
            
            box_rect = bg_rect.inflate(30, 20)
            pygame.draw.rect(screen, (0,0,0), box_rect, border_radius=8)
            pygame.draw.rect(screen, (255,255,0), box_rect, width=2, border_radius=8)
            
            screen.blit(msg_surf, bg_rect)
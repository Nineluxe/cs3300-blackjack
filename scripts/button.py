import pygame

class Button:
    
    def __init__(self, x, y, w, h, color, text, font):
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.font = font
        self.text = text
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.fillColor = color
        self.cornerRadius = 2
        self.borderColor = pygame.color.Color(0, 0, 0, 255)
        self.textColor = pygame.color.Color(255, 255, 255, 255)
        self.outlineWidth = 2

    def isMouseOver(self, mousePos):
        return self.rect.collidepoint(mousePos)
    
    def draw(self, surface):
        # Draw filled rectangle
        pygame.draw.rect(surface, self.fillColor, self.rect, border_radius=self.cornerRadius)
        
        # Draw outline
        pygame.draw.rect(surface, self.borderColor, self.rect, width=self.outlineWidth, border_radius=self.cornerRadius)

        # Render text and center it
        text_surface = self.font.render(self.text, True, self.textColor)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    # Unused 
    def update(self, dt):
        pass
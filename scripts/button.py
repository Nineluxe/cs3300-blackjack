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
        self.blackColor = pygame.color.Color(0, 0, 0, 255)
        self.whiteColor = pygame.color.Color(255, 255, 255, 255)
        self.borderColor = self.blackColor
        self.textColor = self.whiteColor
        self.outlineWidth = 2
        self.disabled = False
        self.doDraw = True
    
    def isMouseOver(self, mousePos):     
        if self.disabled:
            return False
        return self.rect.collidepoint(mousePos)
    
    # Function not currently used
    def update(self, dt):
        pass

    def draw(self, surface, mousePos):  # Add mousePos parameter
        if not self.doDraw:
            return
        
        # Update border color based on hover state
        if self.isMouseOver(mousePos):
            self.borderColor = self.whiteColor
        else:
            self.borderColor = self.blackColor
        
        # Draw filled rectangle
        pygame.draw.rect(surface, self.fillColor, self.rect, border_radius=self.cornerRadius)
        
        # Draw outline
        pygame.draw.rect(surface, self.borderColor, self.rect, width=self.outlineWidth, border_radius=self.cornerRadius)
        
        # Render text and center it
        text_surface = self.font.render(self.text, True, self.textColor)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
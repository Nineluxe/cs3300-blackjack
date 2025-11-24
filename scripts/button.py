
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

    def isMouseOver(self, mousePos):
        return self.rect.collidepoint(mousePos)

    def draw(self, surface):
        pygame.draw.rect(surface, self.fillColor, self.rect, border_radius=1)

        self.font.render("Testing", False, pygame.color.Color(255, 255, 255, 255))

    def update(self, dt):
        pass
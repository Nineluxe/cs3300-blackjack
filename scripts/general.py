
import pygame

# Simple linear interpolation function
def lerp(start, stop, amount):
    return start + (stop - start) * amount

# Draw text at the coordinates with alignment
def drawText(coords: tuple, text, font, color, surface, horizontalAlignment="left"):
    rendered_text = font.render(text, False, color)
    text_rect = rendered_text.get_rect()
    
    # Adjust x-coordinate based on alignment
    x, y = coords
    if horizontalAlignment == "center":
        text_rect.centerx = x
        text_rect.y = y
    elif horizontalAlignment == "right":
        text_rect.right = x
        text_rect.y = y
    else:
        text_rect.x = x
        text_rect.y = y
    
    surface.blit(rendered_text, text_rect)
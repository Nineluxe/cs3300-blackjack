
import pygame
import math
import random

# Define constants
BASE_WIDTH, BASE_HEIGHT = 320, 180
SCALE = 4
WINDOW_WIDTH, WINDOW_HEIGHT = BASE_WIDTH * SCALE, BASE_HEIGHT * SCALE

# Initialize
pygame.init()
clock = pygame.time.Clock()
entityList = list()
pygame.font.init()
font = pygame.font.SysFont(None, 16)  # None = default system font, 24 = size
debugging = False

# Create surfaces
base_surface = pygame.Surface( (BASE_WIDTH, BASE_HEIGHT) )
window = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Super Blackjack 9000")

# Create sprite groups
collision_group = pygame.sprite.Group()
score = 0  # Global counter

# Main loop
running = True
game_paused = False
while running:
    
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
      
    # Get key states
    keys = pygame.key.get_pressed()

    # Get mouse position and scale it based on window size
    mouse = pygame.mouse.get_pos()
    mouse_scaled = (mouse[0] / SCALE, mouse[1] / SCALE)

    # Debug
    if keys[pygame.K_ESCAPE]:
        running = False

    # Fill color
    base_surface.fill( (29, 71, 46) )

    # DRAW HERE
    for entity in entityList:
        if not game_paused:
            entity.update()

        entity.draw()

    # Scale and blit to window
    scaled_surface = pygame.transform.scale(base_surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
    window.blit(scaled_surface, (0, 0))

    # Flip the display to put your work on screen
    pygame.display.flip()

    # Limit the FPS to 60
    clock.tick(60)
pygame.quit()


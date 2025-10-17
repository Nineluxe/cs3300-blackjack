<<<<<<< HEAD
print("Let's go gambling!!!")
print("Bryce")
print("Elijah")

<<<<<<< Updated upstream
=======
=======

>>>>>>> bryce
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
<<<<<<< HEAD
pygame.display.set_caption("Super Blackjack 9000")
=======
pygame.display.set_caption("Blackjack")
>>>>>>> bryce

# Create sprite groups
collision_group = pygame.sprite.Group()
score = 0  # Global counter

<<<<<<< HEAD
# # Basic snake segment class
# class Segment(pygame.sprite.Sprite):
#     def __init__(self, _x, _y):
#         super().__init__() # initialize the parent Sprite class
#         self.x = _x
#         self.y = _y
#         self.collision_size = 7.0
#         self.sprite_radius = 5.0

#         # Collision
#         self.image = pygame.Surface((self.collision_size, self.collision_size))  # Visual size of sprite
#         self.image.fill("red")  # Fill with color
#         self.rect = self.image.get_rect()  # Get rectangle for positioning
#         self.rect.center = (self.x, self.y)  # Center player

#         self.movespeed = 2.0
#         self.turnspeed = 0.1
#         self.x_vel = 0.0
#         self.y_vel = 0.0
#         self.move_direction = 0.0
#         self.child = None
#         self.parent = None
#         self.trail = []
#         self.trail_spacing = 10
#         entityList.append(self)

#     def update(self):
#         if self.parent is None:
#             # Head movement
#             self.x_vel = self.movespeed * math.cos(self.move_direction)
#             self.y_vel = self.movespeed * math.sin(self.move_direction)
#             self.x += self.x_vel
#             self.y += self.y_vel

#             self.trail.append((self.x, self.y))
#             if len(self.trail) > 1000:
#                 self.trail.pop(0)
#         else:
            
#             if len(self.parent.trail) > self.trail_spacing:
#                 target_pos = self.parent.trail[-self.trail_spacing]
#                 self.x += (target_pos[0] - self.x) * 0.3
#                 self.y += (target_pos[1] - self.y) * 0.3
#                 self.trail.append((self.x, self.y))

#                 if len(self.trail) > 1000:
#                     self.trail.pop(0)

#         # Update collision box location (updated)
#         self.rect.center = (self.x, self.y)

#     def draw(self):

#         # Draw self
#         pygame.draw.circle(base_surface, "black", (self.x - 1, self.y + 1), self.sprite_radius)

#         # Draw self
#         pygame.draw.circle(base_surface, "red", (self.x, self.y), self.sprite_radius)

#         # Draw collision
#         if debugging == True:
#             pygame.draw.rect(base_surface, "lime", self.rect, width=1)

#     def addChild(self, group):
#         global score
#         score += 1
        
#         self.child = Segment(self.x, self.y)
#         self.child.parent = self
#         self.child.movespeed = self.movespeed
#         self.child.turnspeed = self.turnspeed

#         group.add(self)
#         return self.child
    
#     # Remove self from the global entity list when destroyed
#     def delete(self):
#         entityList.remove(self)

#     def check_collision(self, group):
        
#         collisions = []

#         for sprite in group:
#             if sprite is not self and self.rect.colliderect(sprite.rect):
#                 collisions.append(sprite)

#         # Iterate through  collision list
#         for collided in collisions:

#             # Check if collision is with upgrade type
#             if isinstance(collided, Upgrade):
#                 print("Upgrade collected!")

#                 # Move upgrade to a new, random location
#                 collided.random_location()

#                 # Add new tail segment
#                 global head
#                 last = head
#                 while last.child:
#                     last = last.child
#                 last = last.addChild(group)

#             elif isinstance(collided, Segment):
#                 global game_paused
#                 game_paused = True

=======
>>>>>>> bryce
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

<<<<<<< HEAD
    if game_paused == False:
        text_surface = font.render(f"Score: {score}", True, "white")
        base_surface.blit(text_surface, (140, 10))
    else:
        # Draw "Game Over!" below the score
        text_surface1 = font.render(f"Score: {score}", True, "white")
        text_surface2 = font.render("Game Over!", True, "white")

        base_surface.blit(text_surface1, (140, 10))   # Score at top
        base_surface.blit(text_surface2, (140, 30))   # Game Over below it

    # DRAW HERE
    for entity in entityList:
        if game_paused == False:
=======
    # DRAW HERE
    for entity in entityList:
        if not game_paused:
>>>>>>> bryce
            entity.update()

        entity.draw()

    # Scale and blit to window
    scaled_surface = pygame.transform.scale(base_surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
    window.blit(scaled_surface, (0, 0))

    # Flip the display to put your work on screen
    pygame.display.flip()

    # Limit the FPS to 60
    clock.tick(60)

<<<<<<< HEAD
pygame.quit()
>>>>>>> Stashed changes
=======
pygame.quit()
>>>>>>> bryce

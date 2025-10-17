# Basic snake segment class
class Segment(pygame.sprite.Sprite):
    def __init__(self, _x, _y):
        super().__init__() # initialize the parent Sprite class
        self.x = _x
        self.y = _y
        self.collision_size = 7.0
        self.sprite_radius = 5.0

        # Collision
        self.image = pygame.Surface((self.collision_size, self.collision_size))  # Visual size of sprite
        self.image.fill("red")  # Fill with color
        self.rect = self.image.get_rect()  # Get rectangle for positioning
        self.rect.center = (self.x, self.y)  # Center player

        self.movespeed = 2.0
        self.turnspeed = 0.1
        self.x_vel = 0.0
        self.y_vel = 0.0
        self.move_direction = 0.0
        self.child = None
        self.parent = None
        self.trail = []
        self.trail_spacing = 10
        entityList.append(self)

    def update(self):
        if self.parent is None:
            # Head movement
            self.x_vel = self.movespeed * math.cos(self.move_direction)
            self.y_vel = self.movespeed * math.sin(self.move_direction)
            self.x += self.x_vel
            self.y += self.y_vel

            self.trail.append((self.x, self.y))
            if len(self.trail) > 1000:
                self.trail.pop(0)
        else:
            
            if len(self.parent.trail) > self.trail_spacing:
                target_pos = self.parent.trail[-self.trail_spacing]
                self.x += (target_pos[0] - self.x) * 0.3
                self.y += (target_pos[1] - self.y) * 0.3
                self.trail.append((self.x, self.y))

                if len(self.trail) > 1000:
                    self.trail.pop(0)

        # Update collision box location (updated)
        self.rect.center = (self.x, self.y)

    def draw(self):

        # Draw self
        pygame.draw.circle(base_surface, "black", (self.x - 1, self.y + 1), self.sprite_radius)

        # Draw self
        pygame.draw.circle(base_surface, "red", (self.x, self.y), self.sprite_radius)

        # Draw collision
        if debugging == True:
            pygame.draw.rect(base_surface, "lime", self.rect, width=1)

    def addChild(self, group):
        global score
        score += 1
        
        self.child = Segment(self.x, self.y)
        self.child.parent = self
        self.child.movespeed = self.movespeed
        self.child.turnspeed = self.turnspeed

        group.add(self)
        return self.child
    
    # Remove self from the global entity list when destroyed
    def delete(self):
        entityList.remove(self)

    def check_collision(self, group):
        
        collisions = []

        for sprite in group:
            if sprite is not self and self.rect.colliderect(sprite.rect):
                collisions.append(sprite)

        # Iterate through  collision list
        for collided in collisions:

            # Check if collision is with upgrade type
            if isinstance(collided, Upgrade):
                print("Upgrade collected!")

                # Move upgrade to a new, random location
                collided.random_location()

                # Add new tail segment
                global head
                last = head
                while last.child:
                    last = last.child
                last = last.addChild(group)

            elif isinstance(collided, Segment):
                global game_paused
                game_paused = True

# Upgrade pellet class
class Upgrade(pygame.sprite.Sprite):

    def __init__(self, _x, _y):
        super().__init__()
        self.x = _x
        self.y = _y
        self.collision_size = 5
        entityList.append(self)

        # Collision
        self.image = pygame.Surface((self.collision_size, self.collision_size))  # Visual size of sprite
        self.image.fill("yellow")  # Fill with color
        self.rect = self.image.get_rect()  # Get rectangle for positioning
        self.rect.center = (self.x, self.y)  # Center player

    def random_location(self):
        self.x = random.randint(self.collision_size, BASE_WIDTH - self.collision_size)
        self.y = random.randint(self.collision_size, BASE_HEIGHT - self.collision_size)
        self.rect.center = (self.x, self.y)
        print(f"Random location found!: ")

    def draw(self):
        
        pygame.draw.rect(base_surface, "yellow", self.rect)

    # Remove self from the global entity list when destroyed
    def destroy(self):
        entityList.remove(self)

Instantiate player and add to group
collision_group.add(head)

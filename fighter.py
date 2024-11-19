import pygame

class Fighter():
    def __init__(self, x, y):
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.jump = False

    
    def move(self, screen_width, screen_height):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0

        # Get keypresses
        key = pygame.key.get_pressed()

        # Movement
        if key[pygame.K_a]:
            dx = -SPEED 
        if key[pygame.K_d]:
            dx = +SPEED
        # Jump
        if key[pygame.K_w] and self.jump == False:
            self.vel_y = -30
            self.jump = True
        
        # Apply Gravity
        self.vel_y += GRAVITY
        dy += self.vel_y
        
        # Ensure player stays on screen
        if self.rect.left + dx < 0:
            dx = 0 - self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 20:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 20 - self.rect.bottom
        
        # Update player position
        self.rect.x += dx
        self.rect.y += dy

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)
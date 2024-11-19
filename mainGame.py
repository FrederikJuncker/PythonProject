import pygame
from fighter import Fighter

pygame.init()

# Create Game Window
SCREEN_WIDTH = 1000
SCEEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCEEN_HEIGHT))
pygame.display.set_caption("Brawler")

# Set Framerate, so playars dont move to fast
clock = pygame.time.Clock()
FPS = 60

# Load Background Image
bg_image = pygame.image.load("Pygame/images/KoreaJPG.jpg").convert_alpha()

# Function for Drawing Background
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCEEN_HEIGHT))
    screen.blit(scaled_bg, (0,0))

# Create to Instances of Figthers
figther_1 = Fighter(200, 400)
figther_2 = Fighter(700, 400)

# ---------------------- Game Loop ----------------------
run = True
while run:
    # Clock / Framerate
    clock.tick(FPS)

    # Draw Background
    draw_bg()

    # Move Fighters
    figther_1.move(SCREEN_WIDTH, SCEEN_HEIGHT)
    

    # Draw Fighters
    figther_1.draw(screen)
    figther_2.draw(screen)

    # Event Handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    key = pygame.key.get_pressed()
    if key[pygame.K_ESCAPE]:
        run = False

    # Update Display
    pygame.display.update()

#Exit Pygame
pygame.quit()
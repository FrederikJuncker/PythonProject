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

# Defines colors
RED = (255,0,0)
YELLOW = (255,255,0)
WHITE = (0,0,0)

# Define Figher variables
SAMURAI1_SIZE = 128 # 128
SAMURAI1_SCALE = 2.5
SAMURAI1_OFFSET = [20, 60] # 60
SAMURAI1_DATA = [SAMURAI1_SIZE, SAMURAI1_SCALE, SAMURAI1_OFFSET]

SAMURAI2_SIZE = 128 # 128
SAMURAI2_SCALE = 2.5
SAMURAI2_OFFSET = [45, 60] # 60
SAMURAI2_DATA = [SAMURAI2_SIZE, SAMURAI2_SCALE, SAMURAI2_OFFSET]

# Load Background Image
bg_image = pygame.image.load("C:/Users/Frede/OneDrive/Skrivebord/University/5 Semester/Python/Pygame/korea.jpg").convert_alpha()

# Load Sprite Sheet
samurai1_sheet = pygame.image.load("C:/Users/Frede/OneDrive/Skrivebord/University/5 Semester/Python/Pygame/Sam1_spritesheet.png").convert_alpha()
samurai2_sheet = pygame.image.load("C:/Users/Frede/OneDrive/Skrivebord/University/5 Semester/Python/Pygame/Sam2_spritesheet.png").convert_alpha()

# Define Numbers of Steps in each animations
SAMURAI1_ANIMATIONS_STEPS = [6, 8, 9, 5, 4, 3, 6]
SAMURAI2_ANIMATIONS_STEPS = [5, 8, 7, 5, 4, 2, 6]

# Function for Drawing Background
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCEEN_HEIGHT))
    screen.blit(scaled_bg, (0,0))

# Function for Drawing figher healt bar
def draw_healt_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))

# Create to Instances of Figthers
figther_1 = Fighter(200, 400, False, SAMURAI1_DATA, samurai1_sheet, SAMURAI1_ANIMATIONS_STEPS) # 200 400
figther_2 = Fighter(700, 400, True, SAMURAI2_DATA, samurai2_sheet, SAMURAI2_ANIMATIONS_STEPS) # 700 400

# ---------------------- Game Loop ----------------------
run = True
while run:
    # Clock / Framerate
    clock.tick(FPS)

    # Draw Background
    draw_bg()

    # Shower Player Stats
    draw_healt_bar(figther_1.health, 20, 20)
    draw_healt_bar(figther_2.health, 580, 20)

    # Move Fighters
    figther_1.move(SCREEN_WIDTH, SCEEN_HEIGHT, screen, figther_2)

    # Update Fighters
    figther_1.update()
    figther_2.update()
    
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
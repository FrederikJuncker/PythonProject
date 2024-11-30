import pygame
from fighter import Fighter

pygame.init()

# Create Game Window
SCREEN_WIDTH = 1000
SCEEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCEEN_HEIGHT))
pygame.display.set_caption("Brawler")

# Set Framerate
clock = pygame.time.Clock()
FPS = 60

# Define colors
RED = (255,0,0)
YELLOW = (255,255,0)
WHITE = (0,0,0)

# Define Fighter variables
SAMURAI1_SIZE = 128
SAMURAI1_SCALE = 2.5
SAMURAI1_OFFSET = [20, 60]
SAMURAI1_DATA = [SAMURAI1_SIZE, SAMURAI1_SCALE, SAMURAI1_OFFSET]

SAMURAI2_SIZE = 128
SAMURAI2_SCALE = 2.5
SAMURAI2_OFFSET = [45, 60]
SAMURAI2_DATA = [SAMURAI2_SIZE, SAMURAI2_SCALE, SAMURAI2_OFFSET]

# Load Background Image
bg_image = pygame.image.load("korea.jpg").convert_alpha()

# Load Sprite Sheets
samurai1_sheet = pygame.image.load("Sam1_spritesheet.png").convert_alpha()
samurai2_sheet = pygame.image.load("Sam2_spritesheet.png").convert_alpha()

# Define animation steps
SAMURAI1_ANIMATIONS_STEPS = [6, 8, 9, 5, 4, 3, 6]
SAMURAI2_ANIMATIONS_STEPS = [5, 8, 7, 5, 4, 2, 6]

def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCEEN_HEIGHT))
    screen.blit(scaled_bg, (0,0))

def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))

# Create fighters
fighter_1 = Fighter(200, 400, False, SAMURAI1_DATA, samurai1_sheet, SAMURAI1_ANIMATIONS_STEPS, 1)
fighter_2 = Fighter(700, 400, True, SAMURAI2_DATA, samurai2_sheet, SAMURAI2_ANIMATIONS_STEPS, 2)

# Game Loop
run = True
while run:
    clock.tick(FPS)

    # Draw background
    draw_bg()

    # Show health bars
    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 580, 20)

    # Move fighters
    fighter_1.move(SCREEN_WIDTH, SCEEN_HEIGHT, screen, fighter_2)
    fighter_2.move(SCREEN_WIDTH, SCEEN_HEIGHT, screen, fighter_1)

    # Update fighters
    fighter_1.update()
    fighter_2.update()
    
    # Draw fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        run = False

    # Update display
    pygame.display.update()

pygame.quit()

from operator import truediv
import pygame
import os
import time
import random
pygame.font.init()  #Initialize fonts

# Initalize Pygame surface for drawing(size only)
WXH = (750, 750) #Width x Height
WINDOW = pygame.display.set_mode(WXH)
pygame.display.set_caption("Space Command")

# Load image assets
# Enemy ships
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

# Player Ship
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# Background Image and fit window
BG = pygame.image.load(os.path.join("assets", "background-black.png"))
BG = pygame.transform.scale(BG, WXH)

# Define movable objects
class Ship:
    def __init__(self, (x,y), health=100):
        self.pos = (x,y)
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0
    def draw(self):
        self.x += 1


# Set up fonts
# font colour and attributes
ANTIALIAS = True
WHITE=(255,255,255)
FONT_SIZE = 50
# Create main font
main_font = pygame.font.SysFont("comicsans", FONT_SIZE)

def main():

    # Collision checking setup
    run = True
    FPS = 60 #Frames per second
    clock = pygame.time.Clock()

    # Game Play Variables
    level = 1
    lives = 5

    def redraw_window():

        #Cover previous screen
        WINDOW.blit(BG, (0,0))

        # Print user info
        level_label=main_font.render(f"Level: {level}", ANTIALIAS, WHITE)
        lives_label=main_font.render(f"Lives: {lives}", ANTIALIAS, WHITE)

        WINDOW.blit(level_label, (10,10))
        WINDOW.blit(lives_label,(BG.get_width()-10-lives_label.get_width(),10))

        #Update Surface
        pygame.display.update()

    while run:
        
        #wait for tick
        clock.tick(FPS)

        #draw window
        redraw_window()

        #Check for user inputs
        for event in pygame.event.get():

            #Check for QUIT
            if event.type == pygame.QUIT:
                run = False
                
                


main()
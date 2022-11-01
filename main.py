from operator import truediv
import pygame
import os
import time
import random


# Initalize Pygame surface for drawing(size only)
WXH = (750, 750)
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

# Background Image
BG = pygame.image.load(os.path.join("assets", "background-black.png"))
BG = pygame.transform.scale(BG, WXH)

def main():

    # Collision checking setup
    run = True
    FPS = 60 #Frames per second
    clock = pygame.time.Clock()

    def redraw_window():

        #Cover previous screen
        WINDOW.blit
        WINDOW.blit(BG, (0,0))

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
from operator import truediv
import pygame
import os
import time
import random

pygame.font.init()  #Initialize fonts

# Initalize Pygame surface for drawing(size only)
WIDTH = 750
HEIGHT = 750
WXH = [WIDTH, HEIGHT] #Width x Height
WINDOW = pygame.display.set_mode(WXH)
pygame.display.set_caption("Space Command")

# Load image assets
# Enemy ships
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

# Player Ship
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# Background Image and fit window
BG = pygame.image.load(os.path.join("assets", "background-black.png"))
BG = pygame.transform.scale(BG, WXH)

#colour constants
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

# Set up fonts
# font colour and attributes
ANTIALIAS = True
FONT_SIZE = 50
# Create fonts
main_font = pygame.font.SysFont("comicsans", FONT_SIZE)
lost_font = pygame.font.SysFont("comicsans", FONT_SIZE+10)


# Define movable objects
#Define lasers
class Laser:
    def __init__(self, x, y, img):
        self.x = x 
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, y):
        self.y += y

    def off_screen(self):
        return self.y < 0 or self.y > HEIGHT
    
    def collision(self, obj):
        return collide(self, obj)

#Define ships
class Ship:
    #Class constants
    COOLDOWN = 50

    def __init__(self, x, y, health=100):
        self.x, self.y = x,y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0
        
    def draw(self, window): #draw the ship on specified surface
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen():
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def move(self, x, y):  #move the ship relative to current position +/- x,y and prevent from going off screen
        if (self.x + x > 0) and (self.x + x + self.ship_img.get_width() < WIDTH):
            self.x += x
        if (self.y + y > 0) and (self.y + y + self.ship_img.get_height() +10 < HEIGHT):     # leaves room under the ship for healthbar
            self.y += y
        
    def position(self, x, y): #set the current position of the ship
        self.x = x
        self.y = y

    def set_ship_img(self, ship_img, laser_img): #load graphics for the ship
        self.ship_img = ship_img
        self.laser_img = laser_img

    # Shoot the laser    
    def shoot(self, offset=0):  #shoot stuff
        if self.cool_down_counter == 0:
            laser = Laser(self.x + offset, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
    
    # Cooldown timer
    def cooldown(self):
        if self.cool_down_counter > self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter +=1

    
    # Test is the ship is destoryed
    def isDestroyed(self):
        return self.health == 0

    def get_width(self):
        return self.ship_img.get_width()
    
    def get_height(self):
            return self.ship_img.get_height()

    def off_screen(self):
        return self.y < 0 or self.y > HEIGHT

class Player(Ship):

    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen():
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        self.lasers.remove(laser)

    def healthbar(self, window):
        pygame.draw.rect(window, RED, (self.x, self.y+self.ship_img.get_height()+5, self.ship_img.get_width(), 5))                             # put healthbar 10 below player ship
        pygame.draw.rect(window, GREEN, (self.x, self.y+self.ship_img.get_height()+5, self.ship_img.get_width()* self.health / self.max_health, 5))  # Cover red with % health in green

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

class Enemy(Ship):

    #dictionary for colours of ships
    COLOR_MAP = {
                "RED":(RED_SPACE_SHIP, RED_LASER),
                "GREEN":(GREEN_SPACE_SHIP, GREEN_LASER),
                "BLUE":(BLUE_SPACE_SHIP, BLUE_LASER)
                }
    
    #init
    def __init__(self, x, y, colour, health=100):
        super().__init__(x,y,health)
        self.ship_img, self.laser_img = self.COLOR_MAP[colour]  # Set ship images
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

                       

def collide(obj1, obj2):
	offset_x = obj2.x - obj1.x
	offset_y = obj2.y - obj1.y
	return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None #returns a tuple with x, y location of overlap or None
    
def main():
    
    # Collision checking setup
    run = True
    FPS = 60 #Frames per second
    clock = pygame.time.Clock()

    # Game Play Variables
    level = 0
    lives = 5
    lost = False
    lost_timer = 0
    velocity = 300
    player_velocity = velocity // FPS #adjust velocity for variable FPS
    
    enemies = [] #will hold enemies
    enemy_velocity = 60 // FPS
    wave_length = 0 #number of enemies per level
    laser_velocity = 120 // FPS

    
    # Create ship objects
    player_ship = Player(300, 600)
    


    def redraw_window():

        #Cover previous screen
        WINDOW.blit(BG, (0,0))

        # Print user info
        level_label=main_font.render(f"Level: {level}", ANTIALIAS, WHITE)
        lives_label=main_font.render(f"Lives: {lives}", ANTIALIAS, WHITE)

        WINDOW.blit(level_label, (10,10))
        WINDOW.blit(lives_label,(WIDTH-10-lives_label.get_width(),10))
        
        # Check for lost condition
        if lost:
            gameover_label=lost_font.render("GAME OVER MAN!", ANTIALIAS, WHITE)
            WINDOW.blit(gameover_label, ((WIDTH-gameover_label.get_width())//2, HEIGHT//2 + gameover_label.get_height()//2))

        #draw all enemies
        for enemy in enemies: 
            enemy.draw(WINDOW)
        
        #draw player ship
        player_ship.draw(WINDOW)

        #Update Surface
        pygame.display.update()

    while run:

        #draw window
        redraw_window()

        if lost:
            lost_timer += 1
            if lost_timer > FPS*5:# 5 seconds
                lost_timer=0
                lost = False
                break
            else:
                continue

        
        #wait for tick
        clock.tick(FPS)

        # New level game variable update
        if len(enemies) == 0:  
            level += 1
            wave_length += 5
            enemy_velocity += level // 2
            laser_velocity += level // 2
            for i in range(wave_length):
                enemies.append(Enemy(random.randrange(50, WIDTH-50), random.randrange(-1500, -50), random.choice(("RED", "BLUE", "GREEN"))))

        #Move enemy ships
        for enemy in enemies:
            enemy.move(enemy_velocity)
            enemy.move_lasers(laser_velocity, player_ship)  # move and check for collision

            if random.randrange(0,4*FPS) == 1:              # Try to shoot.
                offset = -50 + (enemy.get_width()/2)
                enemy.shoot(offset)

            if collide(enemy, player_ship):                 # Check for ship to ship collision
                enemies.remove(enemy)
                player_ship.health -= 20
            elif enemy.y +enemy.get_height() > HEIGHT:        # Check for enemy making it to bottom of sceen
                lives -= 1
                enemies.remove(enemy)



        # Move player ship 
        # Check key presses and move    
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_ship.move(player_velocity, 0)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_ship.move(-player_velocity, 0)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player_ship.move(0, -player_velocity)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player_ship.move(0, player_velocity)
        if keys[pygame.K_SPACE]:
            player_ship.shoot()

         # Check for losing condition
        if lives <= 0 or player_ship.health <= 0:
            lost = True
        # Check for user inputs(Check for QUIT)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Move Player lasers after moving ship and check if we hit an enemy
        player_ship.move_lasers(-laser_velocity, enemies)
#start game       
main()

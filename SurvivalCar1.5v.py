import pygame
import random
import time
pygame.init()

width = 800
height = 600

score = 0

center = width//2

black = (0, 0, 0)
red = (255, 0, 0)
orange = (255, 165, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
light_blue = (135, 206, 235)
blue = (0, 0, 255)
purple = (138, 43, 226)
white = (255, 255, 255)
dark_green = (34, 139, 34)

colors = [red, orange, yellow, green, light_blue, blue, purple]
car_color = random.choice(colors)



screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Dangerous Highway")

class player_car(pygame.sprite.Sprite):
    def __init__(self, x, y, car_width, car_height):
        super().__init__()
        self.image = pygame.Surface((car_width, car_height))
        self.image.fill(red)
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.player_speed = 10
    def update(self):
        screen_rect = pygame.Rect(0, 0, width, height)
        self.rect.clamp_ip(screen_rect)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rect.x -= self.player_speed
        if keys[pygame.K_d]:
            self.rect.x += self.player_speed
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.player_speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.player_speed

class enemy_car(pygame.sprite.Sprite):
    def __init__(self, x, y, car_width, car_height):
        super().__init__()
        self.image = pygame.Surface((car_width, car_height))
        self.color = random.choice(colors)
        self.image.fill(self.color)
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.speed = 25
        self.score = 0
    def update(self):
        global score
        if self.rect.top >= height:
            score += 1
            enemy_group.empty()
            self.respawn()
            

        self.rect.y += self.speed
    def respawn(self):
        self.rect.x = random.randint(0, width - self.rect.width)
        self.rect.y += self.speed
        self.color = random.choice(colors)
        self.image.fill(self.color)
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.rect.x, self.rect.y, self.rect.width, self.rect.height))

class highway_marker(pygame.sprite.Sprite):
    def __init__(self, x, y, marker_width, marker_height, color):
        super().__init__()
        self.image = pygame.Surface((marker_width, marker_height))
        self.image.fill(color)
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.speed = 50
    def update(self):
        if self.rect.top >= height:
            self.respawn(color=white)

        self.rect.y += self.speed 
    def respawn(self, color):
        self.rect.x = width // 2
        self.rect.y = -120
        self.image.fill(color)

class Grass(pygame.sprite.Sprite):
    def __init__(self, x, y, grass_width, grass_height, color):
        super().__init__()
        self.image = pygame.Surface((grass_width, grass_height))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))

player = player_car(x=center, y=height, car_width=70, car_height=100)
player_group = pygame.sprite.Group(player)


grass = Grass(x=0, y=0, grass_width=270, grass_height=height, color=dark_green)
grass_2 = Grass(x=530, y=0, grass_width=290, grass_height=height, color=dark_green)
grass_group = pygame.sprite.Group(grass, grass_2)

highway = highway_marker(x=center, y=-30, marker_width=20, marker_height=100, color=white)
highway_group = pygame.sprite.Group(highway)

lanes = [300, 450]

num_of_cars = 1

enemy_group = pygame.sprite.Group()

running = True
clock = pygame.time.Clock()

spawn_timer = 0 # Start of the spawn timer
spawn_delay = 1000 # 1000 milliseconds = 1 second

all_groups = [grass_group ,highway_group, player_group]

highway_start = 0
highway_speed = 500

game_over = False

# Starts the game loop
while running:
    dt = clock.tick(60)
    spawn_timer += dt
    for event in pygame.event.get():
        #Stops the game loop when player closes the window
        if event.type == pygame.QUIT:
            running = False
    # An event that is helpeful for detecting when a certain key gets pressed


    keys = pygame.key.get_pressed()
    if not game_over:
        screen.fill(black)
        

        hit = pygame.sprite.spritecollide(player, enemy_group,  False)
        grass_hit = pygame.sprite.spritecollide(player, grass_group, False)
        if hit or grass_hit:
            game_over = True
        for group in all_groups:
            group.update()
        enemy_group.update()
        
        if spawn_timer >= spawn_delay:
            spawn_lanes = random.sample(lanes, num_of_cars)
            for lane_x in spawn_lanes:
                enemy = enemy_car(x= lane_x, y=-30, car_width=70, car_height=100)
                enemy_group.add(enemy)
            spawn_timer = 0
    

        for group in all_groups:
            group.draw(screen)
        font = pygame.font.SysFont(None, 50)

        score_text = font.render("Score: "+str(score), True, (white))
        screen.blit(score_text, (width//2 - score_text.get_width()// 2-320,
                           height//2 - score_text.get_height()//2-270))
        for enemy in enemy_group:
                enemy.draw(screen)
    else:
        screen.fill(black)
        font = pygame.font.SysFont(None, 80)
        game_over_text = font.render("Game Over!", True, (white))
        r_text = font.render("Press R to Restart!", True, (white))
        (screen.blit(game_over_text, (width//2 - game_over_text.get_width()// 2,
                           height//2 - game_over_text.get_height()//2-90)))
        screen.blit(r_text, (width//2 - r_text.get_width()// 2,
                           height//2 - r_text.get_height()//2-30))
        if keys[pygame.K_r]:
            game_over = False
            score = 0
            player.rect.x = center
            enemy_group.empty()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
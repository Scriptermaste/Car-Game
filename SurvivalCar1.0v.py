import pygame
import random
import time
pygame.init()

width = 800
height = 600

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

colors = [red, orange, yellow, green, light_blue, blue, purple]
car_color = random.choice(colors)

def flip_through_colors(color):
        return color

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

class enemy_car(pygame.sprite.Sprite):
    def __init__(self, x, y, car_width, car_height):
        super().__init__()
        self.image = pygame.Surface((car_width, car_height))
        self.color = random.choice(colors)
        self.image.fill(self.color)
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.speed = 25
    def update(self):
        if self.rect.top > height:
            self.respawn()
            

        self.rect.y += self.speed
    def respawn(self):
        self.rect.x = random.randint(0, width - self.rect.width)
        self.rect.y += self.speed
        self.color = random.choice(colors)
        self.image.fill(self.color)
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.rect.x, self.rect.y, self.rect.width, self.rect.height))


player = player_car(x=center, y=height, car_width=70, car_height=100)
player_group = pygame.sprite.Group(player)

lanes = [100, 200, 300, 400, 500, 600]

num_of_cars = 2

enemy_group = pygame.sprite.Group()

running = True
clock = pygame.time.Clock()

spawn_timer = 0 # Start of the spawn timer
spawn_delay = 1000 # 1000 milliseconds = 1 second

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
        hit = pygame.sprite.spritecollide(player, enemy_group, False)
        if hit:
            game_over = True
        player_group.update()
        enemy_group.update()

        if spawn_timer >= spawn_delay:
            spawn_lanes = random.sample(lanes, num_of_cars)
            for lane_x in spawn_lanes:
                enemy = enemy_car(x= lane_x, y=-120, car_width=70, car_height=100)
                enemy_group.add(enemy)
            spawn_timer = 0
                
        screen.fill(black)


        player_group.draw(screen)
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
            enemy_group.empty()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
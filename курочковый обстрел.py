import pygame
import random
import sys
import os

# Инициализация Pygame
pygame.init()

# Размеры экрана
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ловец яиц")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)

# Игровые переменные
basket_width = 100
basket_height = 80
basket_x = WIDTH // 2 - basket_width // 2
basket_y = HEIGHT - basket_height - 10
basket_speed = 8

egg_radius = 20  # Размер яйца
eggs = []
egg_speed = 3
missed_eggs = 0
max_missed_eggs = 3
score = 0

#фоточки
background_image = pygame.image.load("fon.jpg")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

basket_image = pygame.image.load("gde_egs.png").convert_alpha()
basket_image = pygame.transform.scale(basket_image, (basket_width, basket_height))

egg_image = pygame.image.load("boll.png").convert_alpha()
egg_width = egg_radius * 2 
egg_height = egg_radius * 2 
egg_image = pygame.transform.scale(egg_image, (egg_width, egg_height))

#музычка
catch_sound = pygame.mixer.Sound("lovit.wav")
miss_sound = pygame.mixer.Sound("end.wav")
game_over_sound = pygame.mixer.Sound("nelovit.wav")
    
# Таймер для создания новых яиц
egg_timer = 0
egg_interval = 60

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Функция для создания нового яйца
def create_egg():
    x = random.randint(egg_radius, WIDTH - egg_radius)
    y = -egg_radius
    dx = random.uniform(-1.5, 1.5)
    return [x, y, dx]

# самое важное
running = True
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and basket_x > 0:
            basket_x -= basket_speed
        if keys[pygame.K_RIGHT] and basket_x < WIDTH - basket_width:
            basket_x += basket_speed
        
        egg_timer += 1
        if egg_timer >= egg_interval:
            eggs.append(create_egg())
            egg_timer = 0
            egg_interval = random.randint(30, 90)
        
        for egg in eggs[:]:
            egg[0] += egg[2]
            egg[1] += egg_speed
            
            if egg[0] < egg_radius:
                egg[0] = egg_radius
                egg[2] *= -1
            elif egg[0] > WIDTH - egg_radius:
                egg[0] = WIDTH - egg_radius
                egg[2] *= -1
            
            if (egg[1] + egg_radius > basket_y and 
                egg[0] > basket_x and 
                egg[0] < basket_x + basket_width):
                eggs.remove(egg)
                score += 1
                catch_sound.play()
            
            elif egg[1] > HEIGHT:
                eggs.remove(egg)
                missed_eggs += 1
                game_over_sound.play()
                
                if missed_eggs >= max_missed_eggs:
                    game_over = True
                    miss_sound.play()
    
    # Отрисовка фона
    if background_image:
        screen.blit(background_image, (0, 0))
    else:
        screen.fill(WHITE)
    
    # Отрисовка корзины
    screen.blit(basket_image, (basket_x, basket_y))
    
    # Отрисовка яиц
    for egg in eggs:
         screen.blit(egg_image, (egg[0] - egg_radius, egg[1] - egg_radius))  
        
    
    score_text = font.render(f"Счет: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    
    missed_text = font.render(f"Пропущено: {missed_eggs}/{max_missed_eggs}", True, BLACK)
    screen.blit(missed_text, (10, 50))
    
    if game_over:

        game_over_text = font.render("ИГРА ОКОНЧЕНА!", True, (255, 255, 255))
        screen.blit(game_over_text, (WIDTH//2 - 100, HEIGHT//2))
        
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
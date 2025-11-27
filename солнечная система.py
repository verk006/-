import pygame
import math
import random

pygame.init()
pygame.mixer.init()

# на фон музыка такая вот таинственная пусть будет
try:
    pygame.mixer.music.load("cosmos.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
except:
    print("Фоновая музыка не найдена")

# БАБАХ
try:
    explosion_sound = pygame.mixer.Sound("babax.mp3")
except:
    explosion_sound = None

screen = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)
pygame.display.set_caption("Солнечная система")
WIDTH, HEIGHT = 1200, 800
cx = WIDTH // 2
cy = HEIGHT // 2   
FPS = 60
clock = pygame.time.Clock()

class CelestialBody:
    def __init__(self, screen, radius, orbit_radius, color=None, orbital_speed=0, angle=0, 
                 image_path=None, name=""):
        self.screen = screen
        self.radius = radius
        self.orbit_radius = orbit_radius
        self.color = color
        self.orbital_speed = orbital_speed
        self.angle = angle
        self.name = name
        self.x = 0
        self.y = 0
        self.image = None
        
        if image_path:
            try:
                self.image = pygame.image.load(image_path).convert_alpha()
                self.image = pygame.transform.scale(self.image, (radius*2, radius*2))
            except:
                print(f"изображение не загрузилось это грустно: {image_path}")
                self.image = None

    def update(self, dt):
        global cx, cy
        self.angle += self.orbital_speed * dt
        self.x = cx + self.orbit_radius * math.cos(self.angle)
        self.y = cy + self.orbit_radius * math.sin(self.angle)

    def draw(self):
        if self.image:
            rect = self.image.get_rect(center=(int(self.x), int(self.y)))
            self.screen.blit(self.image, rect)
        else:
            pygame.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), self.radius)

class Moon(CelestialBody):
    def __init__(self, screen, radius, orbit_radius, parent, color=None, orbital_speed=0, 
                 angle=0, image_path=None, name=""):
        super().__init__(screen, radius, orbit_radius, color, orbital_speed, angle, 
                        image_path, name)
        self.parent = parent

    def update(self, dt):
        self.angle += self.orbital_speed * dt
        self.x = self.parent.x + self.orbit_radius * math.cos(self.angle)
        self.y = self.parent.y + self.orbit_radius * math.sin(self.angle)

class Asteroid:
    def __init__(self, screen, min_radius, max_radius, min_orbit, max_orbit):
        self.screen = screen
        self.radius = random.uniform(min_radius, max_radius)
        self.orbit_radius = random.uniform(min_orbit, max_orbit)
        self.angle = random.uniform(0, 2 * math.pi)
        self.orbital_speed = random.uniform(0.1, 0.3)
        self.color = (150, 150, 150)
        self.x = 0
        self.y = 0

    def update(self, dt):
        global cx, cy
        self.angle += self.orbital_speed * dt
        self.x = cx + self.orbit_radius * math.cos(self.angle)
        self.y = cy + self.orbit_radius * math.sin(self.angle)

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), int(self.radius))

class Comet:
    def __init__(self, screen):
        self.screen = screen
        self.radius = 8
        self.angle = random.uniform(0, 2 * math.pi)
        self.a = random.uniform(400, 600)
        self.e = random.uniform(0.7, 0.9)
        self.b = self.a * math.sqrt(1 - self.e**2)
        self.orbital_speed = random.uniform(0.05, 0.1)
        self.color = (200, 200, 255)
        self.tail_length = 20
        self.tail_particles = []
        self.crashing = False
        self.speed_multiplier = 1.0
        self.active = True
        
        #координаты
        self.x = cx + self.a * math.cos(self.angle)
        self.y = cy + self.b * math.sin(self.angle)
        
        for _ in range(self.tail_length):
            self.tail_particles.append((self.x, self.y))

    def update(self, dt, earth=None):
        global cx, cy
        
        if not self.active:
            return False
            
        if self.crashing and earth:
            dx = earth.x - self.x
            dy = earth.y - self.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance > 10:
                dx /= distance
                dy /= distance
                self.x += dx * self.speed_multiplier * 5
                self.y += dy * self.speed_multiplier * 5
                self.speed_multiplier += 0.05
            else:
                self.active = False
                return True
        else:
            self.angle += self.orbital_speed * dt
            self.x = cx + self.a * math.cos(self.angle)
            self.y = cy + self.b * math.sin(self.angle)
        
        # хвостик
        self.tail_particles.insert(0, (self.x, self.y))
        if len(self.tail_particles) > self.tail_length:
            self.tail_particles.pop()
            
        return False

    def draw(self):
        if not self.active:
            return
            
        # красивый хвостик рисуем
        for i, (x, y) in enumerate(self.tail_particles):
            alpha = 255 * (1 - i / len(self.tail_particles))
            radius = self.radius * (1 - i / len(self.tail_particles))
            color = (200, 200, 255, int(alpha))
            pygame.draw.circle(self.screen, color, (int(x), int(y)), int(radius))
        
        # сама комета без хвостика
        pygame.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), self.radius)
        
        if self.crashing:
            pygame.draw.circle(self.screen, (255, 0, 0), (int(self.x), int(self.y)), self.radius + 3, 2)

    def is_clicked(self, pos):
        if not self.active:
            return False
        x, y = pos
        distance = math.sqrt((x - self.x)**2 + (y - self.y)**2)
        return distance <= self.radius

    def start_crash(self, earth):
        if self.active and not self.crashing:
            self.crashing = True

# планеты и солнышко
sun_color = (255, 255, 0)
sun_radius = 40

try:
    sun_image = pygame.image.load("sun.png").convert_alpha()
    sun_image = pygame.transform.scale(sun_image, (sun_radius*2, sun_radius*2))
except:
    sun_image = None
    print("все солнца нет вместо него круг")


mercury = CelestialBody(screen, 8, 100, (200, 200, 200), 4.1, random.uniform(0, 6.28), 
                       "merk.png", "Меркурий")
venus = CelestialBody(screen, 12, 150, (255, 200, 100), 1.6, random.uniform(0, 6.28), 
                     "venera.png", "Венера")
earth = CelestialBody(screen, 13, 200, (100, 100, 255), 1.0, random.uniform(0, 6.28), 
                     "zemla.png", "Земля")
mars = CelestialBody(screen, 10, 250, (255, 100, 80), 0.5, random.uniform(0, 6.28), 
                    "mars.png", "Марс")
jupiter = CelestialBody(screen, 30, 350, (255, 200, 150), 0.08, random.uniform(0, 6.28), 
                       "upiter.png", "Юпитер")
saturn = CelestialBody(screen, 25, 450, (255, 220, 180), 0.03, random.uniform(0, 6.28), 
                      "saturn.png", "Сатурн")
uranus = CelestialBody(screen, 18, 520, (200, 230, 255), 0.01, random.uniform(0, 6.28), 
                      "uran.png", "Уран")
neptune = CelestialBody(screen, 17, 580, (80, 80, 255), 0.006, random.uniform(0, 6.28), 
                       "nept.png", "Нептун")

moon = Moon(screen, 4, 25, earth, (200, 200, 200), 5.0, random.uniform(0, 6.28), 
           "luna.png", "Луна")

asteroids = [Asteroid(screen, 1, 4, 280, 320) for _ in range(100)]

comet = Comet(screen)

planets = [mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

font = pygame.font.Font(None, 24)
big_font = pygame.font.Font(None, 72)

running = True
paused = False
show_names = True
dinosaur_message = False
dinosaur_timer = 0
MESSAGE_DURATION = 5
comet_used = False  # чтобы миллиард раз не убивать динозавров

while running:
    dt = clock.tick(FPS) / 1000.0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            cx = WIDTH // 2
            cy = HEIGHT // 2
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_n:
                show_names = not show_names
            elif event.key == pygame.K_m:
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not comet_used and comet.is_clicked(event.pos):
                comet.start_crash(earth)

    if not paused:
        for planet in planets:
            planet.update(dt)
        moon.update(dt)
        for asteroid in asteroids:
            asteroid.update(dt)
        
        # проверяем всякое
        if comet.active:
            if comet.update(dt, earth):
                # комета врезалась в землю
                dinosaur_message = True
                dinosaur_timer = MESSAGE_DURATION
                comet_used = True
                if explosion_sound:
                    explosion_sound.play()
        
        # сообщение
        if dinosaur_message:
            dinosaur_timer -= dt
            if dinosaur_timer <= 0:
                dinosaur_message = False

    # все рисуем
    screen.fill((0, 0, 0))
    
    # орбиты рисуем
    for planet in planets:
        pygame.draw.circle(screen, (50, 50, 50), (cx, cy), planet.orbit_radius, 1)
    
    # астероидыыыы точнее пояс
    pygame.draw.circle(screen, (70, 70, 70), (cx, cy), 300, 1)
    
    # а вот тут астероиды
    for asteroid in asteroids:
        asteroid.draw()
    
    # комета
    if comet.active:
        comet.draw()
    
    # солнышко
    if sun_image:
      sun_rect = sun_image.get_rect(center=(cx, cy))
      screen.blit(sun_image, sun_rect)
    else:
      pygame.draw.circle(screen, sun_color, (cx, cy), sun_radius)
    
    # планетки рисуем
    for planet in planets:
        planet.draw()
    
    # и луну нарисуем
    moon.draw()
    
    # названия планет
    if show_names:
        for planet in planets:
            name_text = font.render(planet.name, True, (255, 255, 255))
            screen.blit(name_text, (planet.x - name_text.get_width() // 2, planet.y - planet.radius - 20))
        
        moon_text = font.render(moon.name, True, (255, 255, 255))
        screen.blit(moon_text, (moon.x - moon_text.get_width() // 2, moon.y - moon.radius - 15))
    
    # АААА ДИНОЗАВРЫ О НЕТ
    if dinosaur_message:
        message_text = big_font.render("ВЫ УБИЛИ ДИНОЗАВРОВ!!!", True, (255, 0, 0))
        screen.blit(message_text, (WIDTH//2 - message_text.get_width()//2, HEIGHT//2 - 50))
        
        if int(dinosaur_timer * 10) % 2 == 0:
            subtitle_text = font.render("а все только раз взрывать можно", True, (255, 255, 255))
            screen.blit(subtitle_text, (WIDTH//2 - subtitle_text.get_width()//2, HEIGHT//2 + 30))
    
    #инструкция
    instructions = [
        "Управление:",
        "Пробел - пауза",
        "N - показать/скрыть названия",
        "M - вкл/выкл музыку"]
    
    for i, text in enumerate(instructions):
        instruction_text = font.render(text, True, (200, 200, 200))
        screen.blit(instruction_text, (10, 10 + i * 25))
    
    # пауза
    if paused:
        pause_text = font.render("ПАУЗА", True, (255, 0, 0))
        screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, 20))

    pygame.display.flip()

pygame.quit()
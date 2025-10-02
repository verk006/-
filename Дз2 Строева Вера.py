import pygame
pygame.init()
font = pygame.font.SysFont(None, 24)

screen = pygame.display.set_mode((700, 600))
pygame.display.set_caption("хобабоба")

running = True 
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False



    
    screen.fill((2,214,255))
    pygame.draw.rect(screen, (29,232,28), (0,300, 1000, 300))  

    pygame.draw.circle(screen, (235,201,161), (200, 150), 50)
    pygame.draw.ellipse(screen, (137,137,137), (150, 100, 100, 50))
    pygame.draw.ellipse(screen, (137,137,137), (140, 200, 120, 200))
    pygame.draw.line(screen, (0, 0, 0), (157, 231), (86, 329), 3) 
    pygame.draw.line(screen, (0, 0, 0), (238, 225), (319, 325), 3) 
    pygame.draw.line(screen, (0, 0, 0), (173, 387), (138, 526), 3)
    pygame.draw.line(screen, (0, 0, 0), (138, 526),(109,525), 3) 
    pygame.draw.line(screen, (0, 0, 0), (228, 388), (254, 524), 3) 
    pygame.draw.line(screen, (0, 0, 0), (254, 524), (281, 522), 3) 

    pygame.draw.polygon(screen, (236,191,51), [(92, 328), (45, 265), (99, 250)]) 
    pygame.draw.circle(screen, (83,50,18), (54, 248), 20)
    pygame.draw.circle(screen, (245,52,7), (80,237), 20)
    pygame.draw.circle(screen, (255,255,255), (56,211), 20)

    pygame.draw.ellipse(screen, (104,68,21), (380, 70, 160, 200))
    pygame.draw.polygon(screen, (245,52,7), [(456, 184), (382, 391), (537, 392)]) 
    pygame.draw.circle(screen, (235,201,161), (458, 146), 50)
    pygame.draw.rect(screen, (104,68,21), (410,95, 100, 33))  
    pygame.draw.line(screen, (0, 0, 0), (436, 237), (319, 325), 3) 
    pygame.draw.line(screen, (0, 0, 0), (477, 237), (531, 295), 3)
    pygame.draw.line(screen, (0, 0, 0), (586, 254), (531, 295), 3)
    pygame.draw.line(screen, (0, 0, 0), (433, 394), (429, 519), 3)
    pygame.draw.line(screen, (0, 0, 0), (394, 518), (429, 519), 3)
    pygame.draw.line(screen, (0, 0, 0), (473, 394), (474, 519), 3)
    pygame.draw.line(screen, (0, 0, 0), (510, 516), (474, 519), 3)

    pygame.draw.line(screen, (0, 0, 0), (587, 313), (594, 213), 3)
    pygame.draw.polygon(screen, (245,52,7), [(594, 213), (572, 165), (619, 168)]) 
    pygame.draw.circle(screen, (245,52,7), (585,153), 18)
    pygame.draw.circle(screen, (245,52,7), (610,155), 18)

    mx, my = pygame.mouse.get_pos()
    text = font.render(f"x: {mx}, y: {my}", True, (0, 0, 0))
    screen.blit(text, (10, 10))
    pygame.display.flip()

pygame.quit()
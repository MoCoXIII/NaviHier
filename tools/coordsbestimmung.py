import pygame
import math

pygame.init()

screen = pygame.display.set_mode((1500, 1000))

plan = pygame.image.load(r"C:\Bell\NaviHier\Test Gebäudeplan\Gebäudeplan.png")
plan = pygame.transform.scale(plan, (1500, 1000))

x1 = 0
y1 = 0
x2 = 0
y2 = 0
while_running_square = True
while_running_circle = True
while_running_waypoint = True

scale = 1000/plan.get_width()

print("press s for square, c for circle, w for waypoint\nto stop coords input press escape")

running = True
while running:

    screen.blit(plan, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            print("put in first square coord")
            while while_running_square:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x1, y1 = pygame.mouse.get_pos()
                        print("put in second square coord")
                        while while_running_square:
                            for event in pygame.event.get():
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    x2, y2 = pygame.mouse.get_pos()
                                    print(x1/scale, y1/scale, x2/scale, y2/scale)
                                    while_running_square = False
                                    break
                                elif event.type == pygame.QUIT:
                                    running = False
                                    while_running_square = False
                                    break
                                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                                    print("stopped coords input")
                                    while_running_square = False
                                    break
                    elif event.type == pygame.QUIT:
                        running = False
                        while_running_square = False
                        break
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        print("stopped coords input")
                        while_running_square = False
                        break

                    elif event.type == pygame.MOUSEBUTTONUP:
                        continue
        
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
            print("put in the coords of the location of the circle")
            while while_running_circle:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x1, y1 = pygame.mouse.get_pos()
                        print("put in another coord to define the radius of the circle")
                        while while_running_circle:
                            for event in pygame.event.get():
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    x2, y2 = pygame.mouse.get_pos()
                                    print(x1/scale, y1/scale, math.dist((x1/scale, y1/scale), (x2/scale, y2/scale)))
                                    while_running_circle = False
                                    break
                                elif event.type == pygame.QUIT:
                                    running = False
                                    while_running_circle = False
                                    break
                                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                                    print("stopped coords input")
                                    while_running_circle = False
                                    break
                    elif event.type == pygame.QUIT:
                        running = False
                        while_running_circle = False
                        break
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        print("stopped coords input")
                        while_running_circle = False
                        break
                
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
            print("put in the coords of the location of the waypoint")
            while while_running_waypoint:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x1, y1 = pygame.mouse.get_pos()
                        print(x1/scale, y1/scale)
                        while_running_waypoint = False
                        break
                    elif event.type == pygame.QUIT:
                        running = False
                        while_running_waypoint = False
                        break
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        print("stopped coords input")
                        while_running_waypoint = False
                        break
        
        while_running_square = True
        while_running_circle = True
        while_running_waypoint = True

    
    pygame.display.flip()

pygame.quit()
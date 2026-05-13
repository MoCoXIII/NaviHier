# coordsbestimmung_überarbeitet
# Theo Glase
# 12.05.2026

import pygame
import easypygamewidgets as epw
import ctypes
from coordsbestimmung_Funktionen import square, circle, waypoint, polygon, plan_selection, text_display, question_display

# initialisieren von Pygame
pygame.init()

# erstellen der Positionsvariablen für den square Raum // s_x1, s_y1: erste Koordinate (obere linke Ecke); s_x2, s_y2: zweite Koordinate (untere rechte Ecke)
s_x1 = 0
s_y1 = 0
s_x2 = 0
s_y2 = 0

# erstellen der Positionsvariablen für den circle Raum // c_x, c_y: Position des Mittelpunktes, radius_pos_x, radius_pos_y: Position des Radiuspunktes
c_x = 0
c_y = 0
radius_pos_x = 0
radius_pos_y = 0

# erstellen der Positionsvariablen des Wegpunktes // w_x, w_y: Koordinaten
w_x = 0
w_y = 0

# erstellen der temporären positionsvariable
pos = 0

# erstellen der Liste zum speichern der Koordinaten des polygon Raumes
s_coords = []
p_coords = []
w_coords = []

# erstellen der Variable zum speichern des Ausgewählten Inputs // 1: square; 2: Polygon; 3: waypoint
shape = 0

# erstellend der Variablen zum Abbrechen der coordseingabe
s_coords_count = 0
p_coords_count = 0
w_coords_count = 0

# erstellen der Variable zum möglichen Speichern des Raumes
s_submit = False
p_submit = False
w_submit = False

# erstellen der Variable zum Anzeigen der Info
info_shown = False

plan_path = plan_selection()
plan = pygame.image.load(fr"{plan_path}")
plan_w, plan_h = plan.get_size()
screen = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h), pygame.RESIZABLE)
pygame.display.set_caption("Raumeditor")
epw.link_pygame_window(screen)
hwmd = ctypes.windll.user32.FindWindowW(None, "Raumeditor")             # hwmd (handle window): Window ID      # windll.user32: angeben der Datei: "user32.dll"; FindWindowW: Funktion zum finden eines Fensters
ctypes.windll.user32.ShowWindow(hwmd, 3)                                # ShowWindow: Funktion zum ändern des Zustandes eines Fensters // 0 = verstecken, 1 = normal anzeigen, 2 = minimieren, 3 = maximieren, 6 = minimieren in die Taskleiste
pygame.event.pump()                                                     # update von Pygame

screen_info = pygame.display.Info()
screen_w, screen_h = screen_info.current_w, screen_info.current_h
pygame.display.set_mode((screen_w, screen_h))
faktor = min(screen_w/plan_w, screen_h/plan_h, 1.0)
new_w, new_h = int(plan_w*faktor), int(plan_h*faktor)
plan = pygame.transform.scale(plan, (new_w, new_h))
plan_start_x = (screen_w - new_w) // 2
plan_start_y = (screen_h - new_h) // 2
scale = 1000 / int(plan_w*faktor)

# plazieren des Plans; festlegen der Variable des Plans
plan_widget = epw.Surface(plan).place(x = plan_start_x, y = plan_start_y)

running = True
while running:

    # färben des Hintergrunds
    screen.fill((47, 91, 235))

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if shape == 1:
                if s_coords_count < 2:
                    pos == pygame.mouse.get_pos()
                    s_x1, s_y1 = pos[0] - plan_start_x, pos[1] - plan_start_y
                    s_coords.append(s_x1 / scale, s_y1 / scale)
                    s_coords_count += 1
                    if s_coords_count == 2:
                        s_submit = True
                else:
                    print("Platzhalter")

            elif shape == 2:
                pos == pygame.mouse.get_pos()
                p_x, p_y = pos[0] - plan_start_x, pos[1] - plan_start_y
                p_coords.append(p_x / scale, p_y / scale)
                p_submit = True
            
            elif shape == 3:
                if w_coords_count == 0:
                    pos == pygame.mouse.get_pos()
                    w_x, w_y = pos[0] - plan_start_x, pos[1] - plan_start_y
                    w_coords.append(w_x / scale, w_y / scale)
                    if w_coords_count == 1:
                        w_submit = True
                else:
                    print("Platzhalter")
        
        elif event. type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
            if shape == 1 and s_coords_count > 0:
                s_coords.pop()
                s_coords.pop()
                s_coords_count -= 1
                if s_coords_count == 0:
                    s_submit = False
            else:
                print("Platzhalter")
            
            if shape == 2 and p_coords_count > 0:
                p_coords.pop()
                p_coords.pop()
                p_coords_count -= 1
                if p_coords_count == 0:
                    p_submit = False
            else:
                print("Platzhalter")
            
            if shape == 3 and w_coords_count == 1:
                w_coords.pop()
                w_coords.pop()
                w_coords_count -= 1
                if w_coords_count == 0:
                    w_submit = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN and event.key == pygame.K_ESCAPE and shape == 1 or shape == 2 or shape == 3:
            s_coords.clear()
            p_coords.clear()
            w_coords.clear()
            s_coords_count = 0
            p_coords_count = 0
            w_coords_count = 0

        elif event.type == pygame.QUIT:
            running = False
    
        epw.handle_event(event)
    epw.handle_special_events()
    epw.flip()

pygame.quit()
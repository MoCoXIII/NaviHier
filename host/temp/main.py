# coordsbestimmung_überarbeitet
# Theo Glase
# 04.06.2026

import pygame
import easypygamewidgets as epw
from host.json_manager import plan_selection
from widgets import id_answer_list, update_ui, window_create, plan_create, get_widget_dic

# initialisieren von Pygame
pygame.init()

# Planvariablen
plan_start_x = 0
plan_start_y = 0

# erstellen der Positionsvariablen für den square Raum // s_x1, s_y1: erste Koordinate (obere linke Ecke); s_x2, s_y2: zweite Koordinate (untere rechte Ecke)
s_x = 0
s_y = 0

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

screen = window_create()
plan, plan_w, plan_h, plan_path = plan_create()
widget_dic = get_widget_dic(plan)
update_ui(widget_dic, plan, plan_w, plan_h)

running = True
while running:
    # färben des Hintergrunds
    screen.fill((30, 30, 30))

    if s_submit == True or p_submit == True or w_submit == True:
        widget_dic["4_0_button_createsub"].config(state = "enabled")
    else:
        widget_dic["4_0_button_createsub"].config(state = "disabled")

    if shape == 0:
        widget_dic["4_0_button_createcan"].config(state = "disabled")
    else:
        widget_dic["4_0_button_createcan"].config(state = "enabled")
    
    if id_answer_list == []:
        widget_dic["4_1_button_finishsub"].config(state = "disabled")
    else:
        widget_dic["4_1_button_finishsub"].config(state = "enabled")

    for event in pygame.event.get():
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            scale = update_ui(widget_dic, plan, plan_w, plan_h)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if shape == 1:
                pos = pygame.mouse.get_pos()
                s_x, s_y = int((pos[0] - plan_start_x) / scale), int((pos[1] - plan_start_y) / scale)
                if s_coords_count < 2:
                    if s_x >= 0 and s_x <= plan_w and s_y >= 0 and s_y <= plan_h:
                        s_coords.append(s_x)
                        s_coords.append(s_y)
                        s_coords_count += 1
                        widget_dic["4_01_label_statuscontent"].config(text = f"Die Koordinate {s_x}, {s_y} wurde hinzugefügt.")
                    else:
                        pass
                    if s_coords_count >= 2:
                        s_submit = True
                elif s_x >= 0 and s_x <= plan_w and s_y >= 0 and s_y <= plan_h:
                    widget_dic["4_01_label_statuscontent"].config(text = f"Es wurden bereits zwei Koordinaten hinzugefügt. [{s_coords[0]}, {s_coords[1]}]; [{s_coords[2]}, {s_coords[3]}]")
                else:
                    pass

            elif shape == 2:
                pos = pygame.mouse.get_pos()
                p_x, p_y = int((pos[0] - plan_start_x) / scale), int((pos[1] - plan_start_y) / scale)
                if p_x >= 0 and p_x <= plan_w and p_y >= 0 and p_y <= plan_h:
                    p_coords.append(p_x)
                    p_coords.append(p_y)
                    widget_dic["4_01_label_statuscontent"].config(text = f"Die Koordinate {p_x}, {p_y} wurde hinzugefügt.")
                    p_coords_count += 1
                    if p_coords_count >= 3:
                        p_submit = True

            elif shape == 3:
                pos = pygame.mouse.get_pos()
                w_x, w_y = int((pos[0] - plan_start_x) / scale), int((pos[1] - plan_start_y) / scale)
                if w_coords_count == 0 and w_x >= 0 and w_x <= plan_w and w_y >= 0 and w_y <= plan_h:
                    w_coords.append(w_x)
                    w_coords.append(w_y)
                    widget_dic["4_01_label_statuscontent"].config(text = f"Die Koordinate {w_x}, {w_y} wurde hinzugefügt.")
                    if w_coords_count == 1:
                        w_submit = True
                else:
                    pass
        
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
            
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and (shape == 1 or shape == 2 or shape == 3):
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
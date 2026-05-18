# coordsbestimmung_überarbeitet
# Theo Glase
# 18.05.2026

import pygame
import easypygamewidgets as epw
import ctypes
from coordsbestimmung_Funktionen import square, circle, waypoint, polygon, plan_selection, text_display, question_display

# initialisieren von Pygame
pygame.init()

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

# erstellen der Variable zum Anzeigen der Info
info_shown = False

plan_path = plan_selection()
plan = pygame.image.load(fr"{plan_path}")
plan_w, plan_h = plan.get_size()
screen = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h), pygame.RESIZABLE)
pygame.display.set_caption("Raumeditor")
epw.link_pygame_window(screen)
hwnd = pygame.display.get_wm_info()["window"]                                                                           # hwnd (handle window): Window ID      
ctypes.windll.user32.ShowWindow(hwnd, 3)                                                                                # ShowWindow: Funktion zum ändern des Zustandes eines Fensters // 0 = verstecken, 1 = normal anzeigen, 2 = minimieren, 3 = maximieren, 6 = minimieren in die Taskleiste
appereance_mode = ctypes.c_int(2)                                                                                       # appereance_mode: Variable zum Speichern des Anzeigemodus der Titelleiste // 0 = Light Mode, 1 = Dark Mode, 2 = Systemstandard
ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, ctypes.byref(appereance_mode), ctypes.sizeof(appereance_mode))     # DwmSetWindowAttribute: Funktion zum Ändern des Anzeigemodus der Titelleiste       # ctypes.byref: Funktion zu Bestimmen des Speicherorts der Variable; ctypes.sizeof: Funktion zum Bestimmen des Speicherplatzes der Variable (int: 4)
pygame.event.pump()                                                                                                     # update von Pygame

info_icon = pygame.image.load("assets/info_icon.png")

def update_ui(plan):
    screen_info = pygame.display.Info()
    screen_w, screen_h = screen_info.current_w, screen_info.current_h
    pygame.display.set_mode((screen_w, screen_h), pygame.RESIZABLE)
    faktor = min(screen_w/plan_w, screen_h/plan_h, 1.0)
    new_w, new_h = int(plan_w*faktor), int(plan_h*faktor)
    plan = pygame.transform.scale(plan, (new_w, new_h))
    plan_start_x = (screen_w - new_w) // 2
    plan_start_y = (screen_h - new_h) // 2
    scale = 1000 / int(plan_w*faktor)
    # Plan und Überschrift
    widget_dic["plan"].config(surface = plan)
    widget_dic["plan"].place(x = plan_start_x, y = plan_start_y)
    widget_dic["title"].place(x = plan_start_x + new_w // 2 - widget_dic["title"].width // 2, y = plan_start_y // 2 - widget_dic["title"].height // 2)
    # Status
    widget_dic["status_title_label"].place(x = plan_start_x, y = screen_h - plan_start_y // 2 - widget_dic["status_title_label"].height)
    widget_dic["status_label"].place(x = plan_start_x, y = screen_h - plan_start_y // 2)
    widget_dic["status_label"].config(min_width = 2 * new_w // 3)
    # Raumtyp
    widget_dic["room_type_label"].place(x = plan_start_x // 2 - widget_dic["room_type_label"].width // 2, y = plan_start_y)
    widget_dic["square_button_label"].place(x = plan_start_x // 4 - widget_dic["square_button_label"].width // 2, y = plan_start_y + new_h // 3 - widget_dic["square_button_label"].height)
    widget_dic["square_button"].place(x = plan_start_x // 4 - widget_dic["square_button_label"].width // 2, y = plan_start_y + new_h // 3)
    widget_dic["polygon_button_label"].place(x = plan_start_x // 4 - widget_dic["square_button_label"].width // 2, y = plan_start_y + new_h // 2 - widget_dic["polygon_button_label"].height)
    widget_dic["polygon_button"].place(x = plan_start_x // 4 - widget_dic["square_button_label"].width // 2, y = plan_start_y + new_h // 2)
    widget_dic["room_type_cancel_button"].place(x = plan_start_x // 4 - widget_dic["square_button_label"].width // 2, y = plan_start_y + 2 * new_h // 3)
    # Info Symbol
    widget_dic["info_icon"].scale(0.05, 0)
    widget_dic["info_icon"].place(x = screen_w - info_icon.get_width() * 0.05 - 20, y = 20)
    return scale

def square_selected():
    global shape, widget_dic
    if shape == 0:
        shape = 1
        widget_dic["status_label"].config(text = "Quadratischer Raumtyp Ausgewählt")

def polygon_selected():
    global shape, widget_dic
    if shape == 0:
        shape = 2
        widget_dic["status_label"].config(text = "Polygonaler Raumtyp Ausgewählt")

def room_type_cancel():
    global shape, widget_dic, s_coords, p_coords, s_coords_count, p_coords_count
    shape = 0
    s_coords.clear()
    p_coords.clear()
    s_coords_count = 0
    p_coords_count = 0
    widget_dic["status_label"].config(text = "Zurücksetzen des Raumtyps")

widget_dic = {
    "plan": epw.Surface(plan),
    "title": epw.Label(text="Raumeditor", font=epw.SysFont(font="Calibri", font_size=65)),
    "status_title_label": epw.Label(text="Status", font=epw.SysFont(font="Calibri", font_size=40, bold = True), alignment_spacing = 0, alignment = "left"),
    "status_label": epw.Label(text="", font=epw.SysFont(font="Calibri", font_size=30),
                                                        alignment = "left",
                                                        active_unpressed_background_color = (50, 50, 50), 
                                                        active_hover_background_color = (50, 50, 50),
                                                        active_pressed_background_color = (50, 50, 50),
                                                        top_left_corner_radius = 15, 
                                                        top_right_corner_radius = 15, 
                                                        bottom_left_corner_radius = 15, 
                                                        bottom_right_corner_radius = 15),
    "room_type_label": epw.Label(text="Raumtyp - / Wegpunktauswahl", font=epw.SysFont(font="Calibri", font_size=40, bold = True)),
    "square_button_label": epw.Label(text="Quadratischer Raum", font=epw.SysFont(font="Calibri", font_size=30), alignment_spacing = 0, alignment = "left"),
    "square_button": epw.Button(text="Auswählen", font=epw.SysFont(font="Calibri", font_size=30), command = square_selected),
    "polygon_button_label": epw.Label(text="Polygon Raum", font=epw.SysFont(font="Calibri", font_size=30), alignment_spacing = 0, alignment = "left"),
    "polygon_button": epw.Button(text="Auswählen", font=epw.SysFont(font="Calibri", font_size=30), command = polygon_selected),
    "room_type_cancel_button": epw.Button(text="Abbrechen", font=epw.SysFont(font="Calibri", font_size=30), command = room_type_cancel),
    "info_icon": epw.Surface(info_icon)
}

update_ui(plan)
running = True
while running:
    # färben des Hintergrunds
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.VIDEORESIZE:
            scale = update_ui(plan)
            plan_start_x = widget_dic["plan"].x
            plan_start_y = widget_dic["plan"].y

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if shape == 1:
                pos = pygame.mouse.get_pos()
                s_x, s_y = int((pos[0] - plan_start_x) / scale), int((pos[1] - plan_start_y) / scale)
                if s_coords_count < 2:
                    if s_x >= 0 and s_x <= plan_w and s_y >= 0 and s_y <= plan_h:
                        s_coords.append(s_x)
                        s_coords.append(s_y)
                        s_coords_count += 1
                        widget_dic["status_label"].config(text = f"Die Koordinate {s_x}, {s_y} wurde hinzugefügt.")
                    else:
                        pass
                    if s_coords_count >= 2:
                        s_submit = True
                elif s_x >= 0 and s_x <= plan_w and s_y >= 0 and s_y <= plan_h:
                    widget_dic["status_label"].config(text = f"Es wurden bereits zwei Koordinaten hinzugefügt. [{s_coords[0]}, {s_coords[1]}]; [{s_coords[2]}, {s_coords[3]}]")
                else:
                    pass

            elif shape == 2:
                pos = pygame.mouse.get_pos()
                p_x, p_y = int((pos[0] - plan_start_x) / scale), int((pos[1] - plan_start_y) / scale)
                if s_x >= 0 and s_x <= plan_w and s_y >= 0 and s_y <= plan_h:
                    p_coords.append(p_x / scale)
                    p_coords.append(p_y / scale)
                    widget_dic["status_label"].config(text = f"Die Koordinate {p_x}, {p_y} wurde hinzugefügt.")
                    p_coords_count += 1
                    if p_coords_count >= 3:
                        p_submit = True

            elif shape == 3:
                if w_coords_count == 0:
                    pos = pygame.mouse.get_pos()
                    w_x, w_y = pos[0] - plan_start_x, pos[1] - plan_start_y
                    w_coords.append(w_x / scale)
                    w_coords.append(w_y / scale)
                    widget_dic["status_label"].config(text = f"Die Koordinate{s_x}, {s_y} wurde hinzugefügt.")
                    if w_coords_count == 1:
                        w_submit = True
                else:
                    widget_dic["status_label"].config(text = f"Es wurde bereits eine Koordinate hinzugefügt. ({w_coords[0]}, {w_coords[1]})")
        
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
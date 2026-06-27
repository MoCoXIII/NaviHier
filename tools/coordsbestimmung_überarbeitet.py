# coordsbestimmung_überarbeitet
# Theo Glase
# 04.06.2026

import pygame
import easypygamewidgets as epw
import ctypes
from coordsbestimmung_Funktionen import square, circle, waypoint, polygon, plan_selection, text_display, question_display

# initialisieren von Pygame
pygame.init()

# Referenzauflösung der UI
ref_w = 2560
ref_h = 1440

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

# erstellen der Variable zum Anzeigen der Info
info_shown = False

# 
id_answer_list = []
name_answer_list = []
prof_answer_list = []
extrainfo_answer_list = []

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

def update_ui(widget_dic):
    global plan_start_x, plan_start_y
    # Generelle Faktorberechnung
    screen_w, screen_h = screen.get_size()
    gen_faktor_w = screen_w / ref_w
    gen_faktor_h = screen_h / ref_h
    # Planberechnung
    max_w = screen_w * 0.40
    max_h = screen_h * 0.50
    plan_faktor = min(max_w / plan_w, max_h / plan_h)
    new_w = int(plan_w * plan_faktor)
    new_h = int(plan_h * plan_faktor)
    widget_dic["plan"].config(surface = plan)
    widget_dic["plan"].place(x = screen_w * 0.30, y = screen_h * 0.25)
    widget_dic["plan"].scale(plan_faktor)
    plan_start_x = widget_dic["plan"].x
    plan_start_y = widget_dic["plan"].y
    # Plan und Überschrift
    widget_dic["title"].place(x = plan_start_x + new_w // 2 - widget_dic["title"].width // 2, y = plan_start_y // 2 - widget_dic["title"].height // 2).config(font = epw.SysFont(font = "Calibri", font_size=  int(65 * gen_faktor_w)))
    # Status
    widget_dic["status_title_label"].place(x = screen_w * 0.3, y = screen_h * 0.8).config(font = epw.SysFont(font = "Calibri", font_size=  int(40 * gen_faktor_w)))
    widget_dic["status_label"].place(x = screen_w * 0.3, y = screen_h * 0.8 + widget_dic["status_title_label"].height).config(font = epw.SysFont(font = "Calibri", font_size=  int(30 * gen_faktor_w)))
    widget_dic["status_label"].config(min_width = 2 * (screen_w * 0.4) // 3)
    # Raumtyp
    widget_dic["room_type_label"].place(x = screen_w * 0.15 - widget_dic["room_type_label"].width // 2, y = screen_h * 0.25).config(font = epw.SysFont(font = "Calibri", font_size=  int(40 * gen_faktor_w)))
    widget_dic["square_button_label"].place(x = 60, y = screen_h * 0.4 - widget_dic["square_button_label"].height).config(font = epw.SysFont(font = "Calibri", font_size=  int(30 * gen_faktor_w)))
    widget_dic["square_button"].place(x = 60, y = screen_h * 0.4).config(font = epw.SysFont(font = "Calibri", font_size=  int(30 * gen_faktor_w)))
    widget_dic["polygon_button_label"].place(x = 60, y = screen_h * 0.5 - widget_dic["polygon_button_label"].height).config(font = epw.SysFont(font = "Calibri", font_size=  int(30 * gen_faktor_w)))
    widget_dic["polygon_button"].place(x = 60, y = screen_h * 0.5).config(font = epw.SysFont(font = "Calibri", font_size=  int(30 * gen_faktor_w)))
    widget_dic["waypoint_button_label"].place(x = 60, y = screen_h * 0.6 - widget_dic["waypoint_button_label"].height).config(font = epw.SysFont(font = "Calibri", font_size=  int(30 * gen_faktor_w)))
    widget_dic["waypoint_button"].place(x = 60, y = screen_h * 0.6).config(font = epw.SysFont(font = "Calibri", font_size=  int(30 * gen_faktor_w)))
    widget_dic["room_create_submit_button"].place(x = 60 + widget_dic["square_button"].width + (screen_w * 0.3 - (60 + widget_dic["square_button"].width)) // 2 - widget_dic["room_create_submit_button"].width // 2, y = screen_h * 0.4).config(font = epw.SysFont(font = "Calibri", font_size=  int(30 * gen_faktor_w)))
    widget_dic["room_create_cancel_button"].place(x = widget_dic["room_create_submit_button"].x, y = screen_h * 0.5 - widget_dic["room_create_cancel_button"].height).config(font = epw.SysFont(font = "Calibri", font_size=  int(30 * gen_faktor_w)))
    # Rauminfo
    widget_dic["room_info_label"].place(x = screen_w * 0.15 - widget_dic["room_info_label"].width // 2, y = screen_h * 0.25).config(font = epw.SysFont(font = "Calibri", font_size=  int(40 * gen_faktor_w)))
    widget_dic["room_id_label"].place(x = 60, y = screen_h * 0.4 - widget_dic["room_id_label"].height).config(font = epw.SysFont(font = "Calibri", font_size=  int(30 * gen_faktor_w)))
    widget_dic["entry_background_label1"].place(x = 60, y = screen_h * 0.4).config(font = epw.SysFont(font = "Calibri", font_size=  int(30 * gen_faktor_w)))
    widget_dic["room_id_entry"].place(x = 60, y = screen_h * 0.4).config(font = epw.SysFont(font = "Calibri", font_size=  int(30 * gen_faktor_w)))
    widget_dic["room_name_label"].place(x = 60, y = screen_h * 0.5 - widget_dic["room_name_label"].height).config(font = epw.SysFont(font = "Calibri", font_size=  int(30 * gen_faktor_w)))
    widget_dic["entry_background_label2"].place(x = 60, y = screen_h * 0.5).config(font = epw.SysFont(font = "Calibri", font_size=  int(30 * gen_faktor_w)))
    widget_dic["room_name_entry"].place(x = 60, y = screen_h * 0.5).config(font = epw.SysFont(font = "Calibri", font_size=  int(30 * gen_faktor_w)))
    widget_dic["room_prof_label"].place(x = 60, y = screen_h * 0.6 - widget_dic["room_prof_label"].height).config(font = epw.SysFont(font = "Calibri", font_size=  int(30 * gen_faktor_w)))
    widget_dic["entry_background_label3"].place(x = 60, y = screen_h * 0.6).config(font = epw.SysFont(font = "Calibri", font_size=  int(30 * gen_faktor_w)))
    widget_dic["room_prof_entry"].place(x = 60, y = screen_h * 0.6).config(font = epw.SysFont(font = "Calibri", font_size=  int(30 * gen_faktor_w)))
    widget_dic["room_extrainfo_label"].place(x = 60, y = screen_h * 0.7 - widget_dic["room_extrainfo_label"].height).config(font = epw.SysFont(font = "Calibri", font_size=  int(30 * gen_faktor_w)))
    widget_dic["entry_background_label4"].place(x = 60, y = screen_h * 0.7).config(font = epw.SysFont(font = "Calibri", font_size=  int(30 * gen_faktor_w)))
    widget_dic["room_extrainfo_entry"].place(x = 60, y = screen_h * 0.7).config(font = epw.SysFont(font = "Calibri", font_size=  int(30 * gen_faktor_w)))
    widget_dic["room_finish_submit_button"].place(x = 60, y = screen_h * 0.8 - widget_dic["room_finish_submit_button"].height).config(font = epw.SysFont(font = "Calibri", font_size=  int(30 * gen_faktor_w)))
    widget_dic["room_finish_cancel_button"].place(x = 240, y = screen_h * 0.8 - widget_dic["room_finish_cancel_button"].height).config(font = epw.SysFont(font = "Calibri", font_size=  int(30 * gen_faktor_w)))
    widget_dic["star_info_label"].place(x = 60, y = screen_h * 0.875 - widget_dic["star_info_label"].height).config(font = epw.SysFont(font = "Calibri", font_size=  int(20 * gen_faktor_w)))
    # Info Symbol
    widget_dic["info_icon"].scale(0.05, 0)
    widget_dic["info_icon"].place(x = screen_w - info_icon.get_width() * 0.05 - 20, y = 20)
    return plan_faktor

def screenwidth_percent(value):
    screen_w = screen.get_width()
    return screen_w * value

def screenheight_percent(value):
    screen_h = screen.get_height()
    return screen_h * value

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

def waypoint_selected():
    global shape, widget_dic
    if shape == 0:
        shape = 3
        widget_dic["status_label"].config(text = "Waypoint Ausgewählt")

def room_create_submit():
    widget_dic["room_creation_screen"].hide()
    widget_dic["room_info_screen"].show()

def room_create_cancel():
    global shape, widget_dic, s_coords, p_coords, s_coords_count, p_coords_count, s_submit, p_submit, w_submit
    shape = 0
    s_coords.clear()
    p_coords.clear()
    s_coords_count = 0
    p_coords_count = 0
    s_submit = False
    p_submit = False
    w_submit = False
    widget_dic["status_label"].config(text = "Zurücksetzen des Raumtyps")

def room_info_submit_button_delay():
    widget_dic["room_info_submit_button"].config(visible = True)

def room_info_submit_button_show(info_type):
    epw.schedule(room_info_submit_button_delay, 1)
    widget_dic["room_id_entry"].config(width = screenwidth_percent(0.3) - 120 - widget_dic["room_info_submit_button"].width)
    widget_dic["room_name_entry"].config(width = screenwidth_percent(0.3) - 120 - widget_dic["room_info_submit_button"].width)
    widget_dic["room_prof_entry"].config(width = screenwidth_percent(0.3) - 120 - widget_dic["room_info_submit_button"].width)
    widget_dic["room_extrainfo_entry"].config(width = screenwidth_percent(0.3) - 120 - widget_dic["room_info_submit_button"].width)
    if info_type == "id":
        widget_dic["room_info_submit_button"].place(x = screenwidth_percent(0.3) - 60 - widget_dic["room_info_submit_button"].width, y = widget_dic["room_id_entry"].y)
    elif info_type == "name":
        widget_dic["room_info_submit_button"].place(x = screenwidth_percent(0.3) - 60 - widget_dic["room_info_submit_button"].width, y = widget_dic["room_name_entry"].y)
    elif info_type == "prof":
        widget_dic["room_info_submit_button"].place(x = screenwidth_percent(0.3) - 60 - widget_dic["room_info_submit_button"].width, y = widget_dic["room_prof_entry"].y)
    elif info_type == "extra":
        widget_dic["room_info_submit_button"].place(x = screenwidth_percent(0.3) - 60 - widget_dic["room_info_submit_button"].width, y = widget_dic["room_extrainfo_entry"].y)

def room_info_submit_button_hide():
    pos = pygame.mouse.get_pos()
    if pos[0] >= widget_dic["room_info_submit_button"].x and pos[0] <= widget_dic["room_info_submit_button"].x + widget_dic["room_info_submit_button"].width and pos[1] >= widget_dic["room_info_submit_button"].y and pos[1] <= widget_dic["room_info_submit_button"].y + widget_dic["room_info_submit_button"].height:
        pass
    else:
        widget_dic["room_info_submit_button"].config(visible = False)
        widget_dic["room_id_entry"].config(width = screenwidth_percent(0.3) - 120)
        widget_dic["room_name_entry"].config(width = screenwidth_percent(0.3) - 120)
        widget_dic["room_prof_entry"].config(width = screenwidth_percent(0.3) - 120)
        widget_dic["room_extrainfo_entry"].config(width = screenwidth_percent(0.3) - 120)

def room_info_submit():
    global id_answer_list, name_answer_list, prof_answer_list, extra_answer_list
    if widget_dic["room_info_submit_button"].y == screenheight_percent(0.4):
        id_answer_list.clear()
        id_answer_list.append(widget_dic["room_id_entry"].get())
        widget_dic["room_id_entry"].config(text = "")
    elif widget_dic["room_info_submit_button"].y == screenheight_percent(0.5):
        name_answer_list.append(widget_dic["room_name_entry"].get())
        widget_dic["room_name_entry"].config(text = "")
    elif widget_dic["room_info_submit_button"].y == screenheight_percent(0.6):
        prof_answer_list.append(widget_dic["room_prof_entry"].get())
        widget_dic["room_prof_entry"].config(text = "")
    elif widget_dic["room_info_submit_button"].y == screenheight_percent(0.7):
        extrainfo_answer_list.append(widget_dic["room_extrainfo_entry"].get())
        widget_dic["room_extrainfo_entry"].config(text = "")
    widget_dic["room_info_submit_button"].config(visible = False)

def room_create_finish_submit():
    print(id_answer_list, name_answer_list, prof_answer_list, extrainfo_answer_list)

def room_create_finish_cancel():
    id_answer_list.clear()
    name_answer_list.clear()
    prof_answer_list.clear()
    extrainfo_answer_list.clear()
    room_create_cancel()
    widget_dic["room_id_entry"].config(text = "")
    widget_dic["room_name_entry"].config(text = "")
    widget_dic["room_prof_entry"].config(text = "")
    widget_dic["room_extrainfo_entry"].config(text = "")
    widget_dic["room_info_screen"].hide()
    widget_dic["room_creation_screen"].show()
    widget_dic["status_label"].config(text = "Zurücksetzen der Raumerstellung")

room_creation_screen = epw.Screen(visible = True)
room_info_screen = epw.Screen(visible = False)
def create_background_label():
    return epw.Label(text = "", screen = room_info_screen, active_unpressed_background_color = (50, 50, 50), 
                                                            active_hover_background_color = (50, 50, 50),
                                                            active_pressed_background_color = (50, 50, 50),
                                                            top_left_corner_radius = 15, 
                                                            top_right_corner_radius = 15, 
                                                            bottom_left_corner_radius = 15, 
                                                            bottom_right_corner_radius = 15,
                                                            min_width =  screenwidth_percent(0.3) - 120,
                                                            layer = 0)

widget_dic = {
    # Bildschirm
    "room_creation_screen": room_creation_screen,
    "room_info_screen": room_info_screen,
    # plan
    "plan": epw.Surface(plan),
    # 
    "title": epw.Label(text = "Raumeditor", font = epw.SysFont(font = "Calibri", font_size=65)),
    # status label
    "status_title_label": epw.Label(text = "Status", font=epw.SysFont(font="Calibri", font_size=40, bold = True), alignment_spacing = 0, alignment = "left"),
    "status_label": epw.Label(text = "", font = epw.SysFont(font = "Calibri", font_size = 30),
                                                        alignment = "left",
                                                        active_unpressed_background_color = (50, 50, 50), 
                                                        active_hover_background_color = (50, 50, 50),
                                                        active_pressed_background_color = (50, 50, 50),
                                                        top_left_corner_radius = 15, 
                                                        top_right_corner_radius = 15, 
                                                        bottom_left_corner_radius = 15, 
                                                        bottom_right_corner_radius = 15),
    # Raumtyp
    "room_type_label": epw.Label(text = "Raumtyp - / Wegpunktauswahl", font=epw.SysFont(font="Calibri", font_size=40, bold = True), screen = room_creation_screen),
    "square_button_label": epw.Label(text = "Quadratischer Raum", font=epw.SysFont(font="Calibri", font_size=30), alignment_spacing = 0, alignment = "left",screen = room_creation_screen),
    "square_button": epw.Button(text = "Auswählen", font=epw.SysFont(font="Calibri", font_size=30), command = square_selected,screen = room_creation_screen),
    "polygon_button_label": epw.Label(text = "Polygon Raum", font=epw.SysFont(font="Calibri", font_size=30), alignment_spacing = 0, alignment = "left",screen = room_creation_screen),
    "polygon_button": epw.Button(text = "Auswählen", font=epw.SysFont(font="Calibri", font_size=30), command = polygon_selected,screen = room_creation_screen),
    "waypoint_button_label": epw.Label(text = "Wegpunkt", font=epw.SysFont(font="Calibri", font_size=30), alignment_spacing = 0, alignment = "left",screen = room_creation_screen),
    "waypoint_button": epw.Button(text = "Auswählen", font=epw.SysFont(font="Calibri", font_size=30), command = waypoint_selected,screen = room_creation_screen),
    "room_create_submit_button": epw.Button(text = "Bestätigen", font=epw.SysFont(font="Calibri", font_size=30), command = room_create_submit,screen = room_creation_screen),
    "room_create_cancel_button": epw.Button(text = "Abbrechen", font=epw.SysFont(font="Calibri", font_size=30), command = room_create_cancel,screen = room_creation_screen),
    # Rauminfo
    "room_info_label": epw.Label(text = "Rauminformationen", font=epw.SysFont(font="Calibri", font_size=40, bold = True),screen = room_info_screen),
    "room_id_label": epw.Label(text = "Raum Nr / ID *", font=epw.SysFont(font="Calibri", font_size=30), alignment_spacing = 0, alignment = "left", screen = room_info_screen),
    "room_id_entry": epw.Entry(font = epw.SysFont(font="Calibri", font_size=30), height = 57, hide_background = True, hide_border = True, auto_size = False, width =  screenwidth_percent(0.3) - 120, screen = room_info_screen).bind("<FOCUS-IN>", lambda:room_info_submit_button_show("id")).bind("<FOCUS-OUT>", room_info_submit_button_hide, False),
    "room_name_label": epw.Label(text = "Raum Name **", font=epw.SysFont(font="Calibri", font_size=30), alignment_spacing = 0, alignment = "left", screen = room_info_screen),
    "room_name_entry": epw.Entry(font=epw.SysFont(font="Calibri", font_size=30), height = 57, hide_background = True, hide_border = True, auto_size = False, width =  screenwidth_percent(0.3) - 120,screen = room_info_screen).bind("<FOCUS-IN>", lambda:room_info_submit_button_show("name")).bind("<FOCUS-OUT>", room_info_submit_button_hide, False),
    "room_prof_label": epw.Label(text = "Raum Lehrer / Professor **", font=epw.SysFont(font="Calibri", font_size=30), alignment_spacing = 0, alignment = "left", screen = room_info_screen),
    "room_prof_entry": epw.Entry(font = epw.SysFont(font="Calibri", font_size=30), height = 57, hide_background = True, hide_border = True, auto_size = False, width =  screenwidth_percent(0.3) - 120, screen = room_info_screen).bind("<FOCUS-IN>", lambda:room_info_submit_button_show("prof")).bind("<FOCUS-OUT>", room_info_submit_button_hide, False),
    "room_extrainfo_label": epw.Label(text = "Raum Zusatzinformationen **", font=epw.SysFont(font="Calibri", font_size=30), alignment_spacing = 0, alignment = "left", screen = room_info_screen),
    "room_extrainfo_entry": epw.Entry(font = epw.SysFont(font="Calibri", font_size=30), height = 57, hide_background = True, hide_border = True, auto_size = False, width =  screenwidth_percent(0.3) - 120, screen = room_info_screen).bind("<FOCUS-IN>", lambda:room_info_submit_button_show("extra")).bind("<FOCUS-OUT>", room_info_submit_button_hide, False),
    "room_info_submit_button": epw.Button(text = "Bestätigen", font=epw.SysFont(font="Calibri", font_size=30), command = room_info_submit, height = 57, auto_size = False, corner_radius = 15, visible = False, screen = room_info_screen),
    "entry_background_label1": create_background_label(),
    "entry_background_label2": create_background_label(),
    "entry_background_label3": create_background_label(),
    "entry_background_label4": create_background_label(),
    "room_finish_submit_button": epw.Button(text = "Bestätigen", font=epw.SysFont(font="Calibri", font_size=30), command = room_create_finish_submit, screen = room_info_screen),
    "room_finish_cancel_button": epw.Button(text = "Abbrechen", font=epw.SysFont(font="Calibri", font_size=30), command = room_create_finish_cancel, screen = room_info_screen),
    "star_info_label": epw.Label(text = "*   max. eine Angabe\n** optionale Angabe", font=epw.SysFont(font="Calibri", font_size=20), alignment_spacing = 0, alignment = "left", screen = room_info_screen),
    # info icon
    "info_icon": epw.Surface(info_icon)
}


update_ui(widget_dic)
running = True
while running:
    # färben des Hintergrunds
    screen.fill((30, 30, 30))

    if s_submit == True or p_submit == True or w_submit == True:
        widget_dic["room_create_submit_button"].config(state = "enabled")
    else:
        widget_dic["room_create_submit_button"].config(state = "disabled")

    if shape == 0:
        widget_dic["room_create_cancel_button"].config(state = "disabled")
    else:
        widget_dic["room_create_cancel_button"].config(state = "enabled")
    
    if id_answer_list == []:
        widget_dic["room_finish_submit_button"].config(state = "disabled")
    else:
        widget_dic["room_finish_submit_button"].config(state = "enabled")

    for event in pygame.event.get():
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            scale = update_ui(widget_dic)

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
                if p_x >= 0 and p_x <= plan_w and p_y >= 0 and p_y <= plan_h:
                    p_coords.append(p_x)
                    p_coords.append(p_y)
                    widget_dic["status_label"].config(text = f"Die Koordinate {p_x}, {p_y} wurde hinzugefügt.")
                    p_coords_count += 1
                    if p_coords_count >= 3:
                        p_submit = True

            elif shape == 3:
                pos = pygame.mouse.get_pos()
                w_x, w_y = int((pos[0] - plan_start_x) / scale), int((pos[1] - plan_start_y) / scale)
                if w_coords_count == 0 and w_x >= 0 and w_x <= plan_w and w_y >= 0 and w_y <= plan_h:
                    w_coords.append(w_x)
                    w_coords.append(w_y)
                    widget_dic["status_label"].config(text = f"Die Koordinate {w_x}, {w_y} wurde hinzugefügt.")
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
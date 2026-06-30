# coordsbestimmung_überarbeitet
# Theo Glase
# 04.06.2026

import pygame
import easypygamewidgets as epw
import ctypes
from main_functions import plan_selection, save_data

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
        widget_dic["4_01_label_statuscontent"].config(text = "Quadratischer Raumtyp Ausgewählt")

def polygon_selected():
    global shape, widget_dic
    if shape == 0:
        shape = 2
        widget_dic["4_01_label_statuscontent"].config(text = "Polygonaler Raumtyp Ausgewählt")

def waypoint_selected():
    global shape, widget_dic
    if shape == 0:
        shape = 3
        widget_dic["4_01_label_statuscontent"].config(text = "Waypoint Ausgewählt")
    
def room_create_finish_submit():
    #add_json()
    save_data(plan_path, shape, id_answer_list, name_answer_list, prof_answer_list, extrainfo_answer_list)

def room_create_submit():
    widget_dic["4_0_screen_group"].hide()
    widget_dic["4_1_screen_group"].show()

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
    widget_dic["4_01_label_statuscontent"].config(text = "Zurücksetzen des Raumtyps")

def room_info_submit():
    global id_answer_list, name_answer_list, prof_answer_list, extra_answer_list
    if widget_dic["4_1_button_infosub"].y == screenheight_percent(0.4):
        id_answer_list.clear()
        id_answer_list.append(widget_dic["4_1_entry_id"].get())
        widget_dic["4_1_entry_id"].config(text = "")
    elif widget_dic["4_1_button_infosub"].y == screenheight_percent(0.5):
        name_answer_list.append(widget_dic["4_1_entry_name"].get())
        widget_dic["4_1_entry_name"].config(text = "")
    elif widget_dic["4_1_button_infosub"].y == screenheight_percent(0.6):
        prof_answer_list.append(widget_dic["4_1_entry_prof"].get())
        widget_dic["4_1_entry_prof"].config(text = "")
    elif widget_dic["4_1_button_infosub"].y == screenheight_percent(0.7):
        extrainfo_answer_list.append(widget_dic["4_1_entry_extrainfo"].get())
        widget_dic["4_1_entry_extrainfo"].config(text = "")
    widget_dic["4_1_button_infosub"].config(visible = False)

def room_create_finish_cancel():
    id_answer_list.clear()
    name_answer_list.clear()
    prof_answer_list.clear()
    extrainfo_answer_list.clear()
    room_create_cancel()
    widget_dic["4_1_entry_id"].config(text = "")
    widget_dic["4_1_entry_name"].config(text = "")
    widget_dic["4_1_entry_prof"].config(text = "")
    widget_dic["4_1_entry_extrainfo"].config(text = "")
    widget_dic["4_1_screen_group"].hide()
    widget_dic["4_0_screen_group"].show()
    widget_dic["4_01_label_statuscontent"].config(text = "Zurücksetzen der Raumerstellung")

def show_4_1_button_infosub(info_type):
    epw.schedule(delay_4_1_button_infosub, 1)
    widget_dic["4_1_entry_id"].config(width = int((screenwidth_percent(0.3) - 60 - widget_dic["4_1_button_infosub"].width) * gen_faktor_w))
    widget_dic["4_1_entry_name"].config(width = int((screenwidth_percent(0.3) - 60 - widget_dic["4_1_button_infosub"].width) * gen_faktor_w))
    widget_dic["4_1_entry_prof"].config(width = int((screenwidth_percent(0.3) - 60 - widget_dic["4_1_button_infosub"].width) * gen_faktor_w))
    widget_dic["4_1_entry_extrainfo"].config(width = screenwidth_percent(0.3) - 120 - widget_dic["4_1_button_infosub"].width)
    if info_type == "id":
        widget_dic["4_1_button_infosub"].place(x = int((screenwidth_percent(0.3) - 60 - widget_dic["4_1_button_infosub"].width) * gen_faktor_w), y = widget_dic["4_1_entry_id"].y)
    elif info_type == "name":
        widget_dic["4_1_button_infosub"].place(x = int((screenwidth_percent(0.3) - 60 - widget_dic["4_1_button_infosub"].width) * gen_faktor_w), y = widget_dic["4_1_entry_name"].y)
    elif info_type == "prof":
        widget_dic["4_1_button_infosub"].place(x = int((screenwidth_percent(0.3) - 60 - widget_dic["4_1_button_infosub"].width) * gen_faktor_w), y = widget_dic["4_1_entry_prof"].y)
    elif info_type == "extra":
        widget_dic["4_1_button_infosub"].place(x = int((screenwidth_percent(0.3) - 60 - widget_dic["4_1_button_infosub"].width) * gen_faktor_w), y = widget_dic["4_1_entry_extrainfo"].y)

def room_info_submit_button_hide():
    pos = pygame.mouse.get_pos()
    if pos[0] >= widget_dic["4_1_button_infosub"].x and pos[0] <= widget_dic["4_1_button_infosub"].x + widget_dic["4_1_button_infosub"].width and pos[1] >= widget_dic["4_1_button_infosub"].y and pos[1] <= widget_dic["4_1_button_infosub"].y + widget_dic["4_1_button_infosub"].height:
        pass
    else:
        widget_dic["4_1_button_infosub"].config(visible = False)
        widget_dic["4_1_entry_id"].config(width = screenwidth_percent(0.3) - 120)
        widget_dic["4_1_entry_name"].config(width = screenwidth_percent(0.3) - 120)
        widget_dic["4_1_entry_prof"].config(width = screenwidth_percent(0.3) - 120)
        widget_dic["4_1_entry_extrainfo"].config(width = screenwidth_percent(0.3) - 120)

def delay_4_1_button_infosub():
    widget_dic["4_1_button_infosub"].config(visible = True)

def update_ui(widget_dic):
    global gen_faktor_w, gen_faktor_h, plan_start_x, plan_start_y
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
    widget_dic["4_01_surface_plan"].config(surface = plan)
    widget_dic["4_01_surface_plan"].place(x = screen_w * 0.30, y = screen_h * 0.25)
    widget_dic["4_01_surface_plan"].scale(plan_faktor)
    plan_start_x = widget_dic["4_01_surface_plan"].x
    plan_start_y = widget_dic["4_01_surface_plan"].y
    print(f"screen_w: {screen_w}, screen_h: {screen_h}, new_w: {new_w}, new_h: {new_h}, plan_start_x: {plan_start_x}, plan_start_y: {plan_start_y}, plan_faktor: {plan_faktor}, widget w: {int((screenwidth_percent(0.3) - 120) * gen_faktor_w)}, widget h:{int(57 * gen_faktor_h)}")
    # Plan und Überschrift
    widget_dic["4_01_label_maintitle"].place(x = plan_start_x + new_w // 2 - widget_dic["4_01_label_maintitle"].width // 2, y = plan_start_y // 2 - widget_dic["4_01_label_maintitle"].height // 2).config(font = epw.SysFont(font = "Calibri", font_size=  int(65 * gen_faktor_w)))
    # Status
    widget_dic["4_01_label_statustitle"].place(x = screen_w * 0.3, y = screen_h * 0.8).config(font = epw.SysFont(font = "Calibri", font_size=  int(40 * gen_faktor_w)))
    widget_dic["4_01_label_statuscontent"].place(x = screen_w * 0.3, y = screen_h * 0.8 + widget_dic["4_01_label_statustitle"].height).config(font = epw.SysFont(font = "Calibri", font_size=  int(30 * gen_faktor_w)))
    widget_dic["4_01_label_statuscontent"].config(min_width = 2 * (screen_w * 0.4) // 3)
    # Raumtyp
    widget_dic["4_0_label_roomtype"].place(x = screen_w * 0.15 - widget_dic["4_0_label_roomtype"].width // 2, y = screen_h * 0.25).config(font = epw.SysFont(font = "Calibri", font_size=  int(40 * gen_faktor_w)))
    widget_dic["4_0_label_squaretype"].place(x = 60, y = screen_h * 0.4 - widget_dic["4_0_label_squaretype"].height).config(font = epw.SysFont(font = "Calibri", font_size=  int(30 * gen_faktor_w)))
    widget_dic["4_0_button_squaretype"].place(x = 60, y = screen_h * 0.4).config(font = epw.SysFont(font = "Calibri", font_size=  int(30 * gen_faktor_w)))
    widget_dic["4_0_label_polytype"].place(x = 60, y = screen_h * 0.5 - widget_dic["4_0_label_polytype"].height).config(font = epw.SysFont(font = "Calibri", font_size=  int(30 * gen_faktor_w)))
    widget_dic["4_0_button_polytype"].place(x = 60, y = screen_h * 0.5).config(font = epw.SysFont(font = "Calibri", font_size=  int(30 * gen_faktor_w)))
    widget_dic["4_0_label_waytype"].place(x = 60, y = screen_h * 0.6 - widget_dic["4_0_label_waytype"].height).config(font = epw.SysFont(font = "Calibri", font_size=  int(30 * gen_faktor_w)))
    widget_dic["4_0_button_waytype"].place(x = 60, y = screen_h * 0.6).config(font = epw.SysFont(font = "Calibri", font_size=  int(30 * gen_faktor_w)))
    widget_dic["4_0_button_createsub"].place(x = 60 + widget_dic["4_0_button_squaretype"].width + (screen_w * 0.3 - (60 + widget_dic["4_0_button_squaretype"].width)) // 2 - widget_dic["4_0_button_createsub"].width // 2, y = screen_h * 0.4).config(font = epw.SysFont(font = "Calibri", font_size=  int(30 * gen_faktor_w)))
    widget_dic["4_0_button_createcan"].place(x = widget_dic["4_0_button_createsub"].x, y = screen_h * 0.5 - widget_dic["4_0_button_createcan"].height).config(font = epw.SysFont(font = "Calibri", font_size=  int(30 * gen_faktor_w)))
    # Rauminfo
    widget_dic["4_1_button_infosub"].config(font = epw.SysFont(font = "Calibri", font_size=  int(30 * gen_faktor_w)))
    widget_dic["4_1_label_infotitle"].place(x = screen_w * 0.15 - widget_dic["4_1_label_infotitle"].width // 2, y = screen_h * 0.25).config(font = epw.SysFont(font = "Calibri", font_size=  int(40 * gen_faktor_w)))
    widget_dic["4_1_label_id"].place(x = 60, y = screen_h * 0.4 - widget_dic["4_1_label_id"].height).config(font = epw.SysFont(font = "Calibri", font_size=  int(30 * gen_faktor_w)))
    widget_dic["4_1_label_entrybackgr1"].place(x = 60, y = screen_h * 0.4).config(font = epw.SysFont(font = "Calibri", font_size=  int(30 * gen_faktor_w)), min_width = int((screenwidth_percent(0.3) - 120) * gen_faktor_w))
    widget_dic["4_1_entry_id"].place(x = 60, y = screen_h * 0.4).config(font = epw.SysFont(font = "Calibri", font_size=  int(30 * gen_faktor_w)), height = int(57 * gen_faktor_h), width = int((screenwidth_percent(0.3) - 120) * gen_faktor_w))
    widget_dic["4_1_label_name"].place(x = 60, y = screen_h * 0.5 - widget_dic["4_1_label_name"].height).config(font = epw.SysFont(font = "Calibri", font_size=  int(30 * gen_faktor_w)))
    widget_dic["4_1_label_entrybackgr2"].place(x = 60, y = screen_h * 0.5).config(font = epw.SysFont(font = "Calibri", font_size=  int(30 * gen_faktor_w)), min_width = int((screenwidth_percent(0.3) - 120) * gen_faktor_w))
    widget_dic["4_1_entry_name"].place(x = 60, y = screen_h * 0.5).config(font = epw.SysFont(font = "Calibri", font_size=  int(30 * gen_faktor_w)), height = int(57 * gen_faktor_h), width = int((screenwidth_percent(0.3) - 120) * gen_faktor_w))
    widget_dic["4_1_label_prof"].place(x = 60, y = screen_h * 0.6 - widget_dic["4_1_label_prof"].height).config(font = epw.SysFont(font = "Calibri", font_size=  int(30 * gen_faktor_w)))
    widget_dic["4_1_label_entrybackgr3"].place(x = 60, y = screen_h * 0.6).config(font = epw.SysFont(font = "Calibri", font_size=  int(30 * gen_faktor_w)), min_width = int((screenwidth_percent(0.3) - 120) * gen_faktor_w))
    widget_dic["4_1_entry_prof"].place(x = 60, y = screen_h * 0.6).config(font = epw.SysFont(font = "Calibri", font_size=  int(30 * gen_faktor_w)), height = int(57 * gen_faktor_h), width = int((screenwidth_percent(0.3) - 120) * gen_faktor_w))
    widget_dic["4_1_label_extrainfo"].place(x = 60, y = screen_h * 0.7 - widget_dic["4_1_label_extrainfo"].height).config(font = epw.SysFont(font = "Calibri", font_size=  int(30 * gen_faktor_w)))
    widget_dic["4_1_label_entrybackgr4"].place(x = 60, y = screen_h * 0.7).config(font = epw.SysFont(font = "Calibri", font_size=  int(30 * gen_faktor_w)), min_width = int((screenwidth_percent(0.3) - 120) * gen_faktor_w))
    widget_dic["4_1_entry_extrainfo"].place(x = 60, y = screen_h * 0.7).config(font = epw.SysFont(font = "Calibri", font_size=  int(30 * gen_faktor_w)), height = int(57 * gen_faktor_h), width = int((screenwidth_percent(0.3) - 120) * gen_faktor_w))
    widget_dic["4_1_button_finishsub"].place(x = 60, y = screen_h * 0.8 - widget_dic["4_1_button_finishsub"].height).config(font = epw.SysFont(font = "Calibri", font_size=  int(30 * gen_faktor_w)))
    widget_dic["4_1_button_finishcan"].place(x = 240, y = screen_h * 0.8 - widget_dic["4_1_button_finishcan"].height).config(font = epw.SysFont(font = "Calibri", font_size=  int(30 * gen_faktor_w)))
    widget_dic["4_1_label_starinfo"].place(x = 60, y = screen_h * 0.875 - widget_dic["4_1_label_starinfo"].height).config(font = epw.SysFont(font = "Calibri", font_size=  int(20 * gen_faktor_w)))
    # Info Symbol
    widget_dic["4_01_icon_infosymbol"].scale(0.05, 0)
    widget_dic["4_01_icon_infosymbol"].place(x = screen_w - info_icon.get_width() * 0.05 - 20, y = 20)
    return plan_faktor

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
    "4_0_screen_group": room_creation_screen,
    "4_1_screen_group": room_info_screen,
    # plan
    "4_01_surface_plan": epw.Surface(plan),
    # 
    "4_01_label_maintitle": epw.Label(text = "Raumeditor", font = epw.SysFont(font = "Calibri", font_size=65)),
    # status label
    "4_01_label_statustitle": epw.Label(text = "Status", font=epw.SysFont(font="Calibri", font_size=40, bold = True), alignment_spacing = 0, alignment = "left"),
    "4_01_label_statuscontent": epw.Label(text = "", font = epw.SysFont(font = "Calibri", font_size = 30),
                                                        alignment = "left",
                                                        active_unpressed_background_color = (50, 50, 50), 
                                                        active_hover_background_color = (50, 50, 50),
                                                        active_pressed_background_color = (50, 50, 50),
                                                        top_left_corner_radius = 15, 
                                                        top_right_corner_radius = 15, 
                                                        bottom_left_corner_radius = 15, 
                                                        bottom_right_corner_radius = 15),
    # Raumtyp
    "4_0_label_roomtype": epw.Label(text = "Raumtyp - / Wegpunktauswahl", font=epw.SysFont(font="Calibri", font_size=40, bold = True), screen = room_creation_screen),
    "4_0_label_squaretype": epw.Label(text = "Quadratischer Raum", font=epw.SysFont(font="Calibri", font_size=30), alignment_spacing = 0, alignment = "left",screen = room_creation_screen),
    "4_0_button_squaretype": epw.Button(text = "Auswählen", font=epw.SysFont(font="Calibri", font_size=30), command = square_selected,screen = room_creation_screen),
    "4_0_label_polytype": epw.Label(text = "Polygon Raum", font=epw.SysFont(font="Calibri", font_size=30), alignment_spacing = 0, alignment = "left",screen = room_creation_screen),
    "4_0_button_polytype": epw.Button(text = "Auswählen", font=epw.SysFont(font="Calibri", font_size=30), command = polygon_selected,screen = room_creation_screen),
    "4_0_label_waytype": epw.Label(text = "Wegpunkt", font=epw.SysFont(font="Calibri", font_size=30), alignment_spacing = 0, alignment = "left",screen = room_creation_screen),
    "4_0_button_waytype": epw.Button(text = "Auswählen", font=epw.SysFont(font="Calibri", font_size=30), command = waypoint_selected,screen = room_creation_screen),
    "4_0_button_createsub": epw.Button(text = "Bestätigen", font=epw.SysFont(font="Calibri", font_size=30), command = room_create_submit,screen = room_creation_screen),
    "4_0_button_createcan": epw.Button(text = "Abbrechen", font=epw.SysFont(font="Calibri", font_size=30), command = room_create_cancel,screen = room_creation_screen),
    # Rauminfo
    "4_1_label_infotitle": epw.Label(text = "Rauminformationen", font=epw.SysFont(font="Calibri", font_size=40, bold = True),screen = room_info_screen),
    "4_1_label_id": epw.Label(text = "Raum Nr / ID *", font=epw.SysFont(font="Calibri", font_size=30), alignment_spacing = 0, alignment = "left", screen = room_info_screen),
    "4_1_entry_id": epw.Entry(font = epw.SysFont(font="Calibri", font_size=30), height = 57, hide_background = True, hide_border = True, auto_size = False, width =  screenwidth_percent(0.3) - 120, screen = room_info_screen).bind("<FOCUS-IN>", lambda:show_4_1_button_infosub("id")).bind("<FOCUS-OUT>", room_info_submit_button_hide, False),
    "4_1_label_name": epw.Label(text = "Raum Name **", font=epw.SysFont(font="Calibri", font_size=30), alignment_spacing = 0, alignment = "left", screen = room_info_screen),
    "4_1_entry_name": epw.Entry(font=epw.SysFont(font="Calibri", font_size=30), height = 57, hide_background = True, hide_border = True, auto_size = False, width =  screenwidth_percent(0.3) - 120,screen = room_info_screen).bind("<FOCUS-IN>", lambda:show_4_1_button_infosub("name")).bind("<FOCUS-OUT>", room_info_submit_button_hide, False),
    "4_1_label_prof": epw.Label(text = "Raum Lehrer / Professor **", font=epw.SysFont(font="Calibri", font_size=30), alignment_spacing = 0, alignment = "left", screen = room_info_screen),
    "4_1_entry_prof": epw.Entry(font = epw.SysFont(font="Calibri", font_size=30), height = 57, hide_background = True, hide_border = True, auto_size = False, width =  screenwidth_percent(0.3) - 120, screen = room_info_screen).bind("<FOCUS-IN>", lambda:show_4_1_button_infosub("prof")).bind("<FOCUS-OUT>", room_info_submit_button_hide, False),
    "4_1_label_extrainfo": epw.Label(text = "Raum Zusatzinformationen **", font=epw.SysFont(font="Calibri", font_size=30), alignment_spacing = 0, alignment = "left", screen = room_info_screen),
    "4_1_entry_extrainfo": epw.Entry(font = epw.SysFont(font="Calibri", font_size=30), height = 57, hide_background = True, hide_border = True, auto_size = False, width =  screenwidth_percent(0.3) - 120, screen = room_info_screen).bind("<FOCUS-IN>", lambda:show_4_1_button_infosub("extra")).bind("<FOCUS-OUT>", room_info_submit_button_hide, False),
    "4_1_button_infosub": epw.Button(text = "Bestätigen", font=epw.SysFont(font="Calibri", font_size=30), command = room_info_submit, height = 57, auto_size = False, corner_radius = 15, visible = False, screen = room_info_screen),
    "4_1_label_entrybackgr1": create_background_label(),
    "4_1_label_entrybackgr2": create_background_label(),
    "4_1_label_entrybackgr3": create_background_label(),
    "4_1_label_entrybackgr4": create_background_label(),
    "4_1_button_finishsub": epw.Button(text = "Bestätigen", font=epw.SysFont(font="Calibri", font_size=30), command = room_create_finish_submit, screen = room_info_screen),
    "4_1_button_finishcan": epw.Button(text = "Abbrechen", font=epw.SysFont(font="Calibri", font_size=30), command = room_create_finish_cancel, screen = room_info_screen),
    "4_1_label_starinfo": epw.Label(text = "*   max. eine Angabe\n** optionale Angabe", font=epw.SysFont(font="Calibri", font_size=20), alignment_spacing = 0, alignment = "left", screen = room_info_screen),
    # info icon
    "4_01_icon_infosymbol": epw.Surface(info_icon)
}

update_ui(widget_dic)
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
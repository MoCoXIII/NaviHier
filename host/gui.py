# gui.py
# Theo Glase
# 27.07.2026

import pygame
import easypygamewidgets as epw
import customtkinter
import ctypes
import ctypes.wintypes
import data_manager
from json_manager import *

def plan_selection(scenario):
    print("Wähle den Gebäudeplan aus")
    try: 
        plan_path = customtkinter.filedialog.askopenfilename(title = "Bitte wähle die Datei des Gebäudeplans aus", filetypes=[("All", "*.png;*.jpg;*.jpeg;*.webp"), ("PNG Datei", "*.png"), ("JPG Datei", "*.jpg"), ("JPEG Datei", "*.jpeg"), ("WEBP Datei", "*.webp")], initialdir=r"Gymnasium_Wernigerode")
        if plan_path == "": 
            raise FileNotFoundError
        return plan_path
    except FileNotFoundError: 
        if scenario == 1:
            exit(0)
        elif scenario == 2:
            raise FileNotFoundError

def plan_create(scenario):
    if scenario == 1:
        plan_path = plan_selection(1)
        data_manager.plan_path_memory = plan_path
        plan = pygame.image.load(fr"{plan_path}")
        plan_w, plan_h = plan.get_size()
        return plan, plan_w, plan_h, plan_path
    elif scenario == 2:
        try:
            plan_path = plan_selection(2)
        except FileNotFoundError:
            raise FileNotFoundError
        plan = pygame.image.load(fr"{plan_path}")
        plan_w, plan_h = plan.get_size()
        return plan, plan_w, plan_h, plan_path

def get_plan_values():
    plan = pygame.image.load(fr"{data_manager.plan_path}")
    plan_w, plan_h = plan.get_size()
    return plan, plan_w, plan_h

def place_plan():
    scaled_w = data_manager.realplan_w * data_manager.scale
    scaled_h = data_manager.realplan_h * data_manager.scale

    zone_x = data_manager.res_w * 0.30
    zone_y = data_manager.res_h * 0.25
    zone_w = data_manager.res_w * 0.40
    zone_h = data_manager.res_h * 0.50

    offset_x = (zone_w - scaled_w) // 2
    offset_y = (zone_h - scaled_h) // 2

    data_manager.widget_dic["4_012_surface_plan"].config(frames=[data_manager.plan])
    #data_manager.widget_dic["4_012_surface_plan"].scale(None)                                           # WORKAROUND BEI EPW UPDATE ENTFERNEN   
    data_manager.widget_dic["4_012_surface_plan"].scale(data_manager.scale)
    data_manager.widget_dic["4_012_surface_plan"].place(x=zone_x + offset_x, y=zone_y + offset_y)

    data_manager.plan_start_x = data_manager.widget_dic["4_012_surface_plan"].x
    data_manager.plan_start_y = data_manager.widget_dic["4_012_surface_plan"].y
    data_manager.plan_w = scaled_w
    data_manager.plan_h = scaled_h

def window_create():
    screen = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)
    data_manager.res_w = 1920
    data_manager.res_h = 1080
    pygame.display.set_caption("Raumeditor")
    epw.link_pygame_window(screen)
    hwnd = pygame.display.get_wm_info()["window"]                                                                           # hwnd (handle window): Window ID                                                                                    # ShowWindow: Funktion zum ändern des Zustandes eines Fensters // 0 = verstecken, 1 = normal anzeigen, 2 = minimieren, 3 = maximieren, 6 = minimieren in die Taskleiste

    screen_w = ctypes.windll.user32.GetSystemMetrics(0)
    screen_h = ctypes.windll.user32.GetSystemMetrics(1)
    if screen_w == 1920 and screen_h == 1080:
        ctypes.windll.user32.ShowWindow(hwnd, 3)
    screen = pygame.display.set_mode((1920, 1080))
    appereance_mode = ctypes.c_int(2)                                                                                       # appereance_mode: Variable zum Speichern des Anzeigemodus der Titelleiste // 0 = Light Mode, 1 = Dark Mode, 2 = Systemstandard
    ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, ctypes.byref(appereance_mode), ctypes.sizeof(appereance_mode))     # DwmSetWindowAttribute: Funktion zum Ändern des Anzeigemodus der Titelleiste       # ctypes.byref: Funktion zu Bestimmen des Speicherorts der Variable; ctypes.sizeof: Funktion zum Bestimmen des Speicherplatzes der Variable (int: 4)
    pygame.event.pump()
    print(screen_w, screen_h)
    return screen                                                                                                           # update von Pygame

def get_window_size():
    hwnd = pygame.display.get_wm_info()["window"]
    rect = ctypes.wintypes.RECT()
    ctypes.windll.user32.GetClientRect(hwnd, ctypes.byref(rect))
    width = rect.right - rect.left
    height = rect.bottom - rect.top
    return width, height   

def select_stairs():
    try:
        data_manager.plan, data_manager.realplan_w, data_manager.realplan_h, data_manager.plan_path = plan_create(2)
    except FileNotFoundError:
        return
    data_manager.second_plan = True
    data_manager.scale = get_scale()
    place_plan()
    stairs_ui()
    del_old_waypoints()
    place_waypoints()

def stairs_ui():
    data_manager.widget_dic["4_012_label_statuscontent"].config(text = "Wähle einen Wegpunkt")
    data_manager.widget_dic["4_2_screen_group"].hide()
    data_manager.widget_dic["4_3_screen_group"].hide()
    data_manager.widget_dic["4_3_screen_group2"].hide()
    data_manager.widget_dic["4_3_screen_group3"].hide()
    data_manager.widget_dic["4_3_screen_roomlist"].hide()
    data_manager.widget_dic["4_4_screen_group"].show()

def update_gen_factor():
    data_manager.gen_factor_w = data_manager.screen.get_width() / data_manager.res_w
    data_manager.gen_factor_h = data_manager.screen.get_height() / data_manager.res_h

def square_selected():
    if data_manager.shape == 0:
        data_manager.shape = 1
        data_manager.widget_dic["4_012_label_statuscontent"].config(text = "Quadratischer Raumtyp Ausgewählt")

def polygon_selected():
    if data_manager.shape == 0:
        data_manager.shape = 2
        data_manager.widget_dic["4_012_label_statuscontent"].config(text = "Polygonaler Raumtyp Ausgewählt")

def waypoint_selected():
    if data_manager.shape == 0:
        data_manager.shape = 3
        data_manager.widget_dic["4_012_label_statuscontent"].config(text = "Waypoint Ausgewählt")
        data_manager.widget_dic["4_0_screen_group"].hide()
        data_manager.widget_dic["4_2_screen_group"].show()
        place_waypoints()

def waypoint_edit_back():
    data_manager.widget_dic["4_2_screen_group"].hide()
    data_manager.widget_dic["4_3_screen_group"].hide()
    data_manager.widget_dic["4_3_screen_group2"].hide()
    data_manager.widget_dic["4_3_screen_group3"].hide()
    data_manager.widget_dic["4_3_screen_grou4"].hide()
    data_manager.widget_dic["4_0_screen_group"].show()
    data_manager.last_wp = ""
    data_manager.shape = 0
    del_old_waypoints()
    

def place_waypoints():
    data_manager.connections_list = get_connection_list()
    waypoint_asset = pygame.image.load("assets/waypoint.png")
    wp_list = get_waypoint_list()
    for name, inf in wp_list.items():

        data_manager.widget_dic[name] = epw.Surface(frames=[waypoint_asset], anchor_x="center", anchor_y="center", layer=3000).bind("<RELEASE>", lambda name=name: click_waypoint(name))
        data_manager.widget_dic[name].scale(0.02, 1)
        data_manager.widget_geometry[name] = {
            "x": data_manager.plan_start_x + inf[0] * data_manager.scale,
            "y": data_manager.plan_start_y + inf[1] * data_manager.scale
        }
        data_manager.waypoint_list.append(name)
    place_widgets()

def del_old_waypoints():
    for name in data_manager.waypoint_list:
        data_manager.widget_dic[name].delete()
        del data_manager.widget_dic[name]
        del data_manager.widget_geometry[name]
    data_manager.waypoint_list.clear()

def screenwidth_percent(value):
    return data_manager.screen.get_width() * value

def screenheight_percent(value):
    return data_manager.screen.get_height() * value

def create_background_label():
    return epw.Label(text = "", screen = data_manager.room_info_screen, active_unpressed_background_color = (50, 50, 50), 
                                                            active_hover_background_color = (50, 50, 50),
                                                            active_pressed_background_color = (50, 50, 50),
                                                            top_left_corner_radius = 15, 
                                                            top_right_corner_radius = 15, 
                                                            bottom_left_corner_radius = 15, 
                                                            bottom_right_corner_radius = 15,
                                                            min_width =  screenwidth_percent(0.3) - 120,
                                                            layer = 0)

def delay_4_1_button_infosub():
    data_manager.widget_dic["4_1_button_infosub"].config(visible = True)

def room_create_finish_submit():
    save_data(data_manager.plan_path, 
              data_manager.shape, 
              data_manager.id_answer_list, 
              data_manager.name_answer_list, 
              data_manager.prof_answer_list, 
              data_manager.extrainfo_answer_list)

def room_create_submit():
    data_manager.widget_dic["4_0_screen_group"].hide()
    data_manager.widget_dic["4_1_screen_group"].show()

def room_create_cancel():
    data_manager.shape = 0
    data_manager.s_coords.clear()
    data_manager.p_coords.clear()
    data_manager.s_coords_count = 0
    data_manager.p_coords_count = 0
    data_manager.widget_dic["4_012_label_statuscontent"].config(text = "Zurücksetzen des Raumtyps")

def room_info_submit():
    if data_manager.widget_dic["4_1_button_infosub"].y == screenheight_percent(0.4):
        data_manager.id_answer_list.clear()
        data_manager.id_answer_list.append(data_manager.widget_dic["4_1_entry_id"].get())
        data_manager.widget_dic["4_1_entry_id"].config(text="")
    elif data_manager.widget_dic["4_1_button_infosub"].y == screenheight_percent(0.5):
        data_manager.name_answer_list.append(data_manager.widget_dic["4_1_entry_name"].get())
        data_manager.widget_dic["4_1_entry_name"].config(text="")
    elif data_manager.widget_dic["4_1_button_infosub"].y == screenheight_percent(0.6):
        data_manager.prof_answer_list.append(data_manager.widget_dic["4_1_entry_prof"].get())
        data_manager.widget_dic["4_1_entry_prof"].config(text="")
    elif data_manager.widget_dic["4_1_button_infosub"].y == screenheight_percent(0.7):
        data_manager.extrainfo_answer_list.append(data_manager.widget_dic["4_1_entry_extrainfo"].get())
        data_manager.widget_dic["4_1_entry_extrainfo"].config(text="")
    data_manager.widget_dic["4_1_button_infosub"].config(visible=False)

def room_create_finish_cancel():
    data_manager.id_answer_list.clear()
    data_manager.name_answer_list.clear()
    data_manager.prof_answer_list.clear()
    data_manager.extrainfo_answer_list.clear()
    room_create_cancel()
    data_manager.widget_dic["4_1_entry_id"].config(text="")
    data_manager.widget_dic["4_1_entry_name"].config(text="")
    data_manager.widget_dic["4_1_entry_prof"].config(text="")
    data_manager.widget_dic["4_1_entry_extrainfo"].config(text="")
    data_manager.widget_dic["4_1_screen_group"].hide()
    data_manager.widget_dic["4_0_screen_group"].show()
    data_manager.widget_dic["4_012_label_statuscontent"].config(text="Zurücksetzen der Raumerstellung")

def show_4_1_button_infosub(info_type):
    epw.schedule(delay_4_1_button_infosub, 1)
    btn_w = data_manager.widget_dic["4_1_button_infosub"].width
    target_w = int(data_manager.res_w * - 60 - btn_w)
    
    data_manager.widget_dic["4_1_entry_id"].config(width=target_w)
    data_manager.widget_dic["4_1_entry_name"].config(width=target_w)
    data_manager.widget_dic["4_1_entry_prof"].config(width=target_w)
    data_manager.widget_dic["4_1_entry_extrainfo"].config(width=screenwidth_percent(0.3) - 120 - btn_w)
    
    if info_type == "id":
        data_manager.widget_dic["4_1_button_infosub"].place(x=target_w, y=data_manager.widget_dic["4_1_entry_id"].y)
    elif info_type == "name":
        data_manager.widget_dic["4_1_button_infosub"].place(x=target_w, y=data_manager.widget_dic["4_1_entry_name"].y)
    elif info_type == "prof":
        data_manager.widget_dic["4_1_button_infosub"].place(x=target_w, y=data_manager.widget_dic["4_1_entry_prof"].y)
    elif info_type == "extra":
        data_manager.widget_dic["4_1_button_infosub"].place(x=target_w, y=data_manager.widget_dic["4_1_entry_extrainfo"].y)

def room_info_submit_button_hide():
    pos = pygame.mouse.get_pos()
    button = data_manager.widget_dic["4_1_button_infosub"]
    if button.x <= pos[0] <= button.x + button.width and button.y <= pos[1] <= button.y + button.height:
        pass
    else:
        button.config(visible=False)
        default_w = screenwidth_percent(0.3) - 120
        data_manager.widget_dic["4_1_entry_id"].config(width=default_w)
        data_manager.widget_dic["4_1_entry_name"].config(width=default_w)
        data_manager.widget_dic["4_1_entry_prof"].config(width=default_w)
        data_manager.widget_dic["4_1_entry_extrainfo"].config(width=default_w)

def poi_submit():
    name = data_manager.widget_dic["4_3_label_dropdown"].text
    try: add_poi(name, data_manager.plan_path)
    except: pass
    data_manager.widget_dic["4_3_screen_roomlist"].hide()

def stairs_submit():
    pass

def poi():
    if not data_manager.add_poi:
        data_manager.widget_dic["4_3_screen_group2"].show()
        data_manager.widget_dic["4_3_button_poi"].config(text="Zielort entfernen")
        data_manager.add_poi = True
    elif data_manager.add_poi:
        data_manager.widget_dic["4_3_screen_group2"].hide()
        data_manager.widget_dic["4_3_screen_roomlist"].hide()
        data_manager.widget_dic["4_3_button_poi"].config(text="Zielort hinzufügen")
        data_manager.add_poi = False
        del_poi()

def stairs():
    if not data_manager.add_stairs:
        data_manager.widget_dic["4_3_screen_group3"].show()
        data_manager.widget_dic["4_3_button_stairs"].config(text="Treppenverbindung entfernen")
        data_manager.add_stairs = True
        print(data_manager.add_stairs)
    elif data_manager.add_stairs:
        data_manager.widget_dic["4_3_screen_group3"].hide()
        data_manager.widget_dic["4_3_button_stairs"].config(text="Treppenverbindung hinzufügen")
        data_manager.add_stairs = False
        print(data_manager.add_stairs)

def add_stairs_connection():
    data = {
        "start": data_manager.wp_memory,
        "end": data_manager.wp_name
    }
    data_manager.connections_list.append(data)
    add_connection_json(data)
    data_manager.second_plan = False
    data_manager.plan_path = data_manager.plan_path_memory
    data_manager.plan, data_manager.realplan_w, data_manager.realplan_h = get_plan_values()
    print(data_manager.plan, data_manager.realplan_w, data_manager.realplan_h)
    data_manager.scale = get_scale()
    place_plan()
    del_old_waypoints()
    place_waypoints()
    place_widgets()
    data_manager.widget_dic["4_4_screen_group"].hide()
    data_manager.widget_dic["4_2_screen_group"].show()
    data_manager.widget_dic["4_3_screen_group"].show()
    data_manager.widget_dic["4_3_screen_group2"].show()
    data_manager.widget_dic["4_3_screen_group3"].show()
    data_manager.widget_dic["4_3_label_waypoint"].config(text=f"Wegpunkt: {data_manager.wp_memory}")


def poi_select(self):
    data_manager.widget_dic["4_3_label_dropdown"].config(text=self.text)

def show_list():
    room_list = get_room_list(data_manager.plan_path)
    add_room_list = []
    label_max_y = data_manager.res_h * 0.743
    for i in range(len(room_list)):
        if room_list[i] not in data_manager.widget_dic:
            add_room_list.append(room_list[i])
        elif data_manager.widget_geometry[room_list[i]]["y"] > label_max_y:
            label_max_y = data_manager.widget_geometry[room_list[i]]["y"]

    for i in range(len(add_room_list)):
        data_manager.widget_dic[add_room_list[i]] = epw.Label(text=add_room_list[i], font=epw.SysFont(font="Calibri", font_size=30), screen=data_manager.room_list).bind("<RELEASE>", lambda self: poi_select(self))
        data_manager.widget_geometry[add_room_list[i]] = {"x": data_manager.plan_start_x + data_manager.plan_w + 60, "y": label_max_y}
        label_max_y += 50
    place_widgets()
    data_manager.widget_dic["4_3_screen_roomlist"].show()

def del_waypoint(wp, type):
    del_con_list = [
        con for con in data_manager.connections_list if con["start"] == wp or con["end"] == wp
    ]
    for con in del_con_list:
        del_connection_json(con)
        data_manager.connections_list.remove(con)
    if data_manager.w_coords_count > 1:
        data_manager.w_coords.pop()
        data_manager.w_coords.pop()
    data_manager.w_coords_count -= 1
    data_manager.widget_dic[wp].delete()
    data_manager.waypoint_list.remove(wp)
    if type == 0:
        if len(data_manager.waypoint_list) > 0:
            data_manager.last_wp = data_manager.waypoint_list[-1]
        else:
            data_manager.last_wp = ""
    elif type == 1:
        data_manager.last_wp = ""
    del data_manager.widget_dic[wp]
    del data_manager.widget_geometry[wp]
    del_waypoint_json(wp)

def click_waypoint(name):
    data_manager.wp_memory = data_manager.wp_name
    data_manager.wp_name = name
    if not data_manager.r_clicked:
        add = True
        if data_manager.new_line:
            if data_manager.last_wp == "":
                data_manager.last_wp = name
            else:
                data = {
                    "start": data_manager.last_wp,
                    "end": name
                }
                for con in data_manager.connections_list:
                    if (con["start"] == data["start"] and con["end"] == data["end"]) or (con["start"] == data["end"] and con["end"] == data["start"]):
                        add = False
                        break
                if add:
                    add_connection_json(data)
                    data_manager.connections_list.append(data)
                data_manager.last_wp = name
                add = True
        elif not data_manager.second_plan: 
            data_manager.widget_dic["4_3_screen_group"].show()
            data_manager.widget_dic["4_3_label_waypoint"].config(text=f"Wegpunkt: {data_manager.wp_name}")
            place_widgets()
        else:
            data_manager.widget_dic["4_4_label_waypoint"].config(text=f"Wegpunkt: {data_manager.wp_name}")
            data_manager.widget_dic["4_4_button_select"].config(state="enabled")
            place_widgets()

def wp_newline():
    data_manager.widget_dic["4_012_label_statuscontent"].config(text="Wegpunktbearbeitung")
    data_manager.widget_dic["4_2_button_newline"].config(state="disabled")
    data_manager.widget_dic["4_2_button_newlinecan"].config(state="enabled")
    data_manager.widget_dic["4_3_screen_group"].hide()
    data_manager.widget_dic["4_3_screen_group2"].hide()
    data_manager.widget_dic["4_3_screen_group3"].hide()
    data_manager.new_line = True
    data_manager.last_wp = ""
def wp_newline_cancel():
    data_manager.widget_dic["4_012_label_statuscontent"].config(text="Wegpunktbearbeitung abgebrochen")
    data_manager.widget_dic["4_2_button_newline"].config(state="enabled")
    data_manager.widget_dic["4_2_button_newlinecan"].config(state="disabled")
    data_manager.new_line = False

def place_widgets():
    for name in data_manager.widget_geometry.keys():
        if "min_width" in data_manager.widget_geometry[name].keys():
            data_manager.widget_dic[name].config(min_width=data_manager.widget_geometry[name]["min_width"])
        if "width" in data_manager.widget_geometry[name].keys():
            data_manager.widget_dic[name].config(width=data_manager.widget_geometry[name]["width"])
        if "height" in data_manager.widget_geometry[name].keys():
            data_manager.widget_dic[name].config(height=data_manager.widget_geometry[name]["height"])
        if "x" in data_manager.widget_geometry[name].keys() and "y" in data_manager.widget_geometry[name].keys():
            data_manager.widget_dic[name].place(x=data_manager.widget_geometry[name]["x"], y=data_manager.widget_geometry[name]["y"])

def get_scale():
    plan_factor = min(data_manager.res_w * 0.40 / data_manager.realplan_w, data_manager.res_h * 0.50 / data_manager.realplan_h)
    return plan_factor

def draw_lines():
    if data_manager.shape == 3:
        for con in range(len(data_manager.connections_list)):
            try:
                start = data_manager.connections_list[con]["start"]
                end = data_manager.connections_list[con]["end"]
                start_pos = (data_manager.widget_dic[start].x + data_manager.widget_dic[start].width // 2, data_manager.widget_dic[start].y + data_manager.widget_dic[start].height // 2)
                end_pos = (data_manager.widget_dic[end].x + data_manager.widget_dic[end].width // 2, data_manager.widget_dic[end].y + data_manager.widget_dic[end].height // 2)
                pygame.draw.aaline(surface=data_manager.screen, color=(207, 91, 25), start_pos=start_pos, end_pos=end_pos, width=2)
            except KeyError:
                continue
        if data_manager.new_line and len(data_manager.waypoint_list) >= 1 and data_manager.last_wp != "":
            mx, my = pygame.mouse.get_pos()
            if data_manager.plan_start_x <= mx <= data_manager.plan_start_x + data_manager.plan_w and data_manager.plan_start_y <= my <= data_manager.plan_start_y + data_manager.plan_h:
                pygame.draw.aaline(surface=data_manager.screen, color=(207, 91, 25), 
                                   start_pos=(data_manager.widget_dic[data_manager.last_wp].x + data_manager.widget_dic[data_manager.last_wp].width // 2, 
                                              data_manager.widget_dic[data_manager.last_wp].y + data_manager.widget_dic[data_manager.last_wp].height // 2), 
                                   end_pos=(mx, my), width=2)
epw.create_pygame_layer(draw_lines, 2000)

def get_widget_geometry():
    return {
        "4_012_label_maintitle": {
            "x": data_manager.res_w // 2 - data_manager.widget_dic["4_012_label_maintitle"].width // 2,
            "y": data_manager.res_h * 0.125 - data_manager.widget_dic["4_012_label_maintitle"].height // 2,
            "font_size": 65,
        },
        "4_012_label_statustitle": {
            "x": 0.3 * data_manager.res_w,
            "y": 0.8 * data_manager.res_h,
            "font_size": 40,
        },
        "4_012_label_statuscontent": {
            "x": 0.3 * data_manager.res_w,
            "y": data_manager.res_h * 0.8 + data_manager.widget_dic["4_012_label_statustitle"].height,
            "font_size": 25,
            "min_width": 3 * data_manager.plan_w / 4,
        },
        "4_0_label_roomtype": {
            "x": data_manager.res_w * 0.15 - data_manager.widget_dic["4_0_label_roomtype"].width // 2,
            "y": data_manager.res_h * 0.25,
            "font_size": 40,
        },
        "4_0_label_squaretype": {
            "x": 60,
            "y": data_manager.res_h * 0.45 - data_manager.widget_dic["4_0_label_squaretype"].height,
            "font_size": 30,
        },
        "4_0_button_squaretype": {
            "x": 60,
            "y": data_manager.res_h * 0.45,
            "font_size": 30,
        },
        "4_0_label_polytype": {
            "x": 60,
            "y": data_manager.res_h * 0.55 - data_manager.widget_dic["4_0_label_polytype"].height,
            "font_size": 30,
        },
        "4_0_button_polytype": {
            "x": 60,
            "y": data_manager.res_h * 0.55,
            "font_size": 30,
        },
        "4_0_label_waytype": {
            "x": 60,
            "y": data_manager.res_h * 0.65 - data_manager.widget_dic["4_0_label_waytype"].height,
            "font_size": 30,
        },
        "4_0_button_waytype": {
            "x": 60,
            "y": data_manager.res_h * 0.65,
            "font_size": 30,
        },
        "4_0_button_createsub": {
            "x": data_manager.plan_start_x // 2 + 40,
            "y": data_manager.res_h * 0.45,
            "font_size": 30,
        },
        "4_0_button_createcan": {
            "x": data_manager.plan_start_x // 2 + 40,
            "y": data_manager.res_h * 0.50 + 10,
            "font_size": 30,
        },
        "4_1_button_infosub": {
            "font_size": 30,
        },
        "4_1_label_infotitle": {
            "x": data_manager.res_w * 0.15 - data_manager.widget_dic["4_1_label_infotitle"].width // 2,
            "y": data_manager.res_h * 0.25,
            "font_size": 40,
        },
        "4_1_label_id": {
            "x": 60,
            "y": data_manager.res_h * 0.4 - data_manager.widget_dic["4_1_label_id"].height,
            "font_size": 30,
        },
        "4_1_label_entrybackgr1": {
            "x": 60,
            "y": data_manager.res_h * 0.4,
            "font_size": 30,
            "min_width": (data_manager.res_w * 0.3) - 120,
        },
        "4_1_entry_id": {
            "x": 60,
            "y": data_manager.res_h * 0.4,
            "font_size": 30,
            "height": 57,
            "width": (data_manager.res_w * 0.3) - 120,
        },
        "4_1_label_name": {
            "x": 60,
            "y": data_manager.res_h * 0.5 - data_manager.widget_dic["4_1_label_name"].height,
            "font_size": 30,
        },
        "4_1_label_entrybackgr2": {
            "x": 60,
            "y": data_manager.res_h * 0.5,
            "font_size": 30,
            "min_width": (data_manager.res_w * 0.3) - 120,
        },
        "4_1_entry_name": {
            "x": 60,
            "y": data_manager.res_h * 0.5,
            "font_size": 30,
            "height": 57,
            "width": (data_manager.res_w * 0.3) - 120,
        },
        "4_1_label_prof": {
            "x": 60,
            "y": data_manager.res_h * 0.6 - data_manager.widget_dic["4_1_label_prof"].height,
            "font_size": 30,
        },
        "4_1_label_entrybackgr3": {
            "x": 60,
            "y": data_manager.res_h * 0.6,
            "font_size": 30,
            "min_width": (data_manager.res_w * 0.3) - 120,
        },
        "4_1_entry_prof": {
            "x": 60,
            "y": data_manager.res_h * 0.6,
            "font_size": 30,
            "height": 57,
            "width": (data_manager.res_w * 0.3) - 120,
        },
        "4_1_label_extrainfo": {
            "x": 60,
            "y": data_manager.res_h * 0.7 - data_manager.widget_dic["4_1_label_extrainfo"].height,
            "font_size": 30,
        },
        "4_1_label_entrybackgr4": {
            "x": 60,
            "y": data_manager.res_h * 0.7,
            "font_size": 30,
            "min_width": (data_manager.res_w * 0.3) - 120,
        },
        "4_1_entry_extrainfo": {
            "x": 60,
            "y": data_manager.res_h * 0.7,
            "font_size": 30,
            "height": 57,
            "width": (data_manager.res_w * 0.3) - 120,
        },
        "4_1_button_finishsub": {
            "x": 60,
            "y": data_manager.res_h * 0.825 - data_manager.widget_dic["4_1_button_finishsub"].height,
            "font_size": 30,
        },
        "4_1_button_finishcan": {
            "x": 240,
            "y": data_manager.res_h * 0.825 - data_manager.widget_dic["4_1_button_finishcan"].height,
            "font_size": 30,
        },
        "4_1_label_starinfo": {
            "x": 60,
            "y": data_manager.res_h * 0.925 - data_manager.widget_dic["4_1_label_starinfo"].height,
            "font_size": 20,
        },
        "4_2_label_createtitle": {
            "x": data_manager.res_w * 0.15 - data_manager.widget_dic["4_2_label_createtitle"].width // 2,
            "y": data_manager.res_h * 0.25,
            "font_size": 40, 
        },
        "4_2_button_newline": {
            "x": 60,
            "y": data_manager.res_h * 0.4,
            "font_size": 30,
        },
        "4_2_button_newlinecan": {
            "x": 60,
            "y": data_manager.res_h * 0.475,
            "font_size": 30,
        },
        "4_3_label_title": {
            "x": data_manager.res_w * 0.85 - data_manager.widget_dic["4_3_label_title"].width // 2,
            "y": data_manager.res_h * 0.25,
            "font_size": 40,
        },
        "4_3_label_waypoint": {
            "x": data_manager.res_w * 0.85 - data_manager.widget_dic["4_3_label_waypoint"].width // 2,
            "y": data_manager.res_h * 0.3,
            "font_size": 30,
        },
        "4_3_button_poi": {
            "x": data_manager.plan_start_x + data_manager.plan_w + 60,
            "y": data_manager.res_h * 0.6,
            "font_size": 30,
            "min_width": 250
        },
        "4_3_label_dropdown": {
            "x": data_manager.plan_start_x + data_manager.plan_w + 60,
            "y": data_manager.res_h * 0.7,
            "font_size": 30,
            "min_width": 450
        },
        "4_3_button_poiaccept": {
            "x": data_manager.plan_start_x + data_manager.plan_w + 600,
            "y": data_manager.res_h * 0.7,
            "font_size": 30
        },
        "4_3_button_stairs":{
            "x": data_manager.plan_start_x + data_manager.plan_w + 60,
            "y": data_manager.res_h * 0.4,
            "font_size": 30,
            "min_width": 300
        },
        "4_3_label_addstairs": {
            "x": data_manager.plan_start_x + data_manager.plan_w + 60,
            "y": data_manager.res_h * 0.5,
            "font_size": 30,
            "min_width": 450
        },
        "4_3_button_stairsaccept": {
            "x": data_manager.plan_start_x + data_manager.plan_w + 600,
            "y": data_manager.res_h * 0.5,
            "font_size": 30
        },
        "4_3_button_back": {
            "x": 60,
            "y": data_manager.res_h * 0.8 + data_manager.widget_dic["4_012_label_statustitle"].height,
            "font_size": 30
        },
        "4_4_label_waypoint": {
            "x": data_manager.res_w * 0.85 - data_manager.widget_dic["4_4_label_waypoint"].width // 2,
            "y": data_manager.res_h * 0.25,
            "font_size": 30
        },
        "4_4_button_select": {
            "x": data_manager.plan_start_x + data_manager.plan_w + 60,
            "y": data_manager.res_h * 0.35,
        }
    }
def create_widgets(plan):
    data_manager.room_creation_screen = epw.Screen(visible=True)
    data_manager.room_info_screen = epw.Screen(visible=False)
    data_manager.waypoint_creation_screen = epw.Screen(visible=False)
    data_manager.waypoint_edit_screen = epw.Screen(visible=False)
    data_manager.room_list = epw.Screen(visible=True)
    data_manager.poi_widgets = epw.Screen(visible=False)
    data_manager.stairs_widgets = epw.Screen(visible=False)
    data_manager.stairs_waypoint = epw.Screen(visible=False)
    
    widget_dic = {
        "4_0_screen_group": data_manager.room_creation_screen,
        "4_1_screen_group": data_manager.room_info_screen,
        "4_2_screen_group": data_manager.waypoint_creation_screen,
        "4_3_screen_group": data_manager.waypoint_edit_screen,
        "4_3_screen_group2": data_manager.poi_widgets,
        "4_3_screen_group3": data_manager.stairs_widgets,
        "4_4_screen_group": data_manager.stairs_waypoint,
        "4_012_surface_plan": epw.Surface(frames=[plan]),
        "4_012_label_maintitle": epw.Label(text="Raumeditor", font=epw.SysFont(font="Calibri", font_size=65)),
        "4_012_label_statustitle": epw.Label(text="Status", font=epw.SysFont(font="Calibri", font_size=40, bold=True), alignment_spacing=0, alignment="left"),
        "4_012_label_statuscontent": epw.Label(text="", font=epw.SysFont(font="Calibri", font_size=30), alignment="left", active_unpressed_background_color=(50, 50, 50), active_hover_background_color=(50, 50, 50), active_pressed_background_color=(50, 50, 50), top_left_corner_radius=15, top_right_corner_radius=15, bottom_left_corner_radius=15, bottom_right_corner_radius=15),
        "4_0_label_roomtype": epw.Label(text="Raumtyp -\n Wegpunktauswahl", font=epw.SysFont(font="Calibri", font_size=40, bold=True), screen=data_manager.room_creation_screen),
        "4_0_label_squaretype": epw.Label(text="Quadratischer Raum", font=epw.SysFont(font="Calibri", font_size=30), alignment_spacing=0, alignment="left", screen=data_manager.room_creation_screen),
        "4_0_button_squaretype": epw.Button(text="Auswählen", font=epw.SysFont(font="Calibri", font_size=30), command=square_selected, screen=data_manager.room_creation_screen),
        "4_0_label_polytype": epw.Label(text="Polygon Raum", font=epw.SysFont(font="Calibri", font_size=30), alignment_spacing=0, alignment="left", screen=data_manager.room_creation_screen),
        "4_0_button_polytype": epw.Button(text="Auswählen", font=epw.SysFont(font="Calibri", font_size=30), command=polygon_selected, screen=data_manager.room_creation_screen),
        "4_0_label_waytype": epw.Label(text="Wegpunkt", font=epw.SysFont(font="Calibri", font_size=30), alignment_spacing=0, alignment="left", screen=data_manager.room_creation_screen),
        "4_0_button_waytype": epw.Button(text="Auswählen", font=epw.SysFont(font="Calibri", font_size=30), command=waypoint_selected, screen=data_manager.room_creation_screen),
        "4_0_button_createsub": epw.Button(text="Bestätigen", font=epw.SysFont(font="Calibri", font_size=30), command=room_create_submit, screen=data_manager.room_creation_screen),
        "4_0_button_createcan": epw.Button(text="Abbrechen", font=epw.SysFont(font="Calibri", font_size=30), command=room_create_cancel, screen=data_manager.room_creation_screen),
        "4_1_label_infotitle": epw.Label(text="Rauminformationen", font=epw.SysFont(font="Calibri", font_size=40, bold=True), screen=data_manager.room_info_screen),
        "4_1_label_id": epw.Label(text="Raum Nr / ID *", font=epw.SysFont(font="Calibri", font_size=30), alignment_spacing=0, alignment="left", screen=data_manager.room_info_screen),
        "4_1_entry_id": epw.Entry(font=epw.SysFont(font="Calibri", font_size=30), height=57, hide_background=True, hide_border=True, auto_size=False, screen=data_manager.room_info_screen).bind(epw.FOCUS_IN, lambda: show_4_1_button_infosub("id")).bind(epw.FOCUS_OUT, room_info_submit_button_hide, False),
        "4_1_label_name": epw.Label(text="Raum Name **", font=epw.SysFont(font="Calibri", font_size=30), alignment_spacing=0, alignment="left", screen=data_manager.room_info_screen),
        "4_1_entry_name": epw.Entry(font=epw.SysFont(font="Calibri", font_size=30), height=57, hide_background=True, hide_border=True, auto_size=False, screen=data_manager.room_info_screen).bind(epw.FOCUS_IN, lambda: show_4_1_button_infosub("name")).bind(epw.FOCUS_OUT, room_info_submit_button_hide, False),
        "4_1_label_prof": epw.Label(text="Raum Lehrer / Professor **", font=epw.SysFont(font="Calibri", font_size=30), alignment_spacing=0, alignment="left", screen=data_manager.room_info_screen),
        "4_1_entry_prof": epw.Entry(font=epw.SysFont(font="Calibri", font_size=30), height=57, hide_background=True, hide_border=True, auto_size=False, screen=data_manager.room_info_screen).bind(epw.FOCUS_IN, lambda: show_4_1_button_infosub("prof")).bind(epw.FOCUS_OUT, room_info_submit_button_hide, False),
        "4_1_label_extrainfo": epw.Label(text="Raum Zusatzinformationen **", font=epw.SysFont(font="Calibri", font_size=30), alignment_spacing=0, alignment="left", screen=data_manager.room_info_screen),
        "4_1_entry_extrainfo": epw.Entry(font=epw.SysFont(font="Calibri", font_size=30), height=57, hide_background=True, hide_border=True, auto_size=False, screen=data_manager.room_info_screen).bind(epw.FOCUS_IN, lambda: show_4_1_button_infosub("extra")).bind(epw.FOCUS_OUT, room_info_submit_button_hide, False),
        "4_1_button_infosub": epw.Button(text="Bestätigen", font=epw.SysFont(font="Calibri", font_size=30), command=room_info_submit, height=57, auto_size=False, corner_radius=15, visible=False, screen=data_manager.room_info_screen),
        "4_1_label_entrybackgr1": create_background_label(),
        "4_1_label_entrybackgr2": create_background_label(),
        "4_1_label_entrybackgr3": create_background_label(),
        "4_1_label_entrybackgr4": create_background_label(),
        "4_1_button_finishsub": epw.Button(text="Bestätigen", font=epw.SysFont(font="Calibri", font_size=30), command=room_create_finish_submit, screen=data_manager.room_info_screen),
        "4_1_button_finishcan": epw.Button(text="Abbrechen", font=epw.SysFont(font="Calibri", font_size=30), command=room_create_finish_cancel, screen=data_manager.room_info_screen),
        "4_1_label_starinfo": epw.Label(text="* max. eine Angabe\n** optionale Angabe", font=epw.SysFont(font="Calibri", font_size=20), alignment_spacing=0, alignment="left", screen=data_manager.room_info_screen),
        "4_2_label_createtitle": epw.Label(text="Wegpunkterstellung", font=epw.SysFont(font="Calibri", font_size=40, bold=True), screen=data_manager.waypoint_creation_screen),
        "4_2_button_newline": epw.Button(text="Wegpunktbearbeitung", font=epw.SysFont(font="Calibri", font_size=30), command=wp_newline, screen=data_manager.waypoint_creation_screen),
        "4_2_button_newlinecan": epw.Button(text="Abbrechen", font=epw.SysFont(font="Calibri", font_size=30), command=wp_newline_cancel, state="disabled", screen=data_manager.waypoint_creation_screen),
        "4_3_label_title": epw.Label(text="Wegpunktbearbeitung", font=epw.SysFont(font="Calibri", font_size=40, bold=True), screen=data_manager.waypoint_edit_screen),
        "4_3_label_waypoint": epw.Label(text=f"Wegpunkt:", font=epw.SysFont(font="Calibri", font_size=30), alignment="left", screen=data_manager.waypoint_edit_screen),
        "4_3_button_poi": epw.Button(text="Zielort hinzufügen", font=epw.SysFont(font="Calibri", font_size=30), command=poi, alignment="left", screen=data_manager.waypoint_edit_screen),
        "4_3_label_dropdown": epw.Label(text="", font=epw.SysFont(font="Calibri", font_size=30), alignment="left", active_unpressed_background_color=(50, 50, 50), active_hover_background_color=(50, 50, 50), active_pressed_background_color=(50, 50, 50), top_left_corner_radius=15, top_right_corner_radius=15, bottom_left_corner_radius=15, bottom_right_corner_radius=15, screen=data_manager.poi_widgets).bind("<RELEASE>", show_list),
        "4_3_button_poiaccept": epw.Button(text="Bestätigen", font=epw.SysFont(font="Calibri", font_size=30), command=poi_submit, screen=data_manager.poi_widgets),
        "4_3_screen_roomlist": data_manager.room_list,
        "4_3_button_stairs": epw.Button(text="Treppenverbindung hinzufügen", font=epw.SysFont(font="Calibri", font_size=30), command=stairs, alignment="left", screen=data_manager.waypoint_edit_screen),
        "4_3_label_addstairs": epw.Label(text="", font=epw.SysFont(font="Calibri", font_size=30), active_unpressed_background_color=(50, 50, 50), active_hover_background_color=(50, 50, 50), active_pressed_background_color=(50, 50, 50), top_left_corner_radius=15, top_right_corner_radius=15, bottom_left_corner_radius=15, bottom_right_corner_radius=15, screen=data_manager.stairs_widgets).bind("<RELEASE>", select_stairs, False),
        "4_3_button_stairsaccept": epw.Button(text="Bestätigen", font=epw.SysFont(font="Calibri", font_size=30), command=stairs_submit, screen=data_manager.stairs_widgets),
        "4_3_button_back": epw.Button(text="Zurück", font=epw.SysFont(font="Calibri", font_size=30), command=waypoint_edit_back, screen=data_manager.waypoint_creation_screen),
        "4_4_label_waypoint": epw.Label(text=f"Treppenwegpunkt:", font=epw.SysFont(font="Calibri", font_size=30), alignment="left", screen=data_manager.stairs_waypoint),
        "4_4_button_select": epw.Button(text="Verbindung erstellen", font=epw.SysFont(font="Calibri", font_size=30), command=add_stairs_connection, alignment="left", state="disabled", screen=data_manager.stairs_waypoint),
    }
    return widget_dic

def get_widget_dic(plan=None):
    if not data_manager.widget_dic and plan is not None:
        data_manager.widget_dic.update(create_widgets(plan))
    return data_manager.widget_dic
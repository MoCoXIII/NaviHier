# gui.py
# Theo Glase
# 27.07.2026

import pygame
import easypygamewidgets as epw
import customtkinter
import ctypes
import data_manager
from json_manager import save_data, get_room_list, add_poi, get_waypoint_list, get_connection_list, del_connection_json, del_waypoint_json, add_connection_json

def plan_selection():
    print("Wähle den Gebäudeplan aus")
    try: 
        plan_path = customtkinter.filedialog.askopenfilename(title = "Bitte wähle die Datei des Gebäudeplans aus", filetypes=[("All", "*.png;*.jpg;*.jpeg;*.webp"), ("PNG Datei", "*.png"), ("JPG Datei", "*.jpg"), ("JPEG Datei", "*.jpeg"), ("WEBP Datei", "*.webp")], initialdir=r"Gymnasium_Wernigerode")
        if plan_path == "": 
            raise FileNotFoundError
        return plan_path
    except FileNotFoundError: 
        exit(0)

def plan_create():
    plan_path = plan_selection()
    plan = pygame.image.load(fr"{plan_path}")
    plan_w, plan_h = plan.get_size()
    return plan, plan_w, plan_h, plan_path

def window_create():
    screen = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h), pygame.RESIZABLE)
    pygame.display.set_caption("Raumeditor")
    epw.link_pygame_window(screen)
    hwnd = pygame.display.get_wm_info()["window"]                                                                           # hwnd (handle window): Window ID      
    ctypes.windll.user32.ShowWindow(hwnd, 3)                                                                                # ShowWindow: Funktion zum ändern des Zustandes eines Fensters // 0 = verstecken, 1 = normal anzeigen, 2 = minimieren, 3 = maximieren, 6 = minimieren in die Taskleiste
    appereance_mode = ctypes.c_int(2)                                                                                       # appereance_mode: Variable zum Speichern des Anzeigemodus der Titelleiste // 0 = Light Mode, 1 = Dark Mode, 2 = Systemstandard
    ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, ctypes.byref(appereance_mode), ctypes.sizeof(appereance_mode))     # DwmSetWindowAttribute: Funktion zum Ändern des Anzeigemodus der Titelleiste       # ctypes.byref: Funktion zu Bestimmen des Speicherorts der Variable; ctypes.sizeof: Funktion zum Bestimmen des Speicherplatzes der Variable (int: 4)
    pygame.event.pump()
    return screen                                                                                                           # update von Pygame

def update_gen_factor():
    data_manager.gen_factor_w = data_manager.screen.get_width() / data_manager.ref_w
    data_manager.gen_factor_h = data_manager.screen.get_height() / data_manager.ref_h

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
        data_manager.connections_list = get_connection_list()

        waypoint_asset = pygame.image.load("assets/waypoint.png")
        wp_list = get_waypoint_list()
        scale = update_ui(data_manager.widget_dic, data_manager.plan, data_manager.plan_w, data_manager.plan_h)
        for name, inf in wp_list.items():
            data_manager.widget_dic[name] = epw.Surface(frames=[waypoint_asset], anchor_x="center", anchor_y="center", layer=3000).bind("<RELEASE>", lambda name=name: click_waypoint(name))
            data_manager.widget_dic[name].scale(0.02, 1)
            data_manager.widget_geometry[name] = {
                "x": lambda wi, x=inf[0]: wi["plan_start_x"] + x * wi["plan_factor"],
                "y": lambda wi, y=inf[1]: wi["plan_start_y"] + y * wi["plan_factor"]
            }
            data_manager.waypoint_list.append(name)
        update_ui(data_manager.widget_dic, data_manager.plan, data_manager.plan_w, data_manager.plan_h)

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
    target_w = int((screenwidth_percent(0.3) - 60 - btn_w) * data_manager.gen_factor_w)
    
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

def wp_edit_finish_submit():
    name = data_manager.widget_dic["4_3_label_dropdown"].text
    add_poi(name, data_manager.plan_path)
    data_manager.widget_dic["4_3_screen_roomlist"].hide()

def poi_select(self):
    data_manager.widget_dic["4_3_label_dropdown"].config(text=self.text)

def show_list():
    room_list = get_room_list(data_manager.plan_path)
    add_room_list = []
    label_max_y = data_manager.ref_h * 0.543
    for i in range(len(room_list)):
        if room_list[i] not in data_manager.widget_dic:
            add_room_list.append(room_list[i])
        elif data_manager.widget_geometry[room_list[i]]["y"] > label_max_y:
            label_max_y = data_manager.widget_geometry[room_list[i]]["y"]

    for i in range(len(add_room_list)):
        data_manager.widget_dic[add_room_list[i]] = epw.Label(text=add_room_list[i], font=epw.SysFont(font="Calibri", font_size=30), screen=data_manager.room_list).bind("<RELEASE>", lambda self: poi_select(self))
        data_manager.widget_geometry[add_room_list[i]] = {"x": lambda wi: wi["plan_start_x"] + wi["plan_w"] + 60, "y": label_max_y}
        label_max_y += 50
    update_ui(data_manager.widget_dic, data_manager.plan, data_manager.plan_w, data_manager.plan_h)
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
        else: 
            data_manager.widget_dic["4_3_screen_group"].show()

def wp_newline():
    data_manager.widget_dic["4_012_label_statuscontent"].config(text="Wegpunktbearbeitung")
    data_manager.widget_dic["4_2_button_newline"].config(state="disabled")
    data_manager.widget_dic["4_2_button_newlinecan"].config(state="enabled")
    data_manager.new_line = True
    data_manager.last_wp = ""
def wp_newline_cancel():
    data_manager.widget_dic["4_012_label_statuscontent"].config(text="Wegpunktbearbeitung abgebrochen")
    data_manager.widget_dic["4_2_button_newline"].config(state="enabled")
    data_manager.widget_dic["4_2_button_newlinecan"].config(state="disabled")
    data_manager.new_line = False

def scale_value_hor(value, wi):
    if callable(value):
        return value(wi)
    return value * wi["gen_factor_w"]

def scale_value_ver(value, wi):
    if callable(value):
        return value(wi)
    return value * wi["gen_factor_h"]

def scale_font(font_size, wi):
    scaled_size = int(font_size * wi["gen_factor_w"])
    return epw.SysFont(font="Calibri", font_size=scaled_size)

def scale_widgets(widget_dic, widget_geometry, wi):
    for name, obj in widget_geometry.items():
        config = {}
        if "width" in obj:
            config["width"] = scale_value_hor(obj["width"], wi)
        if "height" in obj:
            config["height"] = scale_value_ver(obj["height"], wi)
        if "min_width" in obj:
            config["min_width"] = scale_value_hor(obj["min_width"], wi)
        if "min_height" in obj:
            config["min_height"] = scale_value_ver(obj["min_height"], wi)
        if "font_size" in obj:
            config["font"] = scale_font(obj["font_size"], wi)
        if config:
            widget_dic[name].config(**config)

        place = {}
        if "x" in obj:
            place["x"] = scale_value_hor(obj["x"], wi)
        if "y" in obj:
            place["y"] = scale_value_ver(obj["y"], wi)
        if place:
            widget_dic[name].place(**place)


def update_ui(widget_dic, plan, plan_w, plan_h):
    screen_w, screen_h = data_manager.screen.get_size()
    plan_factor = min(screen_w * 0.40 / plan_w, screen_h * 0.50 / plan_h)
    widget_dic["4_012_surface_plan"].config(frames=[plan])
    widget_dic["4_012_surface_plan"].place(x=screen_w * 0.30, y=screen_h * 0.25)
    widget_dic["4_012_surface_plan"].scale(plan_factor)
    wi = {  # window information
        "screen_w": screen_w,
        "screen_h": screen_h,
        "gen_factor_w": screen_w / data_manager.ref_w,
        "gen_factor_h": screen_h / data_manager.ref_h,
        "plan_start_x": widget_dic["4_012_surface_plan"].x,
        "plan_start_y": widget_dic["4_012_surface_plan"].y,
        "plan_w": int(plan_w * plan_factor),
        "plan_h": int(plan_h * plan_factor),
        "plan_factor": plan_factor
    }
    data_manager.plan_start_x = wi["plan_start_x"]
    data_manager.plan_start_y = wi["plan_start_y"]
    data_manager.scale = wi["plan_factor"]
    scale_widgets(data_manager.widget_dic, data_manager.widget_geometry, wi)
    return wi["plan_factor"]

def draw_lines():
    if data_manager.shape == 3:
        for con in range(len(data_manager.connections_list)):
            start = data_manager.connections_list[con]["start"]
            end = data_manager.connections_list[con]["end"]
            start_pos = (data_manager.widget_dic[start].x + data_manager.widget_dic[start].width // 2, data_manager.widget_dic[start].y + data_manager.widget_dic[start].height // 2)
            end_pos = (data_manager.widget_dic[end].x + data_manager.widget_dic[end].width // 2, data_manager.widget_dic[end].y + data_manager.widget_dic[end].height // 2)
            pygame.draw.aaline(surface=data_manager.screen, color=(207, 91, 25), start_pos=start_pos, end_pos=end_pos, width=2)
        if data_manager.new_line and len(data_manager.waypoint_list) >= 1 and data_manager.last_wp != "":
            mx, my = pygame.mouse.get_pos()
            if data_manager.plan_start_x <= mx <= data_manager.plan_start_x + data_manager.plan_w and data_manager.plan_start_y <= my <= data_manager.plan_start_y + data_manager.plan_h:
                pygame.draw.aaline(surface=data_manager.screen, color=(207, 91, 25), 
                                   start_pos=(data_manager.widget_dic[data_manager.last_wp].x + data_manager.widget_dic[data_manager.last_wp].width // 2, 
                                              data_manager.widget_dic[data_manager.last_wp].y + data_manager.widget_dic[data_manager.last_wp].height // 2), 
                                   end_pos=(mx, my), width=2)
epw.create_pygame_layer(draw_lines, 2000)

data_manager.widget_geometry = {
    "4_012_label_maintitle": {
        "x": lambda wi: wi["plan_start_x"] + wi["plan_w"] // 2 - data_manager.widget_dic["4_012_label_maintitle"].width // 2,
        "y": lambda wi: wi["plan_start_y"] // 2 - data_manager.widget_dic["4_012_label_maintitle"].height // 2,
        "font_size": 65,
    },
    "4_012_label_statustitle": {
        "x": 0.3 * data_manager.ref_w,
        "y": 0.8 * data_manager.ref_h,
        "font_size": 40,
    },
    "4_012_label_statuscontent": {
        "x": 0.3 * data_manager.ref_w,
        "y": lambda wi: wi["screen_h"] * 0.8 + data_manager.widget_dic["4_012_label_statustitle"].height,
        "font_size": 30,
        "min_width": lambda wi: 2 * (wi["screen_w"] * 0.4) // 3,
    },
    "4_0_label_roomtype": {
        "x": lambda wi: wi["screen_w"] * 0.15 - data_manager.widget_dic["4_0_label_roomtype"].width // 2,
        "y": lambda wi: wi["screen_h"] * 0.25,
        "font_size": 40,
    },
    "4_0_label_squaretype": {
        "x": 60,
        "y": lambda wi: wi["screen_h"] * 0.4 - data_manager.widget_dic["4_0_label_squaretype"].height,
        "font_size": 30,
    },
    "4_0_button_squaretype": {
        "x": 60,
        "y": lambda wi: wi["screen_h"] * 0.4,
        "font_size": 30,
    },
    "4_0_label_polytype": {
        "x": 60,
        "y": lambda wi: wi["screen_h"] * 0.5 - data_manager.widget_dic["4_0_label_polytype"].height,
        "font_size": 30,
    },
    "4_0_button_polytype": {
        "x": 60,
        "y": lambda wi: wi["screen_h"] * 0.5,
        "font_size": 30,
    },
    "4_0_label_waytype": {
        "x": 60,
        "y": lambda wi: wi["screen_h"] * 0.6 - data_manager.widget_dic["4_0_label_waytype"].height,
        "font_size": 30,
    },
    "4_0_button_waytype": {
        "x": 60,
        "y": lambda wi: wi["screen_h"] * 0.6,
        "font_size": 30,
    },
    "4_0_button_createsub": {
        "x": lambda wi: 60 + data_manager.widget_dic["4_0_button_squaretype"].width
             + (wi["screen_w"] * 0.3 - (60 + data_manager.widget_dic["4_0_button_squaretype"].width)) // 2
             - data_manager.widget_dic["4_0_button_createsub"].width // 2,
        "y": lambda wi: wi["screen_h"] * 0.4,
        "font_size": 30,
    },
    "4_0_button_createcan": {
        "x": lambda wi: data_manager.widget_dic["4_0_button_createsub"].x,
        "y": lambda wi: wi["screen_h"] * 0.5 - data_manager.widget_dic["4_0_button_createcan"].height,
        "font_size": 30,
    },
    "4_1_button_infosub": {
        "font_size": 30,
    },
    "4_1_label_infotitle": {
        "x": lambda wi: wi["screen_w"] * 0.15 - data_manager.widget_dic["4_1_label_infotitle"].width // 2,
        "y": lambda wi: wi["screen_h"] * 0.25,
        "font_size": 40,
    },
    "4_1_label_id": {
        "x": 60,
        "y": lambda wi: wi["screen_h"] * 0.4 - data_manager.widget_dic["4_1_label_id"].height,
        "font_size": 30,
    },
    "4_1_label_entrybackgr1": {
        "x": 60,
        "y": lambda wi: wi["screen_h"] * 0.4,
        "font_size": 30,
        "min_width": lambda wi: (wi["screen_w"] * 0.3) - 120,
    },
    "4_1_entry_id": {
        "x": 60,
        "y": lambda wi: wi["screen_h"] * 0.4,
        "font_size": 30,
        "height": 57,
        "width": lambda wi: (wi["screen_w"] * 0.3) - 120,
    },
    "4_1_label_name": {
        "x": 60,
        "y": lambda wi: wi["screen_h"] * 0.5 - data_manager.widget_dic["4_1_label_name"].height,
        "font_size": 30,
    },
    "4_1_label_entrybackgr2": {
        "x": 60,
        "y": lambda wi: wi["screen_h"] * 0.5,
        "font_size": 30,
        "min_width": lambda wi: (wi["screen_w"] * 0.3) - 120,
    },
    "4_1_entry_name": {
        "x": 60,
        "y": lambda wi: wi["screen_h"] * 0.5,
        "font_size": 30,
        "height": 57,
        "width": lambda wi: (wi["screen_w"] * 0.3) - 120,
    },
    "4_1_label_prof": {
        "x": 60,
        "y": lambda wi: wi["screen_h"] * 0.6 - data_manager.widget_dic["4_1_label_prof"].height,
        "font_size": 30,
    },
    "4_1_label_entrybackgr3": {
        "x": 60,
        "y": lambda wi: wi["screen_h"] * 0.6,
        "font_size": 30,
        "min_width": lambda wi: (wi["screen_w"] * 0.3) - 120,
    },
    "4_1_entry_prof": {
        "x": 60,
        "y": lambda wi: wi["screen_h"] * 0.6,
        "font_size": 30,
        "height": 57,
        "width": lambda wi: (wi["screen_w"] * 0.3) - 120,
    },
    "4_1_label_extrainfo": {
        "x": 60,
        "y": lambda wi: wi["screen_h"] * 0.7 - data_manager.widget_dic["4_1_label_extrainfo"].height,
        "font_size": 30,
    },
    "4_1_label_entrybackgr4": {
        "x": 60,
        "y": lambda wi: wi["screen_h"] * 0.7,
        "font_size": 30,
        "min_width": lambda wi: (wi["screen_w"] * 0.3) - 120,
    },
    "4_1_entry_extrainfo": {
        "x": 60,
        "y": lambda wi: wi["screen_h"] * 0.7,
        "font_size": 30,
        "height": 57,
        "width": lambda wi: (wi["screen_w"] * 0.3) - 120,
    },
    "4_1_button_finishsub": {
        "x": 60,
        "y": lambda wi: wi["screen_h"] * 0.8 - data_manager.widget_dic["4_1_button_finishsub"].height,
        "font_size": 30,
    },
    "4_1_button_finishcan": {
        "x": 240,
        "y": lambda wi: wi["screen_h"] * 0.8 - data_manager.widget_dic["4_1_button_finishcan"].height,
        "font_size": 30,
    },
    "4_1_label_starinfo": {
        "x": 60,
        "y": lambda wi: wi["screen_h"] * 0.875 - data_manager.widget_dic["4_1_label_starinfo"].height,
        "font_size": 20,
    },
    "4_2_label_createtitle": {
        "x": lambda wi: wi["screen_w"] * 0.15 - data_manager.widget_dic["4_2_label_createtitle"].width // 2,
        "y": lambda wi: wi["screen_h"] * 0.25,
        "font_size": 40, 
    },
    "4_2_button_newline": {
        "x": 60,
        "y": lambda wi: wi["screen_h"] * 0.4,
        "font_size": 30,
    },
    "4_2_button_newlinecan": {
        "x": 400,
        "y": lambda wi: wi["screen_h"] * 0.4,
        "font_size": 30,
    },
    "4_3_label_title": {
        "x": lambda wi: wi["screen_w"] * 0.85 - data_manager.widget_dic["4_3_label_title"].width // 2,
        "y": lambda wi: wi["screen_h"] * 0.25,
        "font_size": 40,
    },
    "4_3_label_poi": {
        "x": lambda wi: wi["plan_start_x"] + wi["plan_w"] + 60,
        "y": lambda wi: wi["screen_h"] * 0.4,
        "font_size": 30
    },
    "4_3_label_dropdown": {
        "x": lambda wi: wi["plan_start_x"] + wi["plan_w"] + 60,
        "y": lambda wi: wi["screen_h"] * 0.5,
        "font_size": 30,
        "min_width": lambda wi: 500
    },
    "4_3_button_accept": {
        "x": lambda wi: wi["plan_start_x"] + wi["plan_w"] + 600,
        "y": lambda wi: wi["screen_h"] * 0.5,
        "font_size": 30
    }
}
def create_widgets(plan):
    data_manager.room_creation_screen = epw.Screen(visible=True)
    data_manager.room_info_screen = epw.Screen(visible=False)
    data_manager.waypoint_creation_screen = epw.Screen(visible=False)
    data_manager.waypoint_edit_screen = epw.Screen(visible=False)
    data_manager.room_list = epw.Screen(visible=True)

    widget_dic = {
        "4_0_screen_group": data_manager.room_creation_screen,
        "4_1_screen_group": data_manager.room_info_screen,
        "4_2_screen_group": data_manager.waypoint_creation_screen,
        "4_3_screen_group": data_manager.waypoint_edit_screen,
        "4_012_surface_plan": epw.Surface(frames=[plan]),
        "4_012_label_maintitle": epw.Label(text="Raumeditor", font=epw.SysFont(font="Calibri", font_size=65)),
        "4_012_label_statustitle": epw.Label(text="Status", font=epw.SysFont(font="Calibri", font_size=40, bold=True), alignment_spacing=0, alignment="left"),
        "4_012_label_statuscontent": epw.Label(text="", font=epw.SysFont(font="Calibri", font_size=30), alignment="left", active_unpressed_background_color=(50, 50, 50), active_hover_background_color=(50, 50, 50), active_pressed_background_color=(50, 50, 50), top_left_corner_radius=15, top_right_corner_radius=15, bottom_left_corner_radius=15, bottom_right_corner_radius=15),
        "4_0_label_roomtype": epw.Label(text="Raumtyp - / Wegpunktauswahl", font=epw.SysFont(font="Calibri", font_size=40, bold=True), screen=data_manager.room_creation_screen),
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
        "4_1_entry_id": epw.Entry(font=epw.SysFont(font="Calibri", font_size=30), height=57, hide_background=True, hide_border=True, auto_size=False, screen=data_manager.room_info_screen).bind("<FOCUS-IN>", lambda: show_4_1_button_infosub("id")).bind("<FOCUS-OUT>", room_info_submit_button_hide, False),
        "4_1_label_name": epw.Label(text="Raum Name **", font=epw.SysFont(font="Calibri", font_size=30), alignment_spacing=0, alignment="left", screen=data_manager.room_info_screen),
        "4_1_entry_name": epw.Entry(font=epw.SysFont(font="Calibri", font_size=30), height=57, hide_background=True, hide_border=True, auto_size=False, screen=data_manager.room_info_screen).bind("<FOCUS-IN>", lambda: show_4_1_button_infosub("name")).bind("<FOCUS-OUT>", room_info_submit_button_hide, False),
        "4_1_label_prof": epw.Label(text="Raum Lehrer / Professor **", font=epw.SysFont(font="Calibri", font_size=30), alignment_spacing=0, alignment="left", screen=data_manager.room_info_screen),
        "4_1_entry_prof": epw.Entry(font=epw.SysFont(font="Calibri", font_size=30), height=57, hide_background=True, hide_border=True, auto_size=False, screen=data_manager.room_info_screen).bind("<FOCUS-IN>", lambda: show_4_1_button_infosub("prof")).bind("<FOCUS-OUT>", room_info_submit_button_hide, False),
        "4_1_label_extrainfo": epw.Label(text="Raum Zusatzinformationen **", font=epw.SysFont(font="Calibri", font_size=30), alignment_spacing=0, alignment="left", screen=data_manager.room_info_screen),
        "4_1_entry_extrainfo": epw.Entry(font=epw.SysFont(font="Calibri", font_size=30), height=57, hide_background=True, hide_border=True, auto_size=False, screen=data_manager.room_info_screen).bind("<FOCUS-IN>", lambda: show_4_1_button_infosub("extra")).bind("<FOCUS-OUT>", room_info_submit_button_hide, False),
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
        "4_2_button_newlinecan": epw.Button(text="Abbrechen", font=epw.SysFont(font="Calibri", font_size=30), command=wp_newline_cancel, screen=data_manager.waypoint_creation_screen),
        "4_3_label_title": epw.Label(text="Wegpunktbearbeitung", font=epw.SysFont(font="Calibri", font_size=40, bold=True), screen=data_manager.waypoint_edit_screen),
        "4_3_label_poi": epw.Label(text="Zielort", font=epw.SysFont(font="Calibri", font_size=30), alignment_spacing=0, alignment="left", screen=data_manager.waypoint_edit_screen),
        "4_3_label_dropdown": epw.Label(text="", font=epw.SysFont(font="Calibri", font_size=30), alignment="left", active_unpressed_background_color=(50, 50, 50), active_hover_background_color=(50, 50, 50), active_pressed_background_color=(50, 50, 50), top_left_corner_radius=15, top_right_corner_radius=15, bottom_left_corner_radius=15, bottom_right_corner_radius=15, screen=data_manager.waypoint_edit_screen).bind("<RELEASE>", show_list),
        "4_3_button_accept": epw.Button(text="Bestätigen", font=epw.SysFont(font="Calibri", font_size=30), command=wp_edit_finish_submit, screen=data_manager.waypoint_edit_screen),
        "4_3_screen_roomlist": data_manager.room_list
    }
    return widget_dic

def get_widget_dic(plan=None):
    if not data_manager.widget_dic and plan is not None:
        data_manager.widget_dic.update(create_widgets(plan))
    return data_manager.widget_dic
# main.py
# Theo Glase
# 22.07.2026

import pygame
import easypygamewidgets as epw
import data_manager
from gui import window_create, plan_create, get_widget_dic, update_ui
from json_manager import floor_name

pygame.init()

data_manager.screen = window_create()
plan, plan_w, plan_h, plan_path = plan_create()
data_manager.plan_path = plan_path

widget_dic = get_widget_dic(plan)
scale = update_ui(widget_dic, plan, plan_w, plan_h)

running = True
while running:
    # färben des Hintergrunds
    data_manager.screen.fill((30, 30, 30))

    if data_manager.s_coords_count == 2 or data_manager.p_coords_count >= 3:
        widget_dic["4_0_button_createsub"].config(state = "enabled")
    else:
        widget_dic["4_0_button_createsub"].config(state = "disabled")

    if data_manager.shape == 0:
        widget_dic["4_0_button_createcan"].config(state = "disabled")
    else:
        widget_dic["4_0_button_createcan"].config(state = "enabled")
    
    if data_manager.id_answer_list == []:
        widget_dic["4_1_button_finishsub"].config(state = "disabled")
    else:
        widget_dic["4_1_button_finishsub"].config(state = "enabled")

    for event in pygame.event.get():
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            scale = update_ui(widget_dic, plan, plan_w, plan_h)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            current_scale = scale if scale > 0 else 1.0
            
            if data_manager.shape == 1:
                pos = pygame.mouse.get_pos()
                s_x, s_y = int((pos[0] - data_manager.plan_start_x) / current_scale), int((pos[1] - data_manager.plan_start_y) / current_scale)
                if data_manager.s_coords_count < 2:
                    if 0 <= s_x <= plan_w and 0 <= s_y <= plan_h:
                        data_manager.s_coords.append(s_x)
                        data_manager.s_coords.append(s_y)
                        data_manager.s_coords_count += 1
                        widget_dic["4_012_label_statuscontent"].config(text=f"Die Koordinate {s_x}, {s_y} wurde hinzugefügt.")
                elif 0 <= s_x <= plan_w and 0 <= s_y <= plan_h:
                    widget_dic["4_012_label_statuscontent"].config(text=f"Es wurden bereits zwei Koordinaten hinzugefügt. [{data_manager.s_coords[0]}, {data_manager.s_coords[1]}]; [{data_manager.s_coords[2]}, {data_manager.s_coords[3]}]")

            elif data_manager.shape == 2:
                pos = pygame.mouse.get_pos()
                p_x, p_y = int((pos[0] - data_manager.plan_start_x) / current_scale), int((pos[1] - data_manager.plan_start_y) / current_scale)
                if 0 <= p_x <= plan_w and 0 <= p_y <= plan_h:
                    data_manager.p_coords.append(p_x)
                    data_manager.p_coords.append(p_y)
                    widget_dic["4_012_label_statuscontent"].config(text=f"Die Koordinate {p_x}, {p_y} wurde hinzugefügt.")
                    data_manager.p_coords_count += 1

            elif data_manager.new_line:
                if not data_manager.show_line: data_manager.show_line = True
                pos = pygame.mouse.get_pos()
                w_x, w_y = int((pos[0] - data_manager.plan_start_x) / current_scale), int((pos[1] - data_manager.plan_start_y) / current_scale)
                if 0 <= w_x <= plan_w and 0 <= w_y <= plan_h:
                    data_manager.w_coords.append(w_x)
                    data_manager.w_coords.append(w_y)
                    data_manager.w_coords_count += 1
                    data_manager.waypoint_id += 1
                    widget_dic["4_012_label_statuscontent"].config(text=f"Der Wegpunkt bei {w_x}, {w_y} wurde hinzugefügt.")

                    w_name = f"{floor_name(data_manager.plan_path)}_{w_x},{w_y}"
                    info = {
                        "x": pos[0],
                        "y": pos[1],
                        "stair": False
                    }
                    waypoint_list_data = {
                        "name": w_name,
                        "line_ID": data_manager.line_id,
                        "waypoint_ID": data_manager.waypoint_id
                    }
                    data_manager.waypoint_list.append(waypoint_list_data)
                    print(data_manager.waypoint_list)
                    data_manager.widget_geometry[w_name] = info
                    waypoint_asset = pygame.image.load("assets/waypoint.png")
                    data_manager.widget_dic[w_name] = epw.Surface(waypoint_asset, anchor_x="center", anchor_y="center", layer=3000)
                    data_manager.widget_dic[w_name].scale(0.02, 1)
                    data_manager.widget_dic[w_name].place(x = pos[0], y = pos[1])
        
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
            if data_manager.shape == 1 and data_manager.s_coords_count > 0:
                widget_dic["4_012_label_statuscontent"].config(text=f"Die Koordinate {data_manager.s_coords[-2]}, {data_manager.s_coords[-1]} wurde entfernt.")
                data_manager.s_coords.pop()
                data_manager.s_coords.pop()
                data_manager.s_coords_count -= 1
                print(data_manager.s_coords_count)
            
            if data_manager.shape == 2 and data_manager.p_coords_count > 0:
                widget_dic["4_012_label_statuscontent"].config(text=f"Die Koordinate {data_manager.p_coords[-2]}, {data_manager.p_coords[-1]} wurde entfernt.")
                data_manager.p_coords.pop()
                data_manager.p_coords.pop()
                data_manager.p_coords_count -= 1
            
            if data_manager.shape == 3 and data_manager.w_coords_count > 0:
                widget_dic["4_012_label_statuscontent"].config(text=f"Der Wegpunkt bei {data_manager.w_coords[-2]}, {data_manager.w_coords[-1]} wurde entfernt.")
                data_manager.w_coords.pop()
                data_manager.w_coords.pop()
                data_manager.w_coords_count -= 1
                print(data_manager.w_coords_count)
            
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and data_manager.shape in (1, 2, 3) and data_manager.widget_dic["4_0_screen_group"].visible:
            data_manager.s_coords.clear()
            data_manager.p_coords.clear()
            data_manager.w_coords.clear()
            data_manager.s_coords_count = 0
            data_manager.p_coords_count = 0
            data_manager.w_coords_count = 0
            widget_dic["4_012_label_statuscontent"].config(text="Zurücksetzen der Variablen")

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            data_manager.new_line = False
            data_manager.show_line = False

        elif event.type == pygame.QUIT:
            running = False
    
        epw.handle_event(event)
    epw.handle_special_events()
    epw.flip()

pygame.quit()
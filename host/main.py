# main.py
# Theo Glase
# 22.07.2026

import pygame
import easypygamewidgets as epw
import data_manager
from gui import window_create, plan_create, get_widget_dic, update_ui, update_gen_factor, click_waypoint, del_waypoint
from json_manager import floor_name, add_waypoint_json, add_connection_json

pygame.init()

data_manager.screen = window_create()
data_manager.plan, data_manager.plan_w, data_manager.plan_h, data_manager.plan_path = plan_create()

widget_dic = get_widget_dic(data_manager.plan)
scale = update_ui(widget_dic, data_manager.plan, data_manager.plan_w, data_manager.plan_h)

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
            scale = update_ui(widget_dic, data_manager.plan, data_manager.plan_w, data_manager.plan_h)

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            current_scale = scale if scale > 0 else 1.0
            data_manager.l_clicked = False
            data_manager.r_clicked = False

            for name in data_manager.waypoint_list:
                widget = data_manager.widget_dic[name]
                hovered = widget.rect.collidepoint(pygame.mouse.get_pos())
                if hovered:
                    data_manager.l_clicked = True
                    break
            
            if data_manager.shape == 1:
                pos = pygame.mouse.get_pos()
                s_x, s_y = int((pos[0] - data_manager.plan_start_x) / current_scale), int((pos[1] - data_manager.plan_start_y) / current_scale)
                if data_manager.s_coords_count < 2:
                    if 0 <= s_x <= data_manager.plan_w and 0 <= s_y <= data_manager.plan_h:
                        data_manager.s_coords.append(s_x)
                        data_manager.s_coords.append(s_y)
                        data_manager.s_coords_count += 1
                        widget_dic["4_012_label_statuscontent"].config(text=f"Die Koordinate {s_x}, {s_y} wurde hinzugefügt.")
                elif 0 <= s_x <= data_manager.plan_w and 0 <= s_y <= data_manager.plan_h:
                    widget_dic["4_012_label_statuscontent"].config(text=f"Es wurden bereits zwei Koordinaten hinzugefügt. [{data_manager.s_coords[0]}, {data_manager.s_coords[1]}]; [{data_manager.s_coords[2]}, {data_manager.s_coords[3]}]")

            elif data_manager.shape == 2:
                pos = pygame.mouse.get_pos()
                p_x, p_y = int((pos[0] - data_manager.plan_start_x) / current_scale), int((pos[1] - data_manager.plan_start_y) / current_scale)
                if 0 <= p_x <= data_manager.plan_w and 0 <= p_y <= data_manager.plan_h:
                    data_manager.p_coords.append(p_x)
                    data_manager.p_coords.append(p_y)
                    widget_dic["4_012_label_statuscontent"].config(text=f"Die Koordinate {p_x}, {p_y} wurde hinzugefügt.")
                    data_manager.p_coords_count += 1

            elif data_manager.new_line and not data_manager.l_clicked:
                if not data_manager.show_line: data_manager.show_line = True
                pos = pygame.mouse.get_pos()
                w_x, w_y = int((pos[0] - data_manager.plan_start_x) / current_scale), int((pos[1] - data_manager.plan_start_y) / current_scale)
                if 0 <= w_x <= data_manager.plan_w and 0 <= w_y <= data_manager.plan_h:
                    data_manager.w_coords.append(w_x)
                    data_manager.w_coords.append(w_y)
                    data_manager.w_coords_count += 1
                    widget_dic["4_012_label_statuscontent"].config(text=f"Der Wegpunkt bei {w_x}, {w_y} wurde hinzugefügt.")

                    w_name = f"{floor_name(data_manager.plan_path)}_{w_x},{w_y}"
                    update_gen_factor()
                    info = {
                        "x": lambda wi, x=w_x: wi["plan_start_x"] + x * wi["plan_factor"],
                        "y": lambda wi, y=w_y: wi["plan_start_y"] + y * wi["plan_factor"],
                    }
                    json_data = {
                        "x": w_x,
                        "y": w_y
                    }
                    add_waypoint_json(json_data, w_name)
                    data_manager.waypoint_list.append(w_name)
                    data_manager.widget_geometry[w_name] = info
                    if data_manager.last_wp != "":
                        connections_list_data = {
                            "start": data_manager.last_wp,
                            "end": w_name
                        }
                        add_connection_json(connections_list_data)
                        data_manager.connections_list.append(connections_list_data)
                        data_manager.last_wp = w_name
                    data_manager.last_wp = w_name

                    waypoint_asset = pygame.image.load("assets/waypoint.png")
                    data_manager.widget_dic[w_name] = epw.Surface(frames=[waypoint_asset], anchor_x="center", anchor_y="center", layer=3000).bind("<RELEASE>", lambda name=w_name: click_waypoint(name))
                    data_manager.widget_dic[w_name].scale(0.02, 1)
                    data_manager.widget_dic[w_name].place(x = pos[0], y = pos[1])

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            data_manager.r_clicked = False

            for name in data_manager.waypoint_list:
                widget = data_manager.widget_dic[name]
                hovered = widget.rect.collidepoint(pygame.mouse.get_pos())
                if hovered:
                    data_manager.r_clicked = True
                    wp = name
                    break

            if data_manager.r_clicked:
                del_waypoint(wp, 1)

            
        
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE and data_manager.last_wp != "":
            if data_manager.shape == 1 and data_manager.s_coords_count > 0 and data_manager.widget_dic["4_0_screen_group"].visible:
                widget_dic["4_012_label_statuscontent"].config(text=f"Die Koordinate {data_manager.s_coords[-2]}, {data_manager.s_coords[-1]} wurde entfernt.")
                data_manager.s_coords.pop()
                data_manager.s_coords.pop()
                data_manager.s_coords_count -= 1
            
            if data_manager.shape == 2 and data_manager.p_coords_count > 0:
                widget_dic["4_012_label_statuscontent"].config(text=f"Die Koordinate {data_manager.p_coords[-2]}, {data_manager.p_coords[-1]} wurde entfernt.")
                data_manager.p_coords.pop()
                data_manager.p_coords.pop()
                data_manager.p_coords_count -= 1
            
            if data_manager.shape == 3 and data_manager.w_coords_count > 0:
                    try:
                        if data_manager.last_wp == "":
                            data_manager.last_wp = data_manager.waypoint_list[-1]
                        widget_dic["4_012_label_statuscontent"].config(text=f"Der Wegpunkt bei {data_manager.w_coords[-2]}, {data_manager.w_coords[-1]} wurde entfernt.")
                        del_waypoint(data_manager.last_wp, 0)
                    except:
                        pass
                       

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and data_manager.shape in (1, 2, 3) and data_manager.widget_dic["4_0_screen_group"].visible:
            data_manager.s_coords.clear()
            data_manager.p_coords.clear()
            data_manager.w_coords.clear()
            data_manager.s_coords_count = 0
            data_manager.p_coords_count = 0
            data_manager.w_coords_count = 0
            widget_dic["4_012_label_statuscontent"].config(text="Zurücksetzen der Variablen")

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            data_manager.last_wp = ""
            data_manager.show_line = False

        elif event.type == pygame.QUIT:
            running = False
    
        epw.handle_event(event)
    epw.handle_special_events()
    epw.flip()

pygame.quit()
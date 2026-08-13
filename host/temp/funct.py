import json
from pathlib import Path



def json_path(plan_path):
    path_objekt = Path(plan_path)
    json_folder = path_objekt.parent.parent
    json_folder_name = json_folder.name
    json_folder = json_folder.as_posix()
    json_name = f"{json_folder_name}.json"
    json_path = f"{json_folder}/{json_name}"
    return json_path


def add_room_json(data, plan_path):
    with open(fr"{str(json_path(plan_path))}", "r", encoding="utf-8") as file:
        current_data = json.load(file)
    current_data["rooms"].append(data)
    with open(fr"{str(json_path(plan_path))}", "w", encoding="utf-8") as file:
        json.dump(current_data, file, indent=4, ensure_ascii=False)
    

def save_data(plan_path,shape, nr, name, prof, exrainf):
    if shape == 1 or shape == 2:
        data = {
            "nr": str(nr[0]),
            "name": name,
            "prof": prof,
            "exrainf": exrainf
          }
    elif shape == 3:
        data = {}
    add_room_json(data, plan_path)


    else:
                    if not data_manager.new_line: return
                    plan = get_widget_dic()["4_012_surface_plan"]
                    update_gen_factor()
                    mx, my = pygame.mouse.get_pos()[0] * data_manager.gen_factor_w, pygame.mouse.get_pos()[1] * data_manager.gen_factor_h
                    if plan.x <= mx <= plan.x + plan.width and plan.y <= my <= plan.y + plan.height and data_manager.show_line:
                        pygame.draw.aaline(
                            surface=data_manager.screen, color=(207, 91, 25),
                            start_pos=(data_manager.widget_dic[data_manager.waypoint_list[wp]["name"]].x + data_manager.widget_dic[data_manager.waypoint_list[wp]["name"]].width / 2,
                                       data_manager.widget_dic[data_manager.waypoint_list[wp]["name"]].y + data_manager.widget_dic[data_manager.waypoint_list[wp]["name"]].height / 2),
                            end_pos=(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]), width=2)
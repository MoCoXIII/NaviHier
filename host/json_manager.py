import json
import data_manager
from pathlib import Path

def floor_name(plan_path):
    path_objekt = Path(plan_path)
    folder = path_objekt.parent.parent
    return folder.name    

def json_path(plan_path):
    path_objekt = Path(plan_path)
    json_folder = path_objekt.parent.parent
    json_folder_name = json_folder.name
    json_folder = json_folder.as_posix()
    json_name = f"{json_folder_name}.json"
    json_path = f"{json_folder}/{json_name}"
    return json_path

def add_room_json(data, name, plan_path):
    with open(fr"{str(json_path(plan_path))}", "r", encoding="utf-8") as file:
        current_data = json.load(file)
    current_data["poi"][name] = data
    with open(fr"{str(json_path(plan_path))}", "w", encoding="utf-8") as file:
        json.dump(current_data, file, indent=4, ensure_ascii=False)  

def save_data(plan_path, shape, nr, name, prof, extrainf):
    room_nr = str(nr[0])
    data = {
        "coords": data_manager.s_coords,
        "names": name,
        "prof": prof,
        "extrainfo": extrainf
        }
    add_room_json(data, room_nr, plan_path)

def add_waypoint_json(data, name):
    with open(fr"{str(json_path(data_manager.plan_path))}", "r", encoding="utf-8") as file:
        current_data = json.load(file)
    current_data["waypoints"][name] = data
    with open(fr"{str(json_path(data_manager.plan_path))}", "w", encoding="utf-8") as file:
        json.dump(current_data, file, indent=4, ensure_ascii=False)

def del_waypoint_json(plan_path):
    with open(fr"{str(json_path(plan_path))}", "r", encoding="utf-8") as file:
        current_data = json.load(file)
    current_data["waypoints"].popitem()
    with open(fr"{str(json_path(plan_path))}", "w", encoding="utf-8") as file:
        json.dump(current_data, file, indent=4, ensure_ascii=False)

def add_connection_json(data, plan_path):
    with open(fr"{str(json_path(plan_path))}", "r", encoding="utf-8") as file:
        current_data = json.load(file)
    current_data["connections"].append(data)
    with open(fr"{str(json_path(plan_path))}", "w", encoding="utf-8") as file:
        json.dump(current_data, file, indent=4, ensure_ascii=False)

def del_connection_json(plan_path):
    with open(fr"{str(json_path(plan_path))}", "r", encoding="utf-8") as file:
        current_data = json.load(file)
    current_data["connections"].pop()
    with open(fr"{str(json_path(plan_path))}", "w", encoding="utf-8") as file:
        json.dump(current_data, file, indent=4, ensure_ascii=False)

def get_room_list(plan_path):
    with open(fr"{str(json_path(plan_path))}", "r", encoding="utf-8") as file:
        current_data = json.load(file)
    room_list = []
    for room in current_data["poi"].keys():
        room_list.append(room)
    return room_list

def get_room_names(name):
    with open(fr"{str(json_path(data_manager.plan_path))}", "r", encoding="utf-8") as file:
        current_data = json.load(file)
    name_list = current_data["poi"][name]["names"].copy()
    return name_list

def add_poi(poi_name, plan_path):
    with open(fr"{str(json_path(plan_path))}", "r", encoding="utf-8") as file:
        current_data = json.load(file)
    current_data["waypoints"][data_manager.wp_name]["poi"] = poi_name
    current_data["poi"][poi_name] = {}
    current_data["poi"][poi_name]["names"] = get_room_names(poi_name)
    with open(fr"{str(json_path(plan_path))}", "w", encoding="utf-8") as file:
        json.dump(current_data, file, indent=4, ensure_ascii=False)

def get_waypoint_list():
    with open(fr"{str(json_path(data_manager.plan_path))}", "r", encoding="utf-8") as file:
        current_data = json.load(file)
    wp_list = {}
    max_line_ID = 0
    for name, wp in current_data["waypoints"].items():
        wp_list[name] = [wp["x"], wp["y"], wp["line_ID"]]
        if wp["line_ID"] > max_line_ID:
            max_line_ID = wp["line_ID"]
    data_manager.line_id = max_line_ID
    return wp_list

def get_connection_list():
    with open(fr"{str(json_path(data_manager.plan_path))}", "r", encoding="utf-8") as file:
        current_data = json.load(file)
    connection_list = current_data["connections"].copy()
    print(connection_list)
    return connection_list
import json
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

def add_waypoint_json(data, name, plan_path):
    with open(fr"{str(json_path(plan_path))}", "r", encoding="utf-8") as file:
        current_data = json.load(file)
    current_data["waypoints"][name] = data
    with open(fr"{str(json_path(plan_path))}", "w", encoding="utf-8") as file:
        json.dump(current_data, file, indent=4, ensure_ascii=False)

def add_connection_json(data, plan_path):
    with open(fr"{str(json_path(plan_path))}", "r", encoding="utf-8") as file:
        current_data = json.load(file)
    current_data["connections"].append(data)
    with open(fr"{str(json_path(plan_path))}", "w", encoding="utf-8") as file:
        json.dump(current_data, file, indent=4, ensure_ascii=False)
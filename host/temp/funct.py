import customtkinter
import json
from pathlib import Path

def plan_selection():
        print("Wähle den Gebäudeplan aus")
        try: 
            plan_path = customtkinter.filedialog.askopenfilename(title = "Bitte wähle die Datei des Gebäudeplans aus", filetypes=[("All", "*.png;*.jpg;*.jpeg;*.webp"), ("PNG Datei", "*.png"), ("JPG Datei", "*.jpg"), ("JPEG Datei", "*.jpeg"), ("WEBP Datei", "*.webp")], initialdir=r"Gymnasium_Wernigerode")
            if plan_path == "": 
                raise FileNotFoundError
            return plan_path
        except FileNotFoundError: 
            exit(0)

def json_path(plan_path):
    path_objekt = Path(plan_path)
    json_folder = path_objekt.parent.parent
    json_folder_name = json_folder.name
    json_folder = json_folder.as_posix()
    json_name = f"{json_folder_name}.json"
    json_path = f"{json_folder}/{json_name}"
    return json_path


def add_json(data, plan_path):
    with open(fr"{str(json_path(plan_path))}", "r", encoding="utf-8") as file:
        current_data = json.load(file)
    current_data["rooms"].append(data)
    with open(fr"{str(json_path(plan_path))}", "w", encoding="utf-8") as file:
        json.dump(current_data, file, indent=4, ensure_ascii=False)
    

def save_data(plan_path,shape, nr, name, prof, exrainf):
    if shape == 1 or shape == 2:
        data = {
            "nr": nr,
            "name": name,
            "prof": prof,
            "exrainf": exrainf
          }
    elif shape == 3:
        data = {}
    add_json(data, plan_path)
import customtkinter
import pygame
import json
import math
from pathlib import Path

# erstellen des root tkinterfenster
root = customtkinter.CTk()
root.attributes("-topmost", True)
root.withdraw()

# erstellen der Fragelisten // question_...: Enthalten je nach Buchstabenpräfix die entsprechenden Fragen zu den Räumen oder Wegpunkten
questions_s = [
        "Gib die Nr des Raumes ein",
        "Gib den Namen des Raumes ein",
        "Gib den Zweiten Namen des Raumes ein"
        ]

questions_c = [
        "Gib die Nr des Raumes ein",
        "Gib den Namen des Raumes ein",
        "Gib den Zweiten Namen des Raumes ein"
        ]

questions_w = [
        "Gib die Wegpunktnummer ein",
        "Gib den ersten Wegbunktlink ein",
        "Gib den zweiten Wegbunktlink ein",
        "Gib den dritten Wegpunktlink ein",
        "Gib den vierten Wegpunktlink ein"
        ]

question_p = [
        "Gib die Nr des Raumes ein",
        "Gib den Namen des Raumes ein",
        "Gib den Zweiten Namen des Raumes ein"
]

def plan_selection():
        print("Wähle den Gebäudeplan aus")
        try: 
            plan_path = customtkinter.filedialog.askopenfilename(title = "Bitte wähle die Datei des Gebäudeplans aus", filetypes=[("All", "*.png;*.jpg;*.jpeg;*.webp"), ("PNG Datei", "*.png"), ("JPG Datei", "*.jpg"), ("JPEG Datei", "*.jpeg"), ("WEBP Datei", "*.webp")], initialdir=r"Test_Gebäudeplan")
            if plan_path == "": 
                raise FileNotFoundError
            return plan_path
        except FileNotFoundError: 
            exit(0)

def text_display(screen, text, font_size, x, y):
        
        font = pygame.font.SysFont(None, font_size)
        img = font.render(text, True, (255, 255, 255))
        img_w, img_h = img.get_size()
        screen.blit(img, (x - img_w / 2, y - img_h / 2))

def question_display(screen, questions, index):
        font = pygame.font.SysFont(None, 30)
        img = font.render(questions[index], True, (255, 255, 255))
        screen.blit(img, ())

# Funktion zum Erstellen des Dialogfensters und der Eingabeverarbeitung // loc_answers: lokale Variable, die die Eingaben speichert; answ: lokale Variable, die die aktuelle Eingabe speichert
def dialog (questions):
        loc_answers = []
        for question in questions:
                dialog = customtkinter.CTkInputDialog(text=question, title="Attributeingabe")   
                answ = dialog.get_input()
                
                if answ is not None:
                        loc_answers.append(answ)
                else:
                        print("Eingabe abgebrochen")
                        return None
        return loc_answers

# Funktion zum erstellen des Verzeichnisses des square Raumes // answers: Liste mit den Eingaben; data: speichert das Verzeichnis
def square (s_x1, s_y1, s_x2, s_y2, plan_path, scale):
        answers = dialog(questions_s)
        if answers is None:
                return
        else:
                data = {
                "names": [
                        f"{answers[0]}",
                        f"{answers[1]}",
                        f"{answers[2]}"
                ],
                "shape": "rect",
                "coords": [
                        s_x1/scale,
                        s_y1/scale,
                        s_x2/scale,
                        s_y2/scale
                ]
                }
                add_room(data, plan_path)

                list_data = {
                        "name": f"{data['names'][0]}",
                        "path": fr"{str(json_path_floor(plan_path))}",
                        "rooms_list": f"{rooms_list_pos(plan_path)}"
                }
                add_room_list(list_data, plan_path)

# Funktion zum erstellen des Verzeichnisses des circle Raumes // answers: Liste mit den Eingaben; data: speichert das Verzeichnis
def circle (c_x, c_y, radiuspos_x, radiuspos_y, plan_path, scale):
        answers = dialog(questions_c)
        if answers is None:
                return
        else:
                data = {
                "names": [
                        f"{answers[0]}",
                        f"{answers[1]}",
                        f"{answers[2]}"
                ],
                "shape": "circle",
                "coords": [
                        c_x/scale,
                        c_y/scale,
                        math.dist((c_x/scale, c_y/scale), (radiuspos_x/scale, radiuspos_y/scale))
                ]
                }
                add_room(data, plan_path)

                list_data = {
                        "name": f"{data['names'][0]}",
                        "path": fr"{str(json_path_floor(plan_path))}",
                        "rooms_list": f"{rooms_list_pos(plan_path)}"
                }
                add_room_list(list_data, plan_path)

# Funktion zum erstellen des Verzeichnisses des Wegpunktes // answers: Liste mit den Eingaben; data: speichert das Verzeichnis
def waypoint (w_x, w_y, plan_path, scale):
        answers = dialog(questions_w)

        if answers is None:
                return
        else:
                data = {
                "id": f"{answers[0]}",
                "x": w_x/scale,
                "y": w_y/scale,
                "links": [
                        f"{answers[1]}",
                        f"{answers[2]}",
                        f"{answers[3]}",
                        f"{answers[4]}"
                ]
                }
                add_waypoint(data, plan_path)

# Funktion zum erstellen des Verzeichnisses des polygon Raumes // answers: Liste mit den Eingaben; data: speichert das Verzeichnis
def polygon (p_coords, plan_path):
        answers = dialog(question_p)
        if answers is None:
                return
        else:
                data = {
                        "names": [
                                f"P{answers[0]}",
                                f"{answers[1]}",
                                f"{answers[2]}"
                        ],
                        "shape": "poly",
                        "coords": p_coords
                }
                add_room(data, plan_path)  

                list_data = {
                        "name": f"{data['names'][0]}",
                        "path": fr"{str(json_path_floor(plan_path))}",
                        "rooms_list": fr"{str(rooms_list_pos(plan_path))}"
                }
                add_room_list(list_data, plan_path)

# Funktion zum laden, bearbeiten (hinzufügen des neuen Raumes) und speichern der Json Datei // current_data: speichert die aktuelle Json Datei
def add_room(data, plan_path):
        # Laden in die floor json
        with open(fr"{str(json_path_floor(plan_path))}", "r", encoding="utf-8") as file:
                current_data = json.load(file)

        current_data["rooms"].append(data)

        with open(fr"{str(json_path_floor(plan_path))}", "w", encoding="utf-8") as file:
                json.dump(current_data, file, indent=4, ensure_ascii=False)

def add_room_list(list_data, plan_path):
        # laden in die Raumliste json
        with open(fr"{str(json_path_list(plan_path))}", "r", encoding="utf-8") as file:
                current_data = json.load(file)

        print(current_data)
        print(list_data)
        current_data.append(list_data)

        with open(fr"{str(json_path_list(plan_path))}", "w", encoding="utf-8") as file:
                json.dump(current_data, file, indent=4, ensure_ascii=False)

def rooms_list_pos(plan_path):
        with open(fr"{str(json_path_floor(plan_path))}", "r", encoding="utf-8") as file:
                current_data = json.load(file)
        
        return len(current_data["rooms"]) - 1

# Funktion zum laden, bearbeiten (hinzufügen des neuen Wegpunktes) und speichern der Json Datei // current_data: speichert die aktuelle Json Datei
def add_waypoint(data, plan_path):
        with open(fr"{str(json_path_floor(plan_path))}", "r", encoding="utf-8") as file:
                current_data = json.load(file)
        
        current_data["waypoints"].append(data)

        with open(fr"{str(json_path_floor(plan_path))}", "w", encoding="utf-8") as file:
                json.dump(current_data, file, indent=4)

def json_path_floor(plan_path):
        path_objekt = Path(plan_path)
        json_folder = path_objekt.parent.parent
        json_folder_name = json_folder.name
        json_folder = json_folder.as_posix()
        json_name = f"{json_folder_name}.json"
        json_path = f"{json_folder}/{json_name}"
        return json_path

def json_path_list(plan_path):
        path_objekt = Path(plan_path)
        json_folder = path_objekt.parent.parent.parent.parent
        json_folder = json_folder.as_posix()
        json_path = f"{json_folder}/room_list.json"
        print(json_path)
        return json_path
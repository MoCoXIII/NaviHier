import customtkinter
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
        plan_path = customtkinter.filedialog.askopenfilename(title = "Bitte wähle die Datei des Gebäudeplans aus", filetypes=[("PNG Datei", "*.png")], initialdir=r"Test_Gebäudeplan")
        return plan_path

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

# Funktion zum laden, bearbeiten (hinzufügen des neuen Raumes) und speichern der Json Datei // current_data: speichert die aktuelle Json Datei
def add_room(data, plan_path):
        with open(fr"{str(json_path(plan_path))}", "r", encoding="utf-8") as file:
                current_data = json.load(file)

        current_data["rooms"].append(data)

        with open(fr"{str(json_path(plan_path))}", "w", encoding="utf-8") as file:
                json.dump(current_data, file, indent=4, ensure_ascii=False)

# Funktion zum laden, bearbeiten (hinzufügen des neuen Wegpunktes) und speichern der Json Datei // current_data: speichert die aktuelle Json Datei
def add_waypoint(data, plan_path):
        with open(fr"{str(json_path(plan_path))}", "r", encoding="utf-8") as file:
                current_data = json.load(file)
        
        current_data["waypoints"].append(data)

        with open(fr"{str(json_path(plan_path))}", "w", encoding="utf-8") as file:
                json.dump(current_data, file, indent=4)

def json_path(plan_path):
        path_objekt = Path(plan_path)
        json_folder = path_objekt.parent.parent
        json_name = f"{json_folder.name}.json"
        json_path = f"{json_folder}/{json_name}"
        return json_path
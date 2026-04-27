# coordsbestimmung_überarbeitet
# Theo Glase
# 13.04.2026

import pygame
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
def square (s_x1, s_y1, s_x2, s_y2, plan_path):
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
def circle (c_x, c_y, radiuspos_x, radiuspos_y, plan_path):
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
def waypoint (w_x, w_y, plan_path):
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

# initialisieren von Pygame
pygame.init()

# erstellen der Positionsvariablen für den square Raum // s_x1, s_y1: erste Koordinate (obere linke Ecke); s_x2, s_y2: zweite Koordinate (untere rechte Ecke)
s_x1 = 0
s_y1 = 0
s_x2 = 0
s_y2 = 0

# erstellen der Positionsvariablen für den circle Raum // c_x, c_y: Position des Mittelpunktes, radius_pos_x, radius_pos_y: Position des Radiuspunktes
c_x = 0
c_y = 0
radius_pos_x = 0
radius_pos_y = 0

# erstellen der Positionsvariablen des Wegpunktes // w_x, w_y: Koordinaten
w_x = 0
w_y = 0

# erstellen der Liste zum speichern der Koordinaten des polygon Raumes
p_coords = []

# erstellend der Variablen zum Abbrechen der coordseingabe
while_running_s = True
while_running_c = True
while_running_w = True
while_running_p = True

# erstellen der Variablen zum Löschen einer Koordinate
while_running_s_del = True
while_running_c_del = True
while_running_w_del = True

# erstellen der Variable zum Anzeigen der Info
info_shown = False

# erstellen der Variable zum Anzeigen der Pfadeingabe
path_shown = False

running = True
while running:

        # Abfrage des Bildpfades
        if not path_shown:
                plan_path = plan_selection()
                print(plan_path)

                plan = pygame.image.load(fr"{plan_path}")
                plan_w, plan_h = plan.get_size()

                screen_info = pygame.display.Info()
                screen_w, screen_h = screen_info.current_w * 0.8, screen_info.current_h * 0.8

                faktor = min(screen_w/plan_w, screen_h/plan_h, 1.0)

                new_w, new_h = int(plan_w*faktor), int(plan_h*faktor)

                screen = pygame.display.set_mode((new_w, new_h))
                plan = pygame.transform.scale(plan, (new_w, new_h))

                # erstellen der scale
                scale = 1000/int(plan_w*faktor)

                path_shown = True

        # Anzeigen der Info beim starten des Programms
        if not info_shown:
                print("\n         ---Eingabeprogramm für Räume und Wegpunkte---\n\n" \
                "Hinzufügen der Räume durch Drücken folgender Tasten:\n" \
                "Quadratischer Raum: s\n" \
                "Kreisförmiger Raum: c\n" \
                "Raum mit benutzerdefinierter Form (Poygon): p\n\n" \
                "Hinzufügen der Wegpunkte: w\n\n" \
                "Die Koordinateneingabe kann mit ESCAPE abgebrochen werden, oder mit dem Close Knopf bei der Eigenschafteneingabe\n" \
                "Die letzte angegebene Koordinate kann mit BACKSPACE gelöscht werden (relevant bei s, c und p)\n" \
                "Die Eingabe der Koordinaten des Polygons kann mit ENTER abgeschlossen werden\n\n")

                info_shown = True

        # plazieren des Bildes
        screen.blit(plan, (0, 0))

        for event in pygame.event.get():
                
                # prüfen, ob das Fenster geschlossen wird
                if event.type == pygame.QUIT:
                        running = False
                
                # Prüfen, ob der suare Raum ausgewählt wurde
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                        
                        print("Gebe die Koordinate der oberen, linken Ecke ein\n")
                        while while_running_s:
                                screen.blit(plan, (0, 0))
                                pygame.display.flip()
                                for event in pygame.event.get():
                                        # zurücksetzen der Variablen zum Abbrechen der coordeingabe
                                        while_running_s_del = True

                                        # speichern der ersten Koordinate
                                        if event.type == pygame.MOUSEBUTTONDOWN:
                                                s_x1, s_y1 = pygame.mouse.get_pos()
                                                
                                                print("Die Koordinaten wurden gespeichert")
                                                print(f"[{s_x1}, {s_y1}]\n")
                                                print("Gebe die Koordinate der unteren, rechten Ecke ein\n")
                                                while while_running_s and while_running_s_del:
                                                        for event in pygame.event.get():

                                                                # speichern der zweiten Koordinate
                                                                if event.type == pygame.MOUSEBUTTONDOWN:
                                                                        s_x2, s_y2 = pygame.mouse.get_pos()
                                                                        print(f"Abschluss der Koordinateneingabe\nKoordinaten: [{s_x1}, {s_y1}, {s_x2}, {s_y2}]\n")
                                                                        square(s_x1, s_y1, s_x2, s_y2, plan_path)
                                                                        while_running_s = False
                                                                
                                                                # löschen der letzen Koordinate
                                                                elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                                                                        print(f"Du hast die letzte Koordinate: {s_x1}, {s_y1} gelöscht!\n")
                                                                        s_x1 = 0
                                                                        s_y1 = 0
                                                                        while_running_s_del = False

                                                                # stoppen des Programms
                                                                elif event.type == pygame.QUIT:
                                                                        while_running_s = False
                                                                        running = False
                                                                        break

                                                                # abbrechen der Koordinateneingabe
                                                                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                                                                        while_running_s = False
                                                                        print("Koordinateneingabe abgebrochen!\n")
                                                                        break

                                        # stoppen des Programms
                                        elif event.type == pygame.QUIT:
                                                while_running_s = False
                                                running = False
                                                break

                                        # abbrechen der Koordinateneingabe
                                        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                                                while_running_s = False
                                                print("Koordinateneingabe abgebrochen!\n")
                                                break
                
                # Prüfen, ob der Kreis Raum ausgewählt wurde
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                        
                        print("Gebe die Koordinaten des Mittelpunkt des Kreises ein\n")
                        while while_running_c:
                                screen.blit(plan, (0, 0))
                                pygame.display.flip()
                                for event in pygame.event.get():
                                        # zurücksetzen der Variablen zum Abbrechen der coordeingabe
                                        while_running_c_del = True

                                        # speichern der ersten Koordinate
                                        if event.type == pygame.MOUSEBUTTONDOWN:
                                                c_x, c_y = pygame.mouse.get_pos()

                                                print("Die Koordinaten wurden gespeichert")
                                                print(f"[{c_x}, {c_y}]\n")
                                                print("Gebe Koordinaten an, um den Radius zu bestimmen")
                                                while while_running_c and while_running_c_del:
                                                        for event in pygame.event.get():

                                                                # speichern der zweiten Koordinate
                                                                if event.type == pygame.MOUSEBUTTONDOWN:
                                                                        radius_pos_x, radius_pos_y = pygame.mouse.get_pos()
                                                                        print(f"Abschluss der Koordinateneingabe\nKoordinaten: [{c_x}, {c_y}; Radiuskoordinaten: {radius_pos_x}, {radius_pos_y}; Radius: {math.dist((c_x/scale, c_y/scale), (radius_pos_x/scale, radius_pos_y/scale))}]\n")
                                                                        circle(c_x, c_y, radius_pos_x, radius_pos_y, plan_path)
                                                                        while_running_c = False

                                                                # löschen der letzen Koordinate
                                                                elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                                                                        print(f"Du hast die letzte Koordinate: {c_x}, {c_y} gelöscht!\n")
                                                                        c_x = 0
                                                                        c_y = 0
                                                                        while_running_c_del = False

                                                                # stoppen des Programms
                                                                elif event.type == pygame.QUIT:
                                                                        while_running_c = False
                                                                        running = False
                                                                        break

                                                                # abbrechen der Koordinateneingabe
                                                                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                                                                        while_running_c = False
                                                                        print("Koordinateneingabe abgebrochen!\n")
                                                                        break

                                        # stoppen des Programms
                                        elif event.type == pygame.QUIT:
                                                while_running_c = False
                                                running = False
                                                break

                                        # abbrechen der Koordinateneingabe
                                        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                                                while_running_c = False
                                                print("Koordinateneingabe abgebrochen!\n")
                                                break
                
                # Prüfen, ob der Wegpunkt ausgewählt wurde
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                        
                        print("Gebe die Koordinaten des Wegpunktes ein\n")
                        while while_running_w:
                                screen.blit(plan, (0, 0))
                                pygame.display.flip()
                                for event in pygame.event.get():

                                        # speichern der Koordinate
                                        if event.type == pygame.MOUSEBUTTONDOWN:
                                                c_x, c_y = pygame.mouse.get_pos()
                                                print("Die Koordinate wurden gespeichert")
                                                print(f"[{c_x}, {c_y}]\n")
                                                waypoint(c_x, c_y)
                                                while_running_w = False

                                        # stoppen des Programms
                                        elif event.type == pygame.QUIT:
                                                while_running_w = False
                                                running = False
                                                break

                                        # abbrechen der Koordinateneingabe
                                        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                                                while_running_w = False
                                                print("Koordinateneingabe abgebrochen!\n")
                                                break
                
                # Prüfen, ob der Polygon Raum ausgewählt wurde
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:

                        print("Gebe die Koordinaten einer Ecke des Poligons an\n")
                        while while_running_p:
                                screen.blit(plan, (0, 0))
                                pygame.display.flip()
                                for event in pygame.event.get():

                                        # speichern der Koordinate
                                        if event.type == pygame.MOUSEBUTTONDOWN:
                                                p_coords.append(pygame.mouse.get_pos()[0])
                                                p_coords.append(pygame.mouse.get_pos()[1])
                                                print("Die Koordinaten wurden gespeichert")
                                                print(f"{p_coords}\n")
                                                print("Gebe die Koordinaten einer Ecke des Poligons an\n")
                                        
                                        # löschen der letzen Koordinate
                                        elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                                                del_coord_y = p_coords.pop()
                                                del_coords_x = p_coords.pop()
                                                print(f"Du hast die letzte Koordinate {del_coords_x}, {del_coord_y} gelöscht!")
                                                print(f"{p_coords}\n")
                                                print("Gebe die Koordinaten einer Ecke des Poligons an\n")
                                        
                                        # abschließen der Koordinateneingabe
                                        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                                                print(f"Abschluss der Koordinateneingabe\nKoordinaten:{p_coords}")
                                                polygon(p_coords, plan_path)
                                                while_running_p = False
                                        
                                        # stoppen des Programms
                                        elif event.type == pygame.QUIT:
                                                while_running_p = False
                                                running = False
                                                break

                                        # abbrechen der Koordinateneingabe
                                        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                                                while_running_p = False
                                                print("Koordinateneingabe abgebrochen!")
                                                break
                                        


                # zurücksetzen der Variablen zum Abbrechen der coordeingabe
                while_running_s = True
                while_running_c = True
                while_running_w = True 
                while_running_p = True

                # Löschen der Werte in der polygon Liste
                p_coords.clear()

        pygame.display.flip()

pygame.quit()
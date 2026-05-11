# coordsbestimmung_überarbeitet
# Theo Glase
# 13.04.2026

import pygame
import ctypes
import math
from coordsbestimmung_Funktionen import square, circle, waypoint, polygon, plan_selection, text_display, question_display

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

# erstellen der temporären positionsvariable
pos = 0

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

                plan = pygame.image.load(fr"{plan_path}")
                plan_w, plan_h = plan.get_size()

                screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
                pygame.display.set_caption("Raumeditor")

                hwmd = ctypes.windll.user32.FindWindowW(None, "Raumeditor")             # hwmd (handle window): Window ID      # windll.user32: angeben der Datei: "user32.dll"; FindWindowW: Funktion zum finden eines Fensters
                ctypes.windll.user32.ShowWindow(hwmd, 3)                                # ShowWindow: Funktion zum ändern des Zustandes eines Fensters (0 = verstecken, 1 = normal anzeigen, 2 = minimieren, 3 = maximieren, 6 = minimieren in die Taskleiste)

                # update von Pygame
                pygame.event.pump()

                screen_info = pygame.display.Info()
                screen_w, screen_h = screen_info.current_w, screen_info.current_h

                pygame.display.set_mode((screen_w, screen_h))

                faktor = min(screen_w/plan_w, screen_h/plan_h, 1.0)

                new_w, new_h = int(plan_w*faktor), int(plan_h*faktor)

                plan = pygame.transform.scale(plan, (new_w, new_h))

                plan_start_x = (screen_w - new_w) // 2
                plan_start_y = (screen_h - new_h) // 2

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

        # färben des Hintergrundes
        screen.fill((47, 91, 235))
        # plazieren des Bildes
        screen.blit(plan, (plan_start_x, plan_start_y))
        # Plazieren des Überschrift
        text_display(screen, "Raum und Wegpunkt Editor", 60, screen_w / 2, screen_w / 8)

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
                                                pos = pygame.mouse.get_pos()
                                                s_x1, s_y1 = pos[0] - plan_start_x, pos[1] - plan_start_y
                                                
                                                print("Die Koordinaten wurden gespeichert")
                                                print(f"[{s_x1}, {s_y1}]\n")
                                                print("Gebe die Koordinate der unteren, rechten Ecke ein\n")
                                                while while_running_s and while_running_s_del:
                                                        for event in pygame.event.get():

                                                                # speichern der zweiten Koordinate
                                                                if event.type == pygame.MOUSEBUTTONDOWN:
                                                                        pos = pygame.mouse.get_pos()
                                                                        s_x2, s_y2 = pos[0] - plan_start_x, pos[1] - plan_start_y
                                                                        print(f"Abschluss der Koordinateneingabe\nKoordinaten: [{s_x1}, {s_y1}, {s_x2}, {s_y2}]\n")
                                                                        square(s_x1, s_y1, s_x2, s_y2, plan_path, scale)
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
                                                pos = pygame.mouse.get_pos()
                                                c_x, c_y = pos[0] - plan_start_x, pos[1] - plan_start_y

                                                print("Die Koordinaten wurden gespeichert")
                                                print(f"[{c_x}, {c_y}]\n")
                                                print("Gebe Koordinaten an, um den Radius zu bestimmen")
                                                while while_running_c and while_running_c_del:
                                                        for event in pygame.event.get():

                                                                # speichern der zweiten Koordinate
                                                                if event.type == pygame.MOUSEBUTTONDOWN:
                                                                        pos = pygame.mouse.get_pos()
                                                                        radius_pos_x, radius_pos_y = pos[0] - plan_start_x, pos[1] - plan_start_y
                                                                        print(f"Abschluss der Koordinateneingabe\nKoordinaten: [{c_x}, {c_y}; Radiuskoordinaten: {radius_pos_x}, {radius_pos_y}; Radius: {math.dist((c_x/scale, c_y/scale), (radius_pos_x/scale, radius_pos_y/scale))}]\n")
                                                                        circle(c_x, c_y, radius_pos_x, radius_pos_y, plan_path, scale)
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
                                                pos = pygame.mouse.get_pos()
                                                c_x, c_y = pos[0] - plan_start_x, pos[1] - plan_start_y
                                                print("Die Koordinate wurden gespeichert")
                                                print(f"[{c_x}, {c_y}]\n")
                                                waypoint(c_x, c_y, plan_path, scale)
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
                                                pos = pygame.mouse.get_pos()
                                                p_x, p_y = pos[0] - plan_start_x, pos[1] - plan_start_y
                                                p_coords.append(p_x)
                                                p_coords.append(p_y)
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
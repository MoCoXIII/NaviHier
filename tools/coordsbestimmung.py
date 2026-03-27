# coordsbestimmung.py
# Theo Glase
# 27.03.2026


import pygame
import customtkinter
import json
import math

# erstelle das root tkinterfenster
root_tk = customtkinter.CTk()
root_tk.withdraw()

# definieren der Funktion zur Eingabe der Namen, sowie ausgabe des formatierten codes


def show_tkinter(x1, y1, x2, y2, selected_shape):
    global scale, index

    # erstellen der Listen
    questions = []
    answers = []
    submit = False

    # erstellen der tkinter zur Eingabe und Ausgabe
    tk = customtkinter.CTkToplevel(root_tk)
    tk.geometry("500x500")
    tk.title("Code")
    tk.resizable(False, False)
    tk.attributes("-topmost", True)
    tk.withdraw()

    tk_input = customtkinter.CTkToplevel(root_tk)
    tk_input.geometry("500x500")
    tk_input.title("Code")
    tk_input.resizable(False, False)
    tk_input.attributes("-topmost", True)

    # definieren der Funktion zum schliessen der tkinter
    def close_tkinter():
        tk.destroy()
        tk_input.destroy()
        root_tk.quit()

    # definieren der Funktion zum kopieren des codes
    def copy_to_clipboard():
        text = textbox.get("1.0", "end-1c")
        tk.clipboard_clear()
        tk.clipboard_append(text)

    # definieren der Funktion zum speichern der Antworten, sowie erstellen des formatierten codes
    def answer_submitted():
        global index

        # hinzufügen der antworten zur Liste
        answers.append(entry.get())
        entry.delete(0, "end")
        index += 1

        # ändern des Labels
        if index < len(questions):
            label.configure(text=questions[index])

        # erstellen des formatierten codes
        else:
            tk_input.withdraw()
            tk.deiconify()
            if selected_shape == "s":
                data = {
                    "names": [
                        f"{answers[0]}",
                        f"{answers[1]}",
                        f"{answers[2]}"
                    ],
                    "shape": "rect",
                    "coords": [
                        x1/scale,
                        y1/scale,
                        x2/scale,
                        y2/scale
                    ]
                }

                code = json.dumps(data, indent=4)

                textbox.insert("0.0", code)
                textbox.configure(state="disabled")

            elif selected_shape == "c":
                data = {
                    "names": [
                        f"{answers[0]}",
                        f"{answers[1]}",
                        f"{answers[2]}"
                    ],
                    "shape": "rect",
                    "coords": [
                        x1/scale,
                        y1/scale,
                        math.dist((x1/scale, y1/scale), (x2/scale, y2/scale))
                    ]
                }

                code = json.dumps(data, indent=4)

                textbox.insert("0.0", code)
                textbox.configure(state="disabled")

            elif selected_shape == "w":
                data = {
                    "id": f"{answers[0]}",
                    "x": 186,
                    "y": 133,
                    "links": [
                        f"{answers[1]}",
                        f"{answers[2]}",
                        f"{answers[3]}",
                        f"{answers[4]}"
                    ]
                }

                code = json.dumps(data, indent=4)

                textbox.insert("0.0", code)
                textbox.configure(state="disabled")

    # erstellen der Elemente des ausgabetkinter
    textbox = customtkinter.CTkTextbox(
        tk, width=400, height=300, font=("Courier", 14))
    copy_button = customtkinter.CTkButton(
        tk, text="Kopieren", command=copy_to_clipboard)
    quit_button = customtkinter.CTkButton(
        tk, text="Schliessen", command=close_tkinter)

    # platzieren der Elemente
    textbox.grid(row=0, column=0, padx=10, pady=10)
    copy_button.grid(row=1, column=0, padx=10, pady=10)
    quit_button.grid(row=2, column=0, padx=10, pady=10)

    # erstellen der Elemente des eingabetkinter
    label = customtkinter.CTkLabel(tk_input, text="")
    entry = customtkinter.CTkEntry(
        tk_input, width=400, height=300, font=("Arial", 14))
    submit_button = customtkinter.CTkButton(
        tk_input, text="Bestätigen", command=answer_submitted)

    # platzieren der Elemente
    label.grid(row=0, column=0, padx=10, pady=10)
    entry.grid(row=1, column=0, padx=10, pady=10)
    submit_button.grid(row=3, column=0, padx=10, pady=10)

    # hinzufügen der Fragen in die Liste
    if selected_shape == "s" or selected_shape == "c":
        questions = [
            "Gib die Nr des Raumes ein",
            "Gib den Namen des Raumes ein",
            "Gib den zweiten Namen des Raumes ein"
        ]
        index = 0
        label.configure(text=questions[index])

    elif selected_shape == "w":
        questions = [
            "Gib die Wegpunktnummer ein",
            "Gib den ersten Wegpunktlink ein",
            "Gib den zweiten Wegpunktlink ein",
            "Gib den dritten Wegpunktlink ein",
            "Gib den vierten Wegpunktlink ein"
        ]
        index = 0
        label.configure(text=questions[index])

    root_tk.mainloop()


# initialisieren von Pygame
pygame.init()

# erstellen der Variablen
screen = pygame.display.set_mode((1500, 1000))
plan = pygame.image.load(r"C:\Bell\NaviHier\Test Gebäudeplan\Gebäudeplan.png")
plan = pygame.transform.scale(plan, (1500, 1000))

x1 = 0
y1 = 0
x2 = 0
y2 = 0
while_running_square = True
while_running_circle = True
while_running_waypoint = True
selected_shape = ""

scale = 1000/plan.get_width()

print("press s for square, c for circle, w for waypoint\nto stop coords input press escape")

# mainloop von Pygame
running = True
while running:

    # plazieren des Bildes
    screen.blit(plan, (0, 0))

    for event in pygame.event.get():

        # prüfen, ob das Fenster geschlossen wird
        if event.type == pygame.QUIT:
            running = False

        # prüfen, was ausgewählt wurde
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            selected_shape = "s"
            print("put in first square coord")
            while while_running_square:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # eingabe der ersten Koordinaten
                        x1, y1 = pygame.mouse.get_pos()
                        print("put in second square coord")
                        while while_running_square:
                            for event in pygame.event.get():
                                # eingabe der zweiten Koordinaten
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    x2, y2 = pygame.mouse.get_pos()
                                    # ausführen der ein - und ausgabefunktion
                                    show_tkinter(x1, y1, x2, y2,
                                                 selected_shape)
                                    selected_shape = ""
                                    while_running_square = False
                                    break
                                # prüfen, ob das Fenster geschlossen wird
                                elif event.type == pygame.QUIT:
                                    running = False
                                    while_running_square = False
                                    break
                                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                                    print("stopped coords input")
                                    selected_shape = ""
                                    while_running_square = False
                                    break
                    # prüfen, ob das Fenster geschlossen wird
                    elif event.type == pygame.QUIT:
                        running = False
                        while_running_square = False
                        break
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        print("stopped coords input")
                        selected_shape = ""
                        while_running_square = False
                        break

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
            selected_shape = "c"
            print("put in the coords of the location of the circle")
            while while_running_circle:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # eingabe der Koordinaten des Kreises
                        x1, y1 = pygame.mouse.get_pos()
                        print("put in another coord to define the radius of the circle")
                        while while_running_circle:
                            for event in pygame.event.get():
                                # eingabe der zweitetn Koordinaten zur Berechnung des Radius des Kreises
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    x2, y2 = pygame.mouse.get_pos()
                                    # ausfüren der ein - und ausgabefunktion
                                    show_tkinter(x1, y1, x2, y2,
                                                 selected_shape)
                                    selected_shape = ""
                                    while_running_circle = False
                                    break
                                # prüfen, ob das Fenster geschlossen wird
                                elif event.type == pygame.QUIT:
                                    running = False
                                    while_running_circle = False
                                    break
                                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                                    selected_shape = ""
                                    print("stopped coords input")
                                    while_running_circle = False
                                    break
                    # prüfen, ob das Fenster geschlossen wird
                    elif event.type == pygame.QUIT:
                        running = False
                        while_running_circle = False
                        break
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        selected_shape = ""
                        print("stopped coords input")
                        while_running_circle = False
                        break

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
            selected_shape = "w"
            print("put in the coords of the location of the waypoint")
            while while_running_waypoint:
                # eingabe der Koordinaten des Waypoints
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x1, y1 = pygame.mouse.get_pos()
                        # ausfüren der ein - und ausgabefunktion
                        show_tkinter(x1, y1, x2, y2, selected_shape)
                        selected_shape = ""
                        while_running_waypoint = False
                        break
                    # prüfen, ob das Fenster geschlossen wird
                    elif event.type == pygame.QUIT:
                        running = False
                        while_running_waypoint = False
                        break
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        selected_shape = ""
                        print("stopped coords input")
                        while_running_waypoint = False
                        break
        
        # zurücksetzen der Variablen der While-Schleifen
        while_running_square = True
        while_running_circle = True
        while_running_waypoint = True

    pygame.display.flip()

pygame.quit()
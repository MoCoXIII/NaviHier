# data_manager
# Theo Glase
# 27.07.2026

#### gui.py
ref_w = 2560
ref_h = 1440

screen = None
plan = None
plan_path = ""

room_creation_screen = None
room_info_screen = None
waypoint_attribute_select = None
widget_geometry = {}
widget_dic = {}

shape = 0

id_answer_list = []
name_answer_list = []
prof_answer_list = []
extrainfo_answer_list = []

#### main.py
plan_start_x = 0
plan_start_y = 0

s_x = 0
s_y = 0
w_x = 0
w_y = 0
pos = 0

s_coords = []
p_coords = []
w_coords = []

s_coords_count = 0
p_coords_count = 0
w_coords_count = 0

s_submit = False
p_submit = False
w_submit = False

scale = 0
gen_faktor_w = 1.0
gen_faktor_h = 1.0
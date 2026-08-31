# data_manager
# Theo Glase
# 27.07.2026

#### gui.py
res_w = 1920
res_h = 1080

screen = None
plan = None
plan_w = 0
plan_h = 0
realplan_w = 0
realplan_h = 0
plan_start_x = 0
plan_start_y = 0
plan_path = ""
plan_path_memory = ""

room_creation_screen = None
room_info_screen = None
poi_widgets = None
stairs_widgets = None
waypoint_attribute_select = None
stairs_waypoint = None
widget_geometry = {}
widget_dic = {}

shape = 0

waypoint_list = []
new_line = False
show_line = True
poi = False
wp_memory = ""
wp_name = ""
connections_list = []
last_wp = ""

id_answer_list = []
name_answer_list = []
prof_answer_list = []
extrainfo_answer_list = []

add_poi = False
add_stairs = False

#### main.py
l_clicked = False
r_clicked = False

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

scale = 0
gen_factor_w = 1.0
gen_factor_h = 1.0

second_plan = False
import numpy as np
import data_manager

def create_vectors():
    lines = []
    for connection in data_manager.connections_list:
        try:
            start = connection["start"]
            end = connection["end"]

            start_pos = [data_manager.widget_dic[start].x + data_manager.widget_dic[start].width // 2, data_manager.widget_dic[start].y + data_manager.widget_dic[start].height // 2]
            end_pos = [data_manager.widget_dic[end].x + data_manager.widget_dic[end].width // 2, data_manager.widget_dic[end].y + data_manager.widget_dic[end].height // 2]
            vector = np.array(end_pos) - np.array(start_pos)
            lines.append({
                "start": np.array(start_pos),
                "end": np.array(end_pos),
                "startwp": connection["start"],
                "endwp": connection["end"],
                "vector": vector
            })
        except KeyError: continue
    return lines

def determine_important_con(pos, lines):
    important_con = []
    for line in lines:
        middle = 1/2 * (line["start"] + line["end"]) # calculate the middle of the connection
        radius = 1/2 * np.linalg.norm(line["vector"]) # calculate the radius of the connectioncircle (connection rotated around the middle)

        # check if the point is inside the connectioncircle
        mp = np.array(pos) - middle
        if np.linalg.norm(mp) <= radius:
            important_con.append(line)
    return important_con

def determine_min_distance(pos, lines):
    distances = []
    # get distance between point and projected point on each connection
    for line in lines:
        # calculate the vector from the connectionstart to the point
        sp = pos - np.array(line["start"])

        # calculate the normed vector of the connection
        normed_vector = line["vector"] / np.linalg.norm(line["vector"]) # vector divided by its length

        # calculate the projection of the point onto the connection
        projection_length = np.dot(normed_vector, sp) # dotproduct between the normed vector and the vector from the connection start to the point

        # calculate the projected point on the connection
        projected_point = np.array(line["start"]) + projection_length * normed_vector # connection start + projection length * normed vector

        # calculate the distance between the point and the projected point
        distance = np.linalg.norm(pos - projected_point)

        distances.append({
            "start": line["start"].tolist(),
            "end": line["end"].tolist(),
            "startwp": line["startwp"], # added: names of the waypoints, so the right connection can be returned
            "endwp": line["endwp"],
            "distance": distance,
            "projectet_point": projected_point.tolist()
        })

    # no connection nearby -> return a tuple, so unpacking doesn't fail
    if not distances:
        return None, None

    min_dist = min(distances, key=lambda x: x["distance"])
    con = {
        "start": min_dist["startwp"], # now taken from the closest connection, not from the last line of the loop
        "end": min_dist["endwp"]
    }
    return min_dist, con
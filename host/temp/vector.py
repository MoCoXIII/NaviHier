import numpy as np
# example connections
connections = [
    {
         "name": "connection1",
        "from": [0, 0],
        "to": [4, 4]
    },
    {
        "name": "connection2",
        "from": [3, 8],
        "to": [6, 2]
    },
    {
        "name": "connection3",
        "from": [1, 5],
        "to": [7, 3]
    }
]

vectors = []
distances = []

# input example point
coord1 = int(input("Enter the x-coordinate of the selected point: "))
coord2 = int(input("Enter the y-coordinate of the selected point: "))
point = np.array([coord1, coord2])
print("\n")

# create vectors from example connections
for connection in connections:
    vector = {}
    vector["vector"] = np.array(connection["to"]) - np.array(connection["from"])
    vector["name"] = connection["name"]
    vector["from"] = np.array(connection["from"])
    vector["to"] = np.array(connection["to"])
    vectors.append(vector)
    print(vector)

# get distance between point and projected point on each connection
for vector in vectors:
    # calculate the vector from the connectionstart to the point
    ax = point - np.array(vector["from"])
    print(f"Vector from connection start to point: {ax}")

    # calculate the normed vector of the connection
    normed_vector = vector["vector"] / np.linalg.norm(vector["vector"])
    print(f"Normed vector: {normed_vector}")

    # calculate the projection of the point onto the connection
    projection_length = np.dot(normed_vector, ax)
    print(f"Projection length: {projection_length}")

    # calculate the projected point on the connection
    projected_point = np.array(vector["from"]) + projection_length * normed_vector
    print(f"Projected point on connection: {projected_point}")

    # calculate the distance between the point and the projected point
    distance = np.linalg.norm(point - projected_point)
    print(f"Distance from point to connection: {distance}\n")

    distances.append({
        "name": vector["name"],
        "distance": distance
    })

# get minimum distance and corresponding connection
min_distance = min(distances, key = lambda x: x["distance"])
print(f"The closest connection to the point is {min_distance['name']} with a distance of {min_distance['distance']}.")
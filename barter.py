# barter.py
# Daniel Kogan Taseen Islam Aritro Sarkar
# 01.29.2022

import json

def add_points(user, points):
    with open('user.json', 'r') as pointssheet:
        point_json = json.load(pointssheet)
    if user in point_json:
        point_json[user] = float(point_json[user]) + float(points)
    else:
        point_json[user] = points
        #print(point_json)
    writeJSON('user.json', point_json)

def writeJSON(filename, data):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile, indent=4,sort_keys=True)
    return True

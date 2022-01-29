# barter.py
# Daniel Kogan Taseen Islam Aritro Sarkar
# 01.29.2022

import json

def add_points(user, points):
    point_json = readJSON('user.json')
    if user in point_json:
        point_json[user]["points"] = int(point_json[user]["points"]) + int(points)
    else:
        point_json[user]["points"] = points
        #print(point_json)
    writeJSON('user.json', point_json)

def writeJSON(filename, data):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile, indent=4,sort_keys=True)
    return True

def readJSON(filename):
    with open(filename, 'r') as infile:
        data = json.load(infile)
    return data
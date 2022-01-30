# barter.py
# Daniel Kogan Taseen Islam Aritro Sarkar
# 01.29.2022

import json

shop = {
    "basic": [500, 1],
    "super": [2000, 5],
    "galactic": [5000, 15]
}

def add_points(user, points, galaxy):
    point_json = readJSON('user.json')
    if user in point_json:
        point_json[user]["points"] = int(point_json[user]["points"]) + int(points)
        if galaxy not in point_json[user]['discovered']:
            point_json[user]['discovered'].append(galaxy)

    else:
        point_json[user]["points"] = points
        point_json[user]["charms"] = 0
        point_json[user]["discovered"] = []
        point_json[user]['discovered'].append(galaxy)
        #print(point_json)
    writeJSON('user.json', point_json)

def add_charm(user, charm):
    charm_json = readJSON('user.json')
    if user not in charm_json:
        return "Play >galaxy first!"
    points = charm_json[user]["points"]
    if shop[charm][0] > points:
        return "Not enough points"
    charm_json[user]["charms"] = int(charm_json[user]["charms"]) + int(shop[charm][1])
    charm_json[user]["points"] = int(charm_json[user]["points"]) - int(shop[charm][0])
    writeJSON('user.json', charm_json)
    return "Success!"

def writeJSON(filename, data):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile, indent=4,sort_keys=True)
    return True

def readJSON(filename):
    with open(filename, 'r') as infile:
        data = json.load(infile)
    return data
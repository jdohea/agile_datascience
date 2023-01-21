import json


user = password = url = ""
def __init__():
    global user, password, url

    with open('constants.json', 'r') as file:
        constants = json.load(file)

    user = constants['mongo']['name']
    password = constants['mongo']['password']
    url = constants['mongo']['url']

    file.close()

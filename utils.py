import json

def getConfigFromFile():
    with open('config.json' , "r") as json_file:
        config = json.load(json_file)
        json_file.close()
    return config
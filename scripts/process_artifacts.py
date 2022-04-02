import json

def main():

    with open('data/artifacts.json', 'r') as f:
        data = json.load(f)

    print(data[0])
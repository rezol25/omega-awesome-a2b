import json

with open('config.json') as f:
    config = json.load(f)
model_name = config["model_name"]

import json

# Load configuration from the JSON file
with open('config.json') as f:
    config = json.load(f)

# Access the model name using the correct path in the config
model_name = config["model"]["name"]

# Print the model name to verify
print("Model Name:", model_name)

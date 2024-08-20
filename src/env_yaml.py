import yaml

def load_config(file_path="src/env.yaml"):
    with open(file_path, "r") as file:
        config = yaml.safe_load(file)
    return config

config = load_config()

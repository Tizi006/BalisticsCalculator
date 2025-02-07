import json
from pathlib import Path
import platformdirs


# Get the path to the configuration file
def get_config_path():
    app_data_dir = platformdirs.user_config_dir("BallisticCalculator", appauthor=False)
    config_file = Path(app_data_dir) / "config.json"
    return config_file


# Save the gravity value
def save_gravity(gravity):
    config_path = get_config_path()
    config_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
    # Load existing data if it exists
    data = {}
    if config_path.exists():
        with open(config_path, "r") as file:
            data = json.load(file)
    # Update the dictionary with the new gravity value
    data["gravity"] = gravity
    with open(config_path, "w") as file:
        json.dump(data, file)


# Load the gravity value
def load_gravity():
    config_path = get_config_path()
    if config_path.exists():
        with open(config_path, "r") as file:
            data = json.load(file)
            return data.get("gravity", "")
    return ""


# Save the gravity value
def save_reset_hot_key(hot_key):
    config_path = get_config_path()
    config_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
    # Load existing data if it exists
    data = {}
    if config_path.exists():
        with open(config_path, "r") as file:
            data = json.load(file)
    # Update the dictionary with the new hotkey value
    data["hot_key"] = hot_key
    with open(config_path, "w") as file:
        json.dump(data, file)


# Load the gravity value
def load__reset_hot_key():
    config_path = get_config_path()
    if config_path.exists():
        with open(config_path, "r") as file:
            data = json.load(file)
            return data.get("hot_key", "r")
    return "r"

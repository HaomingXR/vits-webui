import secrets
import logging
import string
import shutil
import torch
import yaml
import os

from flask import current_app
from tts_app.auth.models import User
from utils.data_utils import check_is_none

import config
YAML_CONFIG_FILE = os.path.join(config.ABS_PATH, 'config.yaml')

# Paths to Concate at Runtime
AUTO_ASSIGN = ['UPLOAD_FOLDER', 'CACHE_PATH', 'LOGS_PATH']


class Config(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getattr__(self, key):
        if key in self:
            return self[key]
        return None

    def __setattr__(self, key, value):
        self[key] = value


global_config = Config()


def represent_torch_device(dumper, device_obj):
    return dumper.represent_scalar('!torch.device', str(device_obj))

def construct_torch_device(loader, node):
    device_str = loader.construct_scalar(node)
    return torch.device(device_str)

def represent_user(dumper, user_obj):
    return dumper.represent_mapping('!User', {
        'id': user_obj.id,
        'username': user_obj.username,
        'password': user_obj.password
    })

def construct_user(loader, node):
    user_data = loader.construct_mapping(node, deep=True)
    return User(user_data['id'], user_data['username'], user_data['password'])


yaml.add_representer(torch.device, represent_torch_device, Dumper=yaml.SafeDumper)
yaml.add_constructor('!torch.device', construct_torch_device, Loader=yaml.SafeLoader)
yaml.add_representer(User, represent_user, Dumper=yaml.SafeDumper)
yaml.add_constructor('!User', construct_user, Loader=yaml.SafeLoader)


def load_yaml_config(filename=YAML_CONFIG_FILE):
    with open(filename, 'r') as f:
        yaml_config = yaml.safe_load(f)
    logging.info(f"Loading Config from {filename}...\n")
    return Config(yaml_config)

def save_yaml_config(data, filename=YAML_CONFIG_FILE):
    temp_filename = f'{filename}.tmp'

    try:
        data = validate_and_convert_data(data)
        dict_data = dict(data)
        with open(temp_filename, 'w') as f:
            yaml.safe_dump(dict_data, f, default_style="'")
        shutil.move(temp_filename, filename)
        logging.info(f"Saving Config to {filename}...\n")
        current_app.config.update(data)

    except Exception as e:
        logging.error(f"Error while Saving Config: {e}...\n")
        if os.path.exists(temp_filename):
            os.remove(temp_filename)


def validate_and_convert_data(data):
    for key, value in data.items():
        if key in ["LOGS_BACKUPCOUNT", "PORT"] and not isinstance(value, int):
            data[key] = int(value)
        elif key in ["LANGUAGE_AUTOMATIC_DETECT"] and not isinstance(value, list):
            data[key] = []

    for key, value in data["default_parameter"].items():
        if value == "":
            value = getattr(config, key.upper())
            data["default_parameter"][key] = int(value)
        elif key in ["id", "length", "segment_size", "length_zh", "length_ja", "length_en"] and not isinstance(value, int):
            data["default_parameter"][key] = int(value)
        elif key in ["noise", "noisew", "sdp_ratio"] and not isinstance(value, float):
            data["default_parameter"][key] = float(value)

    return data


def generate_secret_key(length=32):
    return secrets.token_hex(length)

def generate_random_username(length=8):
    characters = string.ascii_letters + string.digits
    username = ''.join(secrets.choice(characters) for _ in range(length))
    return username

def generate_random_password(length=16):
    characters = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password


def find_all_models(abs_path):
    models_folder = os.path.join(abs_path, 'models')
    model_paths = []

    for folder in os.listdir(models_folder):
        if os.path.isdir(os.path.join(models_folder, folder)):
            files = os.listdir(os.path.join(models_folder, folder))
            assert len(files) == 2 # .pth & .json

            model = []

            if '.json' in files[0]:
                model.append(os.path.join(folder, files[1]))
                model.append(os.path.join(folder, files[0]))
            else:
                model.append(os.path.join(folder, files[0]))
                model.append(os.path.join(folder, files[1]))

            model_paths.append(model)
        else:
            logging.warning(f'Non-folder {folder} found...\n')

    return model_paths

def init_config():
    global global_config

    model_path = ["MODEL_LIST", "HUBERT_SOFT_MODEL", "DIMENSIONAL_EMOTION_NPY", "DIMENSIONAL_EMOTION_MODEL"]
    default_parameter = ["ID", "FORMAT", "LANG", "LENGTH", "NOISE", "NOISEW", "SEGMENT_SIZE",] # "SDP_RATIO", "LENGTH_ZH", "LENGTH_JA", "LENGTH_EN"

    try:
        global_config.update(load_yaml_config())

    except FileNotFoundError:
        global_config.setdefault("model_config", {})
        global_config.setdefault("default_parameter", {})

        for key, value in vars(config).items():
            if key.islower():
                continue
            if key in model_path:
                global_config["model_config"][key.lower()] = value
            elif key in default_parameter:
                global_config["default_parameter"][key.lower()] = value
            else:
                global_config[key] = value

        logging.info("config.yaml not Found. Creating a new config based on default_config.py\n")

    if check_is_none(global_config.API_KEY):
        if global_config.API_KEY_ENABLED is True:
            secret_key = generate_secret_key()
            global_config["API_KEY"] = secret_key
            logging.info(f"Generating a new API_KEY: {secret_key}\n")

    if getattr(global_config, "users") is None:
        random_username = generate_random_username()
        random_password = generate_random_password()
        logging.info(
            f"New User Generated:\n"
            f"{'-' * 40}\n"
            f"| Username: {random_username:<26} |\n"
            f"| Password: {random_password:<26} |\n"
            f"{'-' * 40}\n"
            f"Please do NOT share this information...\n\n")

        global_config["users"] = {}
        global_config["users"]["admin"] = {f"admin": User(1, random_username, random_password)}

    global_config['model_config']['model_list'] = find_all_models(global_config['ABS_PATH'])

    save_yaml_config(global_config)

    # Set up paths at runtime to avoid hardcode
    for path in AUTO_ASSIGN:
        global_config[path] = os.path.join(global_config['ABS_PATH'], global_config[path])
        logging.debug(f'{path}: {global_config[path]}')

init_config()

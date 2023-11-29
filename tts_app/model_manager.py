from model_manager import ModelManager
from tts_manager import TTSManager
from utils.config_manager import global_config

model_manager = ModelManager()
tts_manager = TTSManager(model_manager)

model_manager.attach(tts_manager)

model_manager.model_init(global_config["model_config"]["model_list"])

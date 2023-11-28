import torch
import os

# Debug Mode for Flask
DEBUG = False

# Local Server port
PORT = 8888

# Path of this Project
ABS_PATH = os.path.dirname(os.path.realpath(__file__))

# Paths to Concate at Runtime
AUTO_ASSIGN = ['UPLOAD_FOLDER', 'CACHE_PATH', 'LOGS_PATH']

# Upload Path
UPLOAD_FOLDER = "upload"

# Cahce Path
CACHE_PATH = "cache"

# Logs Path
LOGS_PATH = "logs"

# Number of Log Files to Backup
LOGS_BACKUPCOUNT = 10

# The interval to clear the upload and cache folders
    # If the value <= 0, the cleaning won't be performed
CLEAN_INTERVAL_SECONDS = 6000

# Save Audio to CACHE_PATH
SAVE_AUDIO = False

# If left empty, it will be determined from the config.json
LANGUAGE_AUTOMATIC_DETECT = []

# Set to True to Enable API Key Authentication
API_KEY_ENABLED = False
# API_KEY is Required for Authentication (will be generated if left empty)
API_KEY = ""

# Enable the Admin Backend Functionality
IS_ADMIN_ENABLED = False

# Define the Route for the Admin Backend
ADMIN_ROUTE = '/admin'

# DEBUG / INFO / WARNING / ERROR / CRITICAL
LOGGING_LEVEL = "INFO"

# Language Identification Library
    # fastlid / langid
LANGUAGE_IDENTIFICATION_LIBRARY = "langid"

# To use the english_cleaner, you need to install espeak and enter the path to the libespeak-ng.dll
# ESPEAK_LIBRARY = ""

# === VITS ===
    # Fill in the model path here
MODEL_LIST = []

# === hubert-vits ===
# HUBERT_SOFT_MODEL = "/Model/foo.pt"

# === w2v2-vits ===
    # Need to have both `model.onnx` and `model.yaml` files in the same path.
# DIMENSIONAL_EMOTION_MODEL = "Model/model.yaml"
    #Dimensional emotion npy file
        # load single npy: "all_emotions.npy"
        # load mutiple npy: ["emotions1.npy", "emotions2.npy"]
# DIMENSIONAL_EMOTION_NPY = "Model/npy"

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

DYNAMIC_LOADING = False


ID = 0

FORMAT = "wav"

LANG = "auto"

LENGTH = 1

NOISE = 0.25

NOISEW = 0.25

# Batch-Processing Threshold
# Will not be processed in batches if value <= 0
SEGMENT_SIZE = 32

# === Bert_VITS2 ===
# SDP_RATIO = 0.2
# LENGTH_ZH = 0
# LENGTH_JA = 0
# LENGTH_EN = 0

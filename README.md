<h1 align="center">VITS Webui</h1>
<p align="center">[English|<a href="README_ZH.md">中文</a>]</p>

<p align="center">A simple Webui that allows you to inference VITS TTS models.<br>
Also comes with API supports to interact with other processes.</p>


## Features
- [x] VITS Text-to-Speech
- [x] GPU Acceleration
- [x] Support for Multiple Models
- [x] Automatic Language Recognition & Processing
- [x] Customize Parameters
- [x] Batch Processing for Long Text 

#### Main Differences of the Fork
- [x] No longer hardcode the paths in Config. The project is now portable.
- [x] Automatically load the model paths. No more manually editing the entry in Config.
- [x] Prioritize PyTorch w/ Nvidia GPU Support. *(Built on `CUDA 11.8`)*
  > Edit `requirements.txt` if using other CUDA versions
- [x] Should not throw issues when installing `fasttext`, at least on Windows
- [x] Clean up a few entries of the Config.
- [x] Removed all Docker related stuffs...
- [x] By default, only supports VITS models. You will need to edit the `config.py` and some other scripts to use VITS2, etc.

> Some original features might me missing!


## Deployment

### 1. Clone the Project

Open the console at the target location, then run the following:
```bash
git clone https://github.com/HaomingXR/vits-webui
```

### 2. Prepare Python

#### Local Installation
- Create a virtual environment using the Python installed on your system *(Tested on `3.10.10`)*

```bash
python -m venv venv
venv\scripts\activate
```

#### Portable Installation
- [Download](https://www.python.org/downloads/) a self-contained Python runtime by using **Windows Embeddable Package** 
- You need to edit the files to enable `pip` to install required packages

### 3. Install Python Dependencies
> Edit `requirements.txt` if using other CUDA versions, or not using Nvidia GPU
```bash
pip install -r requirements.txt
```

### 4. Start

Run the following command to start the service:
```bash
python app.py
```

On Windows, you can also run `webui.bat` to directly launch the service.
> Edit the file and point to the Python runtime


## Model Loading

### 1. Download VITS Models
- You may find various VITS models online, usually on `HuggingFace` spaces
- Download the VITS model files *(including both `.pth` and `.json` files)*

### 2. Loading Models
- Place both the model and config into their own folder, then place the folder inside the `models` directory
- On launch, the system *should* automatically detect the models


# Configs
The file `config.py` contains a few default options. After launching the service for the first time, 
it will generate a `config.yaml` in the directory. All future launches will load this config instead.

## Admin Backend
The **Admin Backend** allows loading and unloading models, with login authentication. 
For added security, you can just disable the backend in the `config.yaml`:

```yaml
'IS_ADMIN_ENABLED': !!bool 'false'
```
> When enabled, it will automatically generate a pair of username and password in `config.yaml`


## API Key
You can enable this setting, so that the API usages require a key to connect.

```yaml
'API_KEY_ENABLED': !!bool 'false'
```
> When enabled, it will automatically generate a random key in `config.yaml`

## Server Port
You can edit this setting to set the local server port for the API.
```yaml
'PORT': !!int '8888'
```


# APIs
- Return the dictionary mapping of IDs to Speaker
```
GET http://127.0.0.1:8888/voice/speakers
```

- Return the audio data speaking <ins>prompt</ins>
> **default parameters** are used when not specified
```
GET http://127.0.0.1:8888/voice/vits?text=prompt
```

## Parameter
**VITS**

| Parameter    | Required | Default Value      | Type  | Instruction                                                                       |
| ------------ | -------- | ------------------ | ----- | --------------------------------------------------------------------------------- |
| text         | true     |                    | str   | Text to speak                                                                     |
| id           | false    | From `config.yaml` | int   | Speaker ID                                                                        |
| format       | false    | From `config.yaml` | str   | wav / ogg / mp3 / flac                                                            |
| lang         | false    | From `config.yaml` | str   | The language of the text to be synthesized                                        |
| length       | false    | From `config.yaml` | float | The length of the synthesized speech. The larger the value, the slower the speed. |
| noise        | false    | From `config.yaml` | float | The randomness of the synthesis                                                   |
| noisew       | false    | From `config.yaml` | float | The length of phoneme pronunciation                                               |
| segment_size | false    | From `config.yaml` | int   | Divide the text into paragraphs based on punctuation marks                        |
| streaming    | false    | false              | bool  | Stream synthesized speech with faster initial response                            |

> Check the original repo for more


# Resources
- **vits**: https://github.com/jaywalnut310/vits
- **MoeGoe**: https://github.com/CjangCjengh/MoeGoe
- **vits-uma-genshin-honkai**: https://huggingface.co/spaces/zomehwh/vits-uma-genshin-honkai
- **vits-models**: https://huggingface.co/spaces/zomehwh/vits-models


# Special Thanks to All the Original Contributors
<img src="https://contrib.rocks/image?repo=artrajz/vits-simple-api"/></a>

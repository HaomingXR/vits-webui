<h1 align="center">VITS Webui</h1>
<p align="center">[<a href="README.md">English</a>|中文]</p>

<p align="center">一個簡單的 VITS 介面<br>
附有 API 功能</p>


## 功能
- [x] VITS 文字轉語音
- [x] GPU 加速
- [x] 支援多個模型
- [x] 自動偵測語言
- [x] 手動控制選項
- [x] 過長文字分成多段短句

#### 與原 Repo 的差異
- [x] 自動偵測路徑，以便未來移動介面
- [x] 自動偵測模型，不用手動輸入路徑
- [x] 安裝支援 Nvidia GPU 的 PyTorch (已用 `CUDA 11.8` 測試)
  > 如果使用不同的 CUDA 版本，編輯 `requirements.txt`
- [x] 安裝`fasttext`時 *應該* 不會再出現問題
- [x] 稍微清理 Config
- [x] 刪除 Docker 相關文件
- [x] 預設只支援 VITS 模型。若要使用其他模型，就需編輯`config.py`等等

> 一些原先的功能可能無法使用


## 佈署

### 1. 下載專案

```bash
git clone https://github.com/HaomingXR/vits-webui
```

### 2. 準備 Python

#### 本地安裝
- 利用系統安裝的 Python 製作 Virtual Environment (已用 `3.10.10` 測試)

```bash
python -m venv venv
venv\scripts\activate
```

#### 可攜式安裝
- [下載](https://www.python.org/downloads/) 自帶的 Python 系統 **Windows Embeddable Package** 

### 3. 安裝 Python 資源
> 如果使用不同的 CUDA 版本或不是使用 Nvidia 顯示卡，編輯 `requirements.txt`
```bash
pip install -r requirements.txt
```

### 4. 執行

```bash
python app.py
```

在 Windows，可以使用 `webui.bat` 直接執行


## 準備模型

### 1. 下載 VITS 模型
- 下載 `.pth` 和 `.json` 檔案

### 2. 載入模型
- 將上述檔案放在一個子資料夾，再將其放至 `models` 資料夾
- 執行時，系統 *應該* 會自動偵測所有模型


# 設定
`config.py` 文件有一些預設的設定。執行第一次後，便會生成一個 `config.yaml` 文件。未來執行都會使用這個新的檔案。

## 管理後臺
使用後臺可以控制模型的載入。可以透過設定將後臺關閉:

```yaml
'IS_ADMIN_ENABLED': !!bool 'false'
```
> 啟用時，會自動產生一組帳號密碼至 `config.yaml` 中


## API Key
透過這項設定，API 便會需要金鑰

```yaml
'API_KEY_ENABLED': !!bool 'false'
```
> 啟用時，會自動產生一把金鑰至 `config.yaml` 中

## Server Port
更改所使用的 Port
```yaml
'PORT': !!int '8888'
```


# APIs
- 回傳所有講者的 ID
```
GET http://127.0.0.1:8888/voice/speakers
```

- 回傳文字轉語音的音訊
```
GET http://127.0.0.1:8888/voice/vits?text=prompt
```

## 參數
**VITS**

| 參數 | 必要 | 預設值 | 種類 | 內容 |
| ------------ | -------- | ------------------ | ----- | ----- |
| text         | true     |                    | str   | 所述說的文字 |
| id           | false    | From `config.yaml` | int   | 講者 ID |
| format       | false    | From `config.yaml` | str   | wav / ogg / mp3 / flac                                                            |
| lang         | false    | From `config.yaml` | str   | 文字的語言 |
| length       | false    | From `config.yaml` | float | 語音長度 |
| noise        | false    | From `config.yaml` | float | 語音的隨機強度 |
| noisew       | false    | From `config.yaml` | float | 發音的長度 |
| segment_size | false    | From `config.yaml` | int   | 過長文字分成多段短句 |
| streaming    | false    | false              | bool  | 串流音訊 |

> 原 Repo 有更詳細的內容


# 資源
- **vits**: https://github.com/jaywalnut310/vits
- **MoeGoe**: https://github.com/CjangCjengh/MoeGoe
- **vits-uma-genshin-honkai**: https://huggingface.co/spaces/zomehwh/vits-uma-genshin-honkai
- **vits-models**: https://huggingface.co/spaces/zomehwh/vits-models


# 特別感謝所有原參與者
<img src="https://contrib.rocks/image?repo=artrajz/vits-simple-api"/></a>

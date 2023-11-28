from pypinyin_dict.phrase_pinyin_data import large_pinyin
from pypinyin_dict.pinyin_data import cc_cedict
import pypinyin
import logging
import jieba
import ast
import os

phrases_dict = {
    "宇萌": [["yǔ"], ["méng"]]
}

def load_phrases_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            additional_phrases = ast.literal_eval(file.read())
            phrases_dict.update(additional_phrases)
            logging.debug(f"Additional phrases loaded from {file_path}...\n")

    except FileNotFoundError:
        logging.debug(f"File {file_path} not found. You can create your own phrases_dict...\n")
    except Exception as e:
        logging.error(f"Error loading additional phrases from {file_path}:\n{str(e)}\n")


def phrases_dict_init(ABS_PATH):
    logging.debug("Loading phrases_dict...\n")
    large_pinyin.load()
    cc_cedict.load()

    additional_phrases_file = os.path.join(ABS_PATH, "phrases_dict.txt")
    load_phrases_from_file(additional_phrases_file)

    for word in phrases_dict.keys():
        jieba.add_word(word)

    pypinyin.load_phrases_dict(phrases_dict)

import requests
from config import YANDEX_DICT


def get_translation(word, lang):
    dictionary_server = 'https://dictionary.yandex.net/api/v1/dicservice.json/lookup'
    params = {'key': YANDEX_DICT,
              'lang': lang,
              'text': word,
              'format': 'json'}
    try:
        return requests.get(dictionary_server, params=params).json()['def'][0]['tr'][0]['text']
    except Exception as e:
        return 'Извините, не удалось перевести текст.'
from fnmatch import fnmatch

import logging
from flask import Flask, request, jsonify

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)


@app.route('/post', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')
    response = {'session': request.json['session'],
                'version': request.json['version'],
                'response': {'end_session': False}}
    handle_dialog(request.json, response)
    logging.info(f'Response:  {response!r}')
    return jsonify(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']
    if req['session']['new']:
        res['response']['text'] = '''Привет, я Алиса-переводчик.
1) Напишите мне "Язык <lang1>-<lang2>", и я изменю направление перевода.
По умолчанию перевод производится с русского на английский (en-ru)
2) Напишите мне "Переведи слово <слово>", и я переведу его на выбранный язык.'''
        sessionStorage[user_id]['lang'] = 'en-ru'
        return
    
    if fnmatch(req['request']['original_utterance'].lower(), 'язык *-*'):
        try:
            _, lang = req['request']['original_utterance'].split()
            res['response']['text'] = f'Направление перевода изменено на {lang}.'
        except Exception:
            res['response']['text'] = 'Некорректная команда.'

    elif fnmatch(req['request']['original_utterance'].lower(), 'переведи* слово *'):
        try:
            _, _, word = req['request']['original_utterance'].split()
            res['response']['text'] = get_translation(word, sessionStorage[user_id]['lang'])
        except Exception:
            res['response']['text'] = 'Слишком много слов.'
            

if __name__ == '__main__':
    app.run()

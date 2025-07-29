from flask import Flask, make_response, request, render_template, jsonify, redirect, url_for
from Assistant.message import Message
from datetime import datetime
from Assistant.model import model
import ast
from os import environ
from static.data import data
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.secret_key = environ.get('SECRET_KEY')

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax'
)

base = [
            "Qual é a capital da França?",
            "Quem escreveu 'Dom Quixote'?",
            "Qual o país que tem a forma de uma bota?",
            "Qual é a cidade luz?",
            "Qual o nome do autor de 'Cem Anos de Solidão'?"
           # "Quais projetos com IA fez?",
           # ""
        ]
response = [
        "A capital da França é Paris.",
        "Miguel de Cervantes escreveu 'Dom Quixote'.",
        "A Itália é o país que tem a forma de uma bota.",
        "Paris é conhecida como a Cidade Luz.",
        "Gabriel García Márquez é o autor de 'Cem Anos de Solidão'."
        ]

#Assistant = model(base, response)

@app.route('/')
def index():
    message_list = []
    consent_cookie = request.cookies.get('user_consented', 'false')
    language = request.cookies.get('language', 'en')
    print(consent_cookie)
    if consent_cookie == 'true':
        message_list = request_messages()

    return render_template(f'{language}/index.html', user_consented=consent_cookie == 'true', messages=message_list)

@app.route('/accept_cookies', methods=['POST'])
def accept_cookies():
    print("Rota /accept_cookies acessada")  # Log no servidor
    resp = make_response(jsonify({
        'success': True,
        'message': 'Cookies aceitos com sucesso'
    }))
    # Define o cookie de consentimento com um longo tempo de vida
    resp.set_cookie('user_consented', 'true', max_age=365 * 24 * 60 * 60, httponly=True) # Válido por 1 ano
    return resp
  #  return render_template('en/index.html', user_consented=True, messages=[])

@app.route('/reject_cookies', methods=['POST'])
def reject_cookies():
    print("Rota /accept_cookies ew")  # Log no servidor
    resp = make_response(jsonify({
        'success': True,
        'message': 'Cookies aceitos com sucesso'
    }))
    resp.set_cookie('user_consented', 'false', max_age=365 * 24 * 60 * 60, httponly=True)
    # Aqui, você também limparia quaisquer cookies de tracking ou outros que dependem do consentimento
    # Ex: resp.delete_cookie('analytics_id')
    return resp


@app.route('/language/en', methods=['GET'])
def to_english():
    cookie_status = request.cookies.get('user_consented', 'false')

    resp = make_response(redirect(url_for('index')))  # ajuste para sua rota principal

    if cookie_status == 'true':
        resp.set_cookie('language', 'en', max_age=365 * 24 * 60 * 60, httponly=True)

    return resp


@app.route('/language/pt', methods=['GET'])
def to_pt():
    cookie_status = request.cookies.get('user_consented', 'false')

    resp = make_response(redirect(url_for('index')))  # ajuste para sua rota principal

    if cookie_status == 'true':
        resp.set_cookie('language', 'pt', max_age=365 * 24 * 60 * 60, httponly=True)

    return resp

@app.route('/api/get_response', methods=['POST'])
def get_response():
    try:
        # Obter dados enviados pelo JavaScript
        data = request.get_json()
        user_message = data.get('message', '')
        user_time = data.get('date', '')

        assistant_response = Assistant.answer_question(user_message)

        if assistant_response is None:
            assistant_response = "I could to respond this question."

        esp = make_response({"success": True, "response": assistant_response, 'timestamp': datetime.now().isoformat()})

        change_cookie(esp, "user_message", Message(user_message, user_time, True).toDict())
        change_cookie(esp, "assistant_message", Message(assistant_response, datetime.now().isoformat(), False).toDict())

        # Retornar resposta em formato JSON
        return esp
     #   return jsonify({
      #      'success': True,
       #     'response': response_text,
        #    'timestamp': datetime.now().isoformat()
        #})
    except Exception as e:
        return make_response({"success": False, "response": str(e), 'timestamp': datetime.now().isoformat()}), 500
    #    return jsonify({
     #       'success': False,
      #      'error': str(e)
       # }), 500

def change_cookie(resp, cookie, value):
    data = request.cookies.get(cookie)
    print(len(data))
    print(data)
    data_list = str_to_list(data)
    if data_list and len(data_list) > 0:
        data_list.append(value)
    else:
        data_list = [value]
        print("dfgfd " + str(value))

    print(data_list)

    resp.set_cookie(cookie, str(data_list),  max_age=365 * 24 * 60 * 60, httponly=True)
 #   data = request.cookies.get(cookie, [])
#    if len(data) > 0:
 #       data.append(value)
  #      resp.set_cookie(cookie, data, max_age=60 * 60 * 24 * 365)
   # else:
    #    resp.set_cookie(cookie, [value], max_age=60 * 60 * 24 * 365)

def request_messages():
    message_list = []
    try:
        user_message = str_to_list(request.cookies.get('user_message', []))
        assistant_message = str_to_list(request.cookies.get('assistant_message', []))

        for user, assistant in zip(user_message, assistant_message):
            message_list.append(user)
            message_list.append(assistant)
    except Exception:
        pass
    return message_list

def str_to_list(text):
    return ast.literal_eval(text)

if __name__ == '__main__':
    app.run(debug=True)
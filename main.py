from flask import Flask, make_response, request, render_template, jsonify, redirect, url_for
from Assistant.message import Message
from datetime import datetime, UTC
from Assistant.model import model
from Database.DB import Messages, connector
from ast import literal_eval
from os import environ
from static.data import data
from dotenv import load_dotenv
from email_service import Email
from threading import Thread

load_dotenv()

app = Flask(__name__)

app.secret_key = environ.get('SECRET_KEY')

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLALCHEMY_DATABASE_URI='sqlite:///messages.db'
)

connector.init_app(app)

with app.app_context():
    connector.create_all()

Assistant = model(data.question, data.answare)

@app.route('/')
def index():
    message_list = []
    consent_cookie = request.cookies.get('user_consented', 'false')
    language = request.cookies.get('language', 'en')
    if consent_cookie == 'true':
        message_list = request_messages()

    return render_template(f'{language}/index.html', user_consented=consent_cookie == 'true', messages=message_list)

@app.route('/accept_cookies', methods=['POST'])
def accept_cookies():
    resp = make_response(jsonify({
        'success': True
    }))
    resp.set_cookie('user_consented', 'true', max_age=30 * 24 * 60 * 60, httponly=True) # Válido por 1 ano
    return resp

@app.route('/reject_cookies', methods=['POST'])
def reject_cookies():
    resp = make_response(jsonify({
        'success': True
    }))
    resp.set_cookie('user_consented', 'false', max_age=30 * 24 * 60 * 60, httponly=True)
    return resp


@app.route('/language/en', methods=['GET'])
def to_english():
    cookie_status = request.cookies.get('user_consented', 'false')

    resp = make_response(redirect(url_for('index')))  # ajuste para sua rota principal

    if cookie_status == 'true':
        resp.set_cookie('language', 'en', max_age=30 * 24 * 60 * 60, httponly=True)

    return resp


@app.route('/language/pt', methods=['GET'])
def to_pt():
    cookie_status = request.cookies.get('user_consented', 'false')

    resp = make_response(redirect(url_for('index')))  # ajuste para sua rota principal

    if cookie_status == 'true':
        resp.set_cookie('language', 'pt', max_age=30 * 24 * 60 * 60, httponly=True)

    return resp

@app.route('/send', methods=['POST'])
def send_message():
    try:
        data_json = request.get_json()
        user_name = data_json.get('name')
        email = data_json.get('email')
        subject = data_json.get('subject')
        message = data_json.get('message')

        language = request.cookies.get('language', 'en')

        row = Messages(username=user_name, email=email, subject=subject, message=message, date=datetime.now(UTC))

        connector.session.add(row)

        connector.session.commit()

        Thread(target=lambda: Email.send_email(email, language == 'en'), daemon=True).start()

        return make_response(jsonify({
        'success': True,
        'message': 'Success to send message.\nAn email has been sent.' if language == 'en' else 'Sucesso a enviar a mensagem.\nUm email será enviado para si.'
    }))
    except Exception as e:
        return make_response(jsonify({ 'success': False, 'message': str(e) })), 500

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

        return esp
    except Exception as e:
        return make_response({"success": False, "response": str(e), 'timestamp': datetime.now().isoformat()}), 500

def change_cookie(resp, cookie, value):
    data = request.cookies.get(cookie)
    data_list = str_to_list(data)
    if data_list and len(data_list) > 0:
        data_list.append(value)
    else:
        data_list = [value]

    resp.set_cookie(cookie, str(data_list),  max_age=30 * 24 * 60 * 60, httponly=True)

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
    return literal_eval(text)

if __name__ == '__main__':
    app.run(debug=True)
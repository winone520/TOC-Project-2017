import sys
from io import BytesIO

import telegram
from flask import Flask, request, send_file

from fsm import TocMachine
from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()

API_TOKEN = '356148980:AAHfSyBim0d8mgT3HhbTHc5Z3v_1cJQ3IoM'
WEBHOOK_URL = 'https://a9b6ede6.ngrok.io/hook'

app = Flask(__name__)
bot = telegram.Bot(token=API_TOKEN)
machine = TocMachine(
    states=[
        'user',
        'help',
        'map',
        'calendar',
        'download',
        'downloadDetail',
        'phone',
        'links',
        'weather',
        'weatherWhere',
        'faultCommand',
        'chat',
        'typingRoom',
        'startState',
        'question',
        'eat'
    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'help',
            'conditions': 'someone_need_help'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'map',
            'conditions': 'NCKU_map'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'download',
            'conditions': 'NCKU_download'
        },
        {
            'trigger': 'advance',
            'source': 'download',
            'dest': 'downloadDetail',
            'conditions': 'NCKU_download_detail'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'map',
            'conditions': 'NCKU_map'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'calendar',
            'conditions': 'NCKU_calendar'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'phone',
            'conditions': 'NCKU_phone'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'links',
            'conditions': 'NCKU_link'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'weather',
            'conditions': 'ask_weather'
        },
        {
            'trigger': 'advance',
            'source': 'weather',
            'dest': 'weatherWhere',
            'conditions': 'ask_weather_where'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'chat',
            'conditions': 'go_chatroom'
        },
        {
            'trigger': 'advance',
            'source': 'chat',
            'dest': 'typingRoom',
            'conditions': 'is_typing'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'startState',
            'conditions': 'is_starting'
        },
        {
            'trigger': 'still_chating',
            'source': 'typingRoom',
            'dest': 'chat'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'question',
            'conditions': 'ask_question'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'eat',
            'conditions': 'ask_food'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'faultCommand',
            'conditions': 'use_fault_command'
        },
        {
            'trigger': 'go_back',
            'source': [
                'help',
                'map',
                'calendar',
                'download',
                'downloadDetail',
                'phone',
                'links',
                'weather',
                'weatherWhere',
                'chat',
                'startState',
                'question',
                'eat',
                'faultCommand'

            ],
            'dest': 'user'
        }
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True,
)


def _set_webhook():
    status = bot.set_webhook(WEBHOOK_URL)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)
    else:
        print('Your webhook URL has been set to "{}"'.format(WEBHOOK_URL))


@app.route('/hook', methods=['POST'])
def webhook_handler():
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        
        state = cache.get(update.message.chat_id) or 'user'
        machine.set_state(state)
        advance_status = machine.advance(update)
        cache.set(update.message.chat_id, machine.state)
        #machine.advance(update)
    return 'ok'



@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    byte_io = BytesIO()
    machine.graph.draw(byte_io, prog='dot', format='png')
    byte_io.seek(0)
    return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')


if __name__ == "__main__":
    _set_webhook()
    app.run()

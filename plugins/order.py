from typing import List
import json
from slackbot.bot import listen_to


@listen_to(r'^!shuffle\s')
def listen_normal_shuffle(message):
    pass


@listen_to(r'^!shuffle')
def listen_custom_shuffle(message):
    send(message, ['あいうえお', 'かきくけこ', 'さしすえそ'])


def get_shuffle_order():
    pass


def send(message, order: List[str]) -> None:
    msg = ' → '.join(order)
    attachments = [
        {
            'text': msg,
            'color': '#56a764'
        }]
    message.send_webapi('', json.dumps(attachments), as_user=False)

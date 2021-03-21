from logging import getLogger, StreamHandler, DEBUG, Formatter
from typing import List, Dict, Any
import json
from random import shuffle
from slackbot.dispatcher import Message
from slackbot.bot import listen_to
from config import get_config, get_member


logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False
handler.setFormatter(Formatter('[labot] %(message)s'))


@listen_to(r'^!shuffle$')
def listen_custom_shuffle(message: Message):
    member = get_member()
    order = get_shuffle_order(member=member, group='student')
    send(message=message, order=order, group='student')


@listen_to(r'^!shuffle\s')
def listen_normal_shuffle(message: Message):
    member = get_member()
    group = message.body['text'].split()[1]
    order = get_shuffle_order(member=member, group=group)
    send(message=message, order=order, group=group)


def get_shuffle_order(member: Dict[str, Dict[str, Any]], group: str) -> List[str]:
    selected_member = []
    if group == 'all':
        selected_member = list(member.keys())
    else:
        selected_member = [k for k, v in member.items() if group in v['group']]

    shuffle(selected_member)
    return selected_member


def send(message: Message, order: List[str], group: str) -> None:
    custom_text = get_config()['order']['text']
    if custom_text == 'DEFAULT':
        text = 'shuffled the order of _{0}_'.format(group)
    else:
        text = custom_text

    msg = '*{}*\n\n'.format(text) + ' → '.join(order)
    attachments = [dict(text=msg, color='#56a764')]
    message.send_webapi('', json.dumps(attachments), as_user=False)

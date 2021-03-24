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
    order = get_shuffle_order(message=message, member=member, _class='student')
    send(message=message, order=order, _class='student')


@listen_to(r'^!shuffle\s')
def listen_normal_shuffle(message: Message):
    member = get_member()
    _class = message.body['text'].split()[1]
    order = get_shuffle_order(message=message, member=member, _class=_class)
    if order:
        send(message=message, order=order, _class=_class)


def get_shuffle_order(message: Message, member: Dict[str, Dict[str, Any]], _class: str) -> List[str]:
    if _class == 'all':
        selected_member = list(member.keys())
    else:
        selected_member = [k for k, v in member.items() if _class in v['class']]

    if len(selected_member) == 0:
        msg = '指定クラス `{0}` に属するメンバーは存在しません'.format(_class)
        attachments = [dict(text=msg, color='#c93a40')]
        message.send_webapi('', json.dumps(attachments), as_user=False)
        return False
    else:
        shuffle(selected_member)
        return selected_member


def send(message: Message, order: List[str], _class: str) -> None:
    custom_text = get_config()['order']['text']
    if custom_text == 'DEFAULT':
        text = '`{0}`のメンバーの順番をシャッフルしました'.format(_class)
    else:
        text = custom_text

    msg = '*{}*\n\n'.format(text) + ' → '.join(order)
    attachments = [dict(text=msg, color='#56a764')]
    message.send_webapi('', json.dumps(attachments), as_user=False)

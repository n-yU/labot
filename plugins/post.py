from logging import getLogger, StreamHandler, DEBUG, Formatter
from typing import List, Dict
import json
from config import get_config, get_slack
from slackbot.dispatcher import Message

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False
handler.setFormatter(Formatter('[labot] %(message)s'))


def get_attachments_by_type(text: str, _type: str) -> List[Dict[str, str]]:
    if _type == 'info':
        attachments = [dict(text=text, color='#56a764')]
    else:
        if _type != 'error':
            text = 'エラー'
        attachments = [dict(text=text, color='#c93a40')]

    return attachments


def slackbot_simple_message(message: Message, text: str, _type: str, pre_text='') -> None:
    attachments = get_attachments_by_type(text=text, _type=_type)
    message.send_webapi('', json.dumps(attachments), as_user=False)


def slacker_simple_message(channel: str, msg: str, _type: str) -> None:
    conf = get_config()
    slack, uname, icon = get_slack(), conf['name'], conf['icon']
    attachments = get_attachments_by_type(text=msg, _type=_type)
    slack.chat.post_message(channel, '', as_user=False, username=uname, icon_url=icon, attachments=attachments)


def slacker_custom_message(channel, attachments: List[Dict[str, str]], text='') -> None:
    pass


def slacker_simple_ephemeral(message: Message, text: str, _type: str) -> None:
    slack, channel, user = get_slack(), message.body['channel'], message.body['user']
    attachments = get_attachments_by_type(text=text, _type=_type)
    slack.chat.post_ephemeral(channel=channel, text='', attachments=attachments, user=user, as_user=True)


def slacker_custom_ephemeral(message: Message, attachments: List[Dict[str, str]], text='') -> None:
    slack, channel, user = get_slack(), message.body['channel'], message.body['user']
    slack.chat.post_ephemeral(channel=channel, text=text, attachments=attachments, user=user, as_user=True)

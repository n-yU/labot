from logging import getLogger, StreamHandler, DEBUG, Formatter
from typing import List, Dict
import json
from config import get_config, get_slack
from slackbot.dispatcher import Message

# ロガー設定
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False
handler.setFormatter(Formatter('[labot] %(message)s'))


def get_attachments_by_type(text: str, _type: str) -> List[Dict[str, str]]:
    """指定メッセージタイプのattachmentsを取得する

    Args:
        text (str): メッセージテキスト
        _type (str): メッセージタイプ

    Returns:
        List[Dict[str, str]]: attachments
    """
    # ref.) attachments    https://qiita.com/daikiojm/items/759ea40c00f9b539a4c8
    # ref.) 配色           http://www.hp-stylelink.com/news/2013/07/20130708.php#lowList01

    if _type == 'info':
        # 情報（正常動作）系
        attachments = [dict(text=text, color='#56a764')]
    else:
        # エラー系
        if _type != 'error':
            # 未定義のメッセージタイプ指定 -> メッセージタイプを直接ユーザに指定させることはないためコード上のミス
            text = 'メッセージタイプ `{0}` は未定義です．恐れ入りますが，Twitter `@nyu923` までお知らせください．'
        attachments = [dict(text=text, color='#c93a40')]

    return attachments


def slackbot_simple_message(message: Message, text: str, _type: str, pre_text='') -> None:
    """slackbotを使ったシングルアタッチメントメッセージ送信

    Args:
        message (Message): slackbot.dispatcher.Message
        text (str): メッセージテキスト
        _type (str): メッセージタイプ
        pre_text (str, optional): attachments前テキスト. Defaults to ''.
    """
    attachments = get_attachments_by_type(text=text, _type=_type)

    # as_user=False -> config.ymlで指定した"name"と"icon"によるtoken発行ユーザによってメッセージ送信
    message.send_webapi('', json.dumps(attachments), as_user=False)


def slackbot_custom_message(message: Message, attachments: List[Dict[str, str]], text='') -> None:
    pass


def slacker_simple_message(channel: str, msg: str, _type: str) -> None:
    """slackerを使ったシングルアタッチメントメッセージ送信

    Args:
        channel (str): 送信チャンネル名
        text (str): メッセージテキスト
        _type (str): メッセージタイプ
    """
    # slackerクライアント＆token発行ユーザ用のユーザ名・アイコン取得
    conf = get_config()
    slack, uname, icon = get_slack(), conf['name'], conf['icon']

    attachments = get_attachments_by_type(text=msg, _type=_type)

    # as_user=False -> "username"と"icon_url"によるtoken発行ユーザによってメッセージ送信
    slack.chat.post_message(channel, '', as_user=False, username=uname, icon_url=icon, attachments=attachments)


def slacker_custom_message(channel: str, attachments: List[Dict[str, str]], pre_text='') -> None:
    """slackerを使ったマルチアタッチメントメッセージ送信

    Args:
        channel (str): 送信チャンネル名
        attachments (List[Dict[str, str]]): attachments
        pre_text (str, optional): attachments前テキスト. Defaults to ''.
    """
    conf = get_config()
    slack, uname, icon = get_slack(), conf['name'], conf['icon']
    slack.chat.post_message(channel=channel, text=pre_text, attachments=attachments,
                            as_user=True, username=uname, icon_url=icon)


def slacker_simple_ephemeral(message: Message, text: str, _type: str) -> None:
    """slackerを使ったシングルアタッチメント隠しメッセージ送信

    Args:
        message (Message): slackbot.dispatcher.Message
        text (str): メッセージテキスト
        _type (str): メッセージタイプ
    """
    # slackerクライアント＆宛先チャンネル・ユーザID取得
    slack, channel, user = get_slack(), message.body['channel'], message.body['user']
    attachments = get_attachments_by_type(text=text, _type=_type)

    # 隠しメッセージ - "only visible to you"と表示される自分自身のみに表示されるメッセージ (ephemeral)
    slack.chat.post_ephemeral(channel=channel, text='', attachments=attachments, user=user, as_user=True)


def slacker_custom_ephemeral(message: Message, attachments: List[Dict[str, str]], pre_text='') -> None:
    """slackerを使ったマルチアタッチメント隠しメッセージ送信

    Args:
        message (Message): slackbot.dispatcher.Message
        attachments (List[Dict[str, str]]): attachments
        pre_text (str, optional): attachments前テキスト. Defaults to ''.
    """
    slack, channel, user = get_slack(), message.body['channel'], message.body['user']
    slack.chat.post_ephemeral(channel=channel, text=pre_text, attachments=attachments, user=user, as_user=True)

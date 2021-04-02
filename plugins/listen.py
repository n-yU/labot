from logging import getLogger, StreamHandler, DEBUG, Formatter
from re import match
from slackbot.dispatcher import Message
from slackbot.bot import listen_to
import plugins.order as order
import plugins.group as group
import plugins.gcalendar as gcal
import plugins.post as post
import config.setting as setting

# ロガー設定
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False
handler.setFormatter(Formatter('[labot] %(asctime)s - %(message)s'))


@listen_to(r'^![a-z]+')
def listen_command(message: Message) -> None:
    """ユーザメッセージからコマンドを受け取り，対応する関数を実行する

    Args:
        message (Message): slackbot.dispatcher.Message
    """
    command = message.body['text']
    display_name = message.user['profile']['display_name']
    is_valid = True

    if match(r'^!shuffle', command):
        # プラグイン: 順番シャッフル
        if match(r'^!shuffle$', command):
            order.custom_shuffle(message)
        elif match(r'^!shuffle\s', command):
            order.normal_shuffle(message)
        else:
            is_valid = False
            error_text = 'shuffleコマンドの形式が間違ってます．\n'
            post.slackbot_simple_message(message, text=error_text, _type='error')
    elif match(r'^!group', command):
        # プラグイン: グループ分け
        if match(r'^!group [a-z][0-9]+ [a-z]+$', command):
            group.group(message)
        else:
            is_valid = False
            error_text = 'groupコマンドの形式が間違ってます．\n'
            post.slackbot_simple_message(message, text=error_text, _type='error')
    elif match(r'!gcal', command):
        # プラグイン: Googleカレンダー
        if match(r'^!gcal$', command):
            gcal.ephemeral_post_event(message)
        else:
            is_valid = False
            error_text = 'gcalコマンドの形式が間違ってます．\n'
            post.slackbot_simple_message(message, text=error_text, _type='error')
    elif match(r'!config', command):
        # 設定読み書き
        if match(r'^!config get member$', command):
            setting.posy_all_member(message)
        elif match(r'^!config get member\s', command):
            setting.post_member(message)
        elif match(r'^!config get cmember$', command):
            setting.post_all_classified_member(message)
        elif match(r'^!config get cmember\s', command):
            setting.post_class_member(message)
        else:
            is_valid = False
            error_text = 'configコマンドの形式が間違ってます．\n'
            post.slackbot_simple_message(message, text=error_text, _type='error')
    else:
        # 存在しないコマンド
        is_valid = False
        error_text = 'コマンドが間違ってます．\n'
        post.slackbot_simple_message(message, text=error_text, _type='error')

    listen_log = 'listen {0}: {1} -> {2}'.format(display_name, command, ('OK' if is_valid else 'NG'))
    logger.debug(listen_log)

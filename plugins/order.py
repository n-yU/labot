from typing import List, Dict, Any
from random import shuffle
from slackbot.dispatcher import Message
from config import get_config, get_member
import plugins.post as post


def custom_shuffle(message: Message) -> None:
    """学生クラスに所属するメンバーの順番をシャッフルし，結果をポストする

    Args:
        message (Message): slackbot.dispatcher.Message
    """
    member = get_member()

    # シャッフル対象のメンバークラスが未付与 -> クラス=学生とみなす
    order = get_shuffle_order(message=message, member=member, _class='student')
    send(message=message, order=order, _class='student')


def normal_shuffle(message: Message) -> None:
    """指定クラスに所属するメンバーの順番をシャッフルし，結果をポストする

    Args:
        message (Message): slackbot.dispatcher.Message
    """
    member = get_member()
    _class = message.body['text'].split()[1]    # !shuffle [class]
    order = get_shuffle_order(message=message, member=member, _class=_class)

    # 指定クラスに所属するメンバーが1人以上 -> シャッフル結果ポスト
    if order:
        send(message=message, order=order, _class=_class)


def get_shuffle_order(message: Message, member: Dict[str, Dict[str, Any]], _class: str) -> List[str]:
    """指定クラスメンバーの順番をシャッフルする

    Args:
        message (Message): slackbot.dispatcher.Message
        member (Dict[str, Dict[str, Any]]): メンバー情報（config.get_member()参照）
        _class (str): メンバークラス

    Returns:
        List[str]: シャッフルされた指定クラスメンバーリスト
    """
    # all -> 全メンバーをシャッフル対象にする
    if _class == 'all':
        selected_member = list(member.keys())
    else:
        selected_member = [k for k, v in member.items() if _class in v['class']]

    if len(selected_member) == 0:
        # 指定クラスメンバーが0人 -> エラーメッセージ返しシャッフルしない
        text = '指定クラス `{0}` に属するメンバーは存在しません'.format(_class)
        post.slackbot_simple_message(message=message, text=text, _type='error')
        return False
    else:
        shuffle(selected_member)
        return selected_member


def send(message: Message, order: List[str], _class: str) -> None:
    """シャッフルされたメンバーリストをポストする

    Args:
        message (Message): slackbot.dispatcher.Message
        order (List[str]): シャッフルされたメンバーリスト
        _class (str): 指定クラス
    """
    # シャッフル順番ポスト時の冒頭テキスト設定
    custom_text = get_config()['order']['text']
    if custom_text == 'DEFAULT':
        if _class == 'all':
            text = '全メンバーの順番をシャッフルしました'
        else:
            text = '`{0}`のメンバーの順番をシャッフルしました'.format(_class)
    else:
        text = custom_text

    # "メンバー → メンバー"という形式で表示
    text = '*{}*\n\n'.format(text) + ' → '.join(order)
    post.slackbot_simple_message(message=message, text=text, _type='info')

from slackbot.dispatcher import Message
from config import get_member
import plugins.post as post


def post_all_member(message: Message) -> None:
    """メンバー設定ファイルに登録されている全メンバーをポストする

    Args:
        message (Message): slackbot.dispatcher.Message
    """
    member = get_member()   # メンバー設定
    attc = []               # メッセージアタッチメント

    for mem_family_name, mem_info in member.items():
        # メンバー設定に登録されているメンバーを順に取得 -> 名前やクラス等表示
        text = '*{}*\n'.format(mem_family_name)
        for k, v in mem_info.items():
            if k == 'class':
                text += '- {}: {}\n'.format(k, ', '.join(v))
            else:
                text += '- {}: {}\n'.format(k, v)

        attc.append(dict(text=text, color='#56a764'))   # 1メンバーあたり1アタッチメント作成

    pre_text = '`member.yml` で設定済の全{0}メンバーは以下の通りです\n'.format(len(member))
    post.slacker_custom_ephemeral(message=message, attachments=attc, text=pre_text)


def post_member(message: Message) -> None:
    """指定したメンバーの詳細をポストする

    Args:
        message (Message): slackbot.dispatcher.Message
    """
    member = get_member()
    mem_family_name = message.body['text'].split()[2].capitalize()  # 指定メンバー（姓）

    try:
        mem_info = member[mem_family_name]
    except KeyError:
        # 指定メンバーが存在しない -> エラー文をポスト
        text = '`{0}` というメンバーは存在しません'.format(mem_family_name)
        post.slacker_simple_ephemeral(message=message, text=text, _type='error')
        return

    text = '*{}*\n'.format(mem_family_name)
    for k, v in mem_info.items():
        if k == 'class':
            text += '- {}: {}\n'.format(k, ', '.join(v))
        else:
            text += '- {}: {}\n'.format(k, v)

    attc = [dict(text=text, color='#56a764')]   # 1メンバーであるためシングルアタッチメント

    pre_text = '`member.yml` で設定済のメンバー `{}` の詳細は以下の通りです\n'.format(mem_family_name)
    post.slacker_custom_ephemeral(message=message, attachments=attc, text=pre_text)


def post_all_classified_member(message: Message) -> None:
    """全メンバーをクラスごとに分類してポストする

    Args:
        message (Message): slackbot.dispatcher.Message
    """
    member = get_member()
    attc = []

    # 全メンバーの所属クラス集合生成
    all_classes = []
    for member_info in member.values():
        all_classes.extend(member_info['class'])
    all_classes = set(all_classes)

    # 各クラスごとに所属メンバーリスト取得
    for _class in all_classes:
        text = '*{}*\n'.format(_class)

        for mem_family_name, mem_info in member.items():
            if _class in mem_info['class']:
                text += '- {} {}\n'.format(mem_info['name'], mem_family_name)

        attc.append(dict(text=text, color='#56a764'))   # 1クラスあたり1アタッチメント作成

    pre_text = '`member.yml` で設定済の全{0}メンバーのクラスは以下の通りです\n'.format(len(member))
    post.slacker_custom_ephemeral(message=message, attachments=attc, text=pre_text)


def post_class_member(message: Message) -> None:
    """指定クラスに所属するメンバーリストをポストする

    Args:
        message (Message): slackbot.dispatcher.Message
    """
    member = get_member()
    _class = message.body['text'].split()[2]    # 指定クラス
    n_member = 0    # 指定クラス所属メンバー数

    text = '*{}*\n'.format(_class)
    for mem_family_name, mem_info in member.items():
        if _class in mem_info['class']:
            text += '- {} {}\n'.format(mem_info['name'], mem_family_name)
            n_member += 1

    if n_member == 0:
        # 指定クラス所属メンバー数が0 -> エラー文をポスト
        text = '`{0}` に所属するメンバーは存在しません'.format(_class)
        post.slacker_simple_ephemeral(message=message, text=text, _type='error')
        return

    attc = [dict(text=text, color='#56a764')]   # 1クラスであるためシングルアタッチメント

    pre_text = '`member.yml` で設定済の`{0}`に所属する{1}メンバーは以下の通りです\n'.format(_class, n_member)
    post.slacker_custom_ephemeral(message=message, attachments=attc, text=pre_text)

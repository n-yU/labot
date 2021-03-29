from logging import getLogger, StreamHandler, DEBUG, Formatter

from slackbot.dispatcher import Message
from slackbot.bot import listen_to

from config import get_member
import plugins.post as post

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False
handler.setFormatter(Formatter('[labot] %(message)s'))


@listen_to(r'^!config member$')
def post_all_member(message: Message) -> None:
    member = get_member()
    attc = []

    for mem_family_name, mem_info in member.items():
        text = '*{}*\n'.format(mem_family_name)
        for k, v in mem_info.items():
            if k == 'class':
                text += '- {}: {}\n'.format(k, ', '.join(v))
            else:
                text += '- {}: {}\n'.format(k, v)

        attc.append(dict(text=text, color='#56a764'))

    pre_text = '`member.yml` で設定済の全{0}メンバーは以下の通りです\n'.format(len(member))
    post.slacker_custom_ephemeral(message=message, attachments=attc, text=pre_text)


@listen_to(r'^!config member\s')
def post_member(message: Message) -> None:
    member = get_member()
    mem_family_name = message.body['text'].split()[2].capitalize()

    text = '*{}*\n'.format(mem_family_name)
    try:
        mem_info = member[mem_family_name]
    except KeyError:
        text = '`{0}` というメンバーは存在しません'.format(mem_family_name)
        post.slacker_simple_ephemeral(message=message, text=text, _type='error')
        return

    for k, v in mem_info.items():
        if k == 'class':
            text += '- {}: {}\n'.format(k, ', '.join(v))
        else:
            text += '- {}: {}\n'.format(k, v)

    attc = [dict(text=text, color='#56a764')]

    pre_text = '`member.yml` で設定済のメンバー `{}` の詳細は以下の通りです\n'.format(mem_family_name)
    post.slacker_custom_ephemeral(message=message, attachments=attc, text=pre_text)


@listen_to(r'^!config cmember$')
def post_all_classified_member(message: Message) -> None:
    member = get_member()
    attc = []

    all_classes = []
    for member_info in member.values():
        all_classes.extend(member_info['class'])
    all_classes = set(all_classes)

    for _class in all_classes:
        text = '*{}*\n'.format(_class)

        for mem_family_name, mem_info in member.items():
            if _class in mem_info['class']:
                text += '- {} {}\n'.format(mem_info['name'], mem_family_name)

        attc.append(dict(text=text, color='#56a764'))

    pre_text = '`member.yml` で設定済の全{0}メンバーのクラスは以下の通りです\n'.format(len(member))
    post.slacker_custom_ephemeral(message=message, attachments=attc, text=pre_text)


@listen_to(r'^!config cmember\s')
def post_class_member(message: Message) -> None:
    member = get_member()
    _class = message.body['text'].split()[2]
    n_member = 0

    text = '*{}*\n'.format(_class)
    for mem_family_name, mem_info in member.items():
        if _class in mem_info['class']:
            text += '- {} {}\n'.format(mem_info['name'], mem_family_name)
            n_member += 1

    if n_member == 0:
        text = '`{0}` に所属するメンバーは存在しません'.format(_class)
        post.slacker_simple_ephemeral(message=message, text=text, _type='error')
        return

    attc = [dict(text=text, color='#56a764')]

    pre_text = '`member.yml` で設定済の`{0}`に所属する{1}メンバーは以下の通りです\n'.format(_class, n_member)
    post.slacker_custom_ephemeral(message=message, attachments=attc, text=pre_text)

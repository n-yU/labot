from logging import getLogger, StreamHandler, DEBUG, Formatter
from typing import List
import json
from slackbot.dispatcher import Message
from slackbot.bot import listen_to

from config import get_config, get_member
from plugins.order import get_shuffle_order

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False
handler.setFormatter(Formatter('[labot] %(message)s'))


@listen_to(r'^!group [a-z][0-9]+ [a-z]+$')
def listen_group(message: Message):
    conf = message.body['text'].split()
    by, ns, _class = conf[1][0], int(conf[1][1:]), conf[2]

    if by in 'ns':
        shuffle_order = get_shuffle_order(message=message, member=get_member(), _class=_class)
        if shuffle_order:
            n_member = len(shuffle_order)

            if ns > n_member:
                msg = '{0}数を指定クラス `{1}` に属する `メンバー数={2}` より小さくして指定してください'.format(
                    ('グループ' if by == 'n' else '1グループメンバー'), _class, n_member)
                attachments = [dict(text=msg, color='#c93a40')]
                message.send_webapi('', json.dumps(attachments), as_user=False)
            elif shuffle_order:
                if by == 'n':
                    group = create_group_by_num(order=shuffle_order, num=ns)
                else:
                    group = create_group_by_size(order=shuffle_order, size=ns)
                send(message=message, by=by, ns=ns, _class=_class, group=group)
    else:
        msg = '指定したグループ分けタイプ `{0}` は定義されていません'.format(by)
        msg += '\n`n` か `s` を指定してください'
        attachments = [dict(text=msg, color='#c93a40')]
        message.send_webapi('', json.dumps(attachments), as_user=False)


def create_group_by_num(order: List[str], num: int) -> List[List[str]]:
    size = len(order) // num
    group = [order[(i * size):(i * size + size)] for i in range(num)]

    for i in range(len(order) % num):
        group[i].append(order[num * size + i])

    return group


def create_group_by_size(order: List[str], size: int):
    num = len(order) // size
    group = [order[(i * size):(i * size + size)] for i in range(num)]

    n_rem_member = len(order) % size
    if n_rem_member > size // 2:
        group.append(order[num * size:])
    else:
        for i in range(len(order) % size):
            group[i % num].append(order[num * size + i])

    return group


def send(message: Message, by: str, ns: int, _class: str, group: List[List[str]]) -> None:
    custom_text = get_config()['group']['text']
    if custom_text == 'DEFAULT':
        text = '*`{0}` のメンバーを `{1}数={2}` でグループ分けしました*'.format(
            _class, ('グループ' if by == 'n' else '1グループメンバー'), ns)
    else:
        text = custom_text

    msg = ''
    for i in range(len(group)):
        msg += 'Group.{0} - '.format(i + 1) + ', '.join(group[i]) + '\n'
    attachments = [dict(text=msg, color='#56a764')]
    message.send_webapi(text, json.dumps(attachments), as_user=False)

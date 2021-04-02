from typing import List
from slackbot.dispatcher import Message
from config import get_config, get_member
from plugins.order import get_shuffle_order
import plugins.post as post


def group(message: Message) -> None:
    """指定設定からグループリストを生成し，結果をポストする

    Args:
        message (Message): slackbot.dispatcher.Message
    """
    # グループ化設定（分割基準と値）得
    # !group [分割基準（アルファベット1文字）][値（0以上の整数）] [メンバークラス]
    group_conf = message.body['text'].split()
    by, ns, _class = group_conf[1][0], int(group_conf[1][1:]), group_conf[2]

    if by in 'ns':
        # グループ分けのランダム化のため，指定クラスメンバーの順番をシャッフル
        shuffle_order = get_shuffle_order(message=message, member=get_member(), _class=_class)

        # シャッフル成功（指定クラスに所属するメンバーが1人以上存在） -> グループ分けプロセスへ
        if shuffle_order:
            n_member = len(shuffle_order)   # メンバー数

            if ns > n_member:
                # メンバー数が指定グループ/1グループメンバー数より小さい -> グループ分け不可のためエラー
                text = '{0}数を指定クラス `{1}` に属する `メンバー数={2}` より小さくして指定してください'.format(
                    ('グループ' if by == 'n' else '1グループメンバー'), _class, n_member)
                post.slackbot_simple_message(message=message, text=text, _type='error')
            else:
                # 分割基準に応じたグループ分け実行
                if by == 'n':
                    group = create_group_by_num(order=shuffle_order, num=ns)
                elif by == 's':
                    group = create_group_by_size(order=shuffle_order, size=ns)
                else:
                    pass

                send(message=message, by=by, ns=ns, _class=_class, group=group)
    else:
        # n, s以外の分割基準は現状未定義
        text = '指定したグループ分けタイプ `{0}` は定義されていません'.format(by)
        text += '\n`n` か `s` を指定してください'
        post.slackbot_simple_message(message=message, text=text, _type='error')


def create_group_by_num(order: List[str], num: int) -> List[List[str]]:
    """グループ数を基準とするグループ分け

    Args:
        order (List[str]): シャッフルメンバーリスト
        num (int): グループ数

    Returns:
        List[List[str]]: グループリスト
    """
    size = len(order) // num    # 1グループメンバー数仮決定
    # シャッフルメンバーリストをsizeごとに分割（余り無視）
    group = [order[(i * size):(i * size + size)] for i in range(num)]

    # 余りメンバーを各グループに順に割り当て（グループ間のメンバー数差を最小にする）
    for i in range(len(order) % num):
        group[i].append(order[num * size + i])

    return group


def create_group_by_size(order: List[str], size: int) -> List[List[str]]:
    """1グループメンバー数を基準とするグループ分け

    Args:
        order (List[str]): シャッフルメンバーリスト
        size (int): 1グループメンバー数

    Returns:
        List[List[str]]: グループリスト
    """
    num = len(order) // size    # グループ数仮決定
    # シャッフルメンバーリストをsizeごとに分割（余り無視）
    group = [order[(i * size):(i * size + size)] for i in range(num)]

    n_rem_member = len(order) % size    # 余りメンバー数
    if n_rem_member > size // 2:
        # 余りが1グループメンバーの過半数 -> 余りメンバーから新たなグループ生成
        group.append(order[num * size:])
    else:
        # 半分未満 -> 余りメンバーを各グループに順に割り当て
        for i in range(len(order) % size):
            group[i % num].append(order[num * size + i])

    return group


def send(message: Message, by: str, ns: int, _class: str, group: List[List[str]]) -> None:
    """グループリストをポストする

    Args:
        message (Message): slackbot.dispatcher.Message
        by (str): 分割基準
        ns (int): 分割基準byにおける値
        _class (str): メンバークラス
        group (List[List[str]]): グループリスト
    """
    # シャッフル順番ポスト時の冒頭テキスト設定
    custom_text = get_config()['group']['text']
    if custom_text == 'DEFAULT':
        text = '*{0}メンバーを `{1}数={2}` でグループ分けしました*\n\n'.format(
            ('全' if _class == 'all' else '`{0}` の'.format(_class)),
            ('グループ' if by == 'n' else '1グループメンバー'), ns)
    else:
        text = custom_text

    # 1グループ1行/メンバーごとにカンマ区切りで表示
    for i in range(len(group)):
        text += 'Group.{0} - '.format(i + 1) + ', '.join(group[i]) + '\n'

    post.slackbot_simple_message(message=message, text=text, _type='info')

import requests
from logging import getLogger, StreamHandler, DEBUG, Formatter
from typing import Tuple, List, Dict
from datetime import datetime as dt
from datetime import timedelta
from slackbot.dispatcher import Message

from config import get_config
import plugins.post as post

# ロガー設定
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False
handler.setFormatter(Formatter('[labot] %(asctime)s - %(message)s'))


def get_week_event(channel: str) -> Tuple[bool, List[Dict[str, str]], str]:
    """ウィークイベントを登録しているGoogleカレンダーから取得する

    Args:
        channel (str): ポストチャンネル名

    Returns:
        Tuple[bool, List[Dict[str, str]], str]: 取得成否，ウィークイベントアタッチメント，冒頭テキスト
    """
    conf = get_config()
    gas = conf['gcalendar']['gas']          # GASウェブアプリURL

    # GASウェブアプリURLがデフォルト -> プラグイン無効
    gas_dummy = 'https://script.google.com/macros/s/******/exec'
    if gas == gas_dummy:
        text = 'Googleカレンダープラグインは無効状態です．\n'
        text += 'プラグインを有効化する際は `config.yml` を編集してください．\n'
        post.slacker_simple_message(channel=channel, text=text, _type='error')
        return False, [], ''

    # start_date = dt(2021, 2, 8)   # デバッグ用
    start_date = dt.now()                       # 取得開始日（実行日）
    end_date = start_date + timedelta(days=7)   # 取得終了日（実行日の7日後）
    # 取得期間
    period = '{0}/{1}~{2}/{3}'.format(start_date.month, start_date.day, end_date.month, end_date.day)

    # ref.) API通信時の例外処理 https://qiita.com/d_kvn/items/5da7f5cdfc8200172a39
    try:
        # GAS経由でGoogleカレンダーから1週間分のイベント取得
        date_params = dict(year=start_date.year, month=start_date.month - 1, day=start_date.day)
        response = requests.get(gas, params=date_params)
        response.raise_for_status()  # HTTPステータスコード確認
        logger.debug('Googleカレンダーから{0}のイベント取得に成功しました'.format(period))
    except requests.RequestException as e:
        # ステータスコード200番台以外 -> エラーログ出力＆メッセージ送信
        logger.debug(e)
        text = 'Googleカレンダーから{0}のイベント取得に失敗しました（ステータスコード: {1}）．\n \
            詳しくはログを確認してください．'.format(period, response.status_code)

        post.slacker_simple_message(channel=channel, text=text, _type='error')
        return False, [], ''

    weekly_events = response.json()  # GASから取得したJSONを辞書に変換

    # 曜日インデックスに対する曜日名・カラー
    wod = dict(zip(list(range(7)), ['月', '火', '水', '木', '金', '土', '日']))
    wod_colors = dict(zip(list(range(7)), list(map(lambda x: '#{}'.format(x), conf['gcalendar']['colors']))))

    attachments = []    # ref.) attachments https://qiita.com/daikiojm/items/759ea40c00f9b539a4c8

    # 1日ごとに1つのアタッチメントを用意
    for elapsed_days in range(7):
        date_events = weekly_events.get(str(elapsed_days))  # 取得開始日からelapsed_days日後の日イベント
        # イベントなし -> アタッチメント作成せず次の日へ
        if date_events is None:
            continue

        # 日付設定
        date = start_date + timedelta(days=elapsed_days)
        text = '*{0:02d}日 ({1})*\n'.format(date.day, wod[date.weekday()])

        # 日イベントの時間とタイトルを順に取得
        for tmp_event_time, event_title in date_events.items():
            # 00:00~00:00 -> 終日扱い
            event_time = '終日' if tmp_event_time == '00:00~00:00' else tmp_event_time
            # "イベントタイトル - イベント時間"形式で1イベント1行表示
            text += '{0} - {1}\n'.format(event_time, event_title)

        attc = dict(text=text, color=wod_colors[date.weekday()])    # アタッチメント（曜日）カラー設定
        attachments.append(attc)

    pre_text = '*【今週({})のイベント】*\n'.format(period)

    return True, attachments, pre_text


def get_schedule(message: Message) -> None:
    """Googleカレンダーからウィークイベントを自動取得する曜日＆時間を取得する

    Args:
        message (Message): slackbot.dispatcher.Message
    """
    dows = dict(zip(['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'],
                    ['月', '火', '水', '木' '金', '土', '日']))
    schedule = get_config()['gcalendar']['time']

    dow, time = dows[schedule[:3]], schedule[3]  # schedule: [dow(アルファベット3文字)][time]
    text = 'Googleカレンダーからのウィークイベント取得は毎週{0}曜{1}時に設定されてます'.format(dow, time)
    post.slacker_simple_ephemeral(message=message, text=text, _type='info')


def ephemeral_post_event(message: Message):
    """コマンドに応じてウィークイベントを取得し，指定チャンネルに隠しメッセージとしてポストする
    """
    conf = get_config()
    channel = conf['gcalendar']['channel']  # ポストチャンネル

    result, attachments, pre_text = get_week_event(channel=channel)
    if result:
        post.slacker_custom_ephemeral(message=message, attachments=attachments, pre_text=pre_text)


def main(message: Message):
    """スケジュール設定に応じてウィークイベントを取得し，指定チャンネルにポストする

    Args:
        message (Message): slackbot.dispatcher.Message
    """
    conf = get_config()
    channel = conf['gcalendar']['channel']  # ポストチャンネル

    result, attachments, pre_text = get_week_event(channel=channel)
    pre_text = '<!channel>\n{}\n\n'.format(conf['gcalendar']['text']) + pre_text
    if result:
        post.slacker_custom_message(channel=channel, attachments=attachments, pre_text=pre_text)


if __name__ == '__main__':
    main()

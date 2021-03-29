import requests
from logging import getLogger, StreamHandler, DEBUG, Formatter
from datetime import datetime as dt
from datetime import timedelta
# from slackbot.bot import listen_to

from config import get_config
import plugins.post as post

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False
handler.setFormatter(Formatter('[labot] %(message)s'))


# @listen_to(r'^!gcal$')
def main(message):
    conf = get_config()
    gas = conf['gcalendar']['gas']

    start_date = dt.now()
    # start_date = dt(2021, 2, 8)
    end_date = start_date + timedelta(days=7)
    date_params = dict(year=start_date.year, month=start_date.month - 1, day=start_date.day)
    period = '{0}/{1}~{2}/{3}'.format(start_date.month, start_date.day, end_date.month, end_date.day)

    # ref.) https://qiita.com/d_kvn/items/5da7f5cdfc8200172a39
    try:
        response = requests.get(gas, params=date_params)
        response.raise_for_status()
        logger.debug('Googleカレンダーから{0}のイベントを取得することに成功しました'.format(period))
    except requests.RequestException as e:
        logger.debug(e)
        msg = 'Googleカレンダーから{0}のイベントを取得することに失敗しました（ステータスコード: {1}）．\n \
            詳しくはログを確認してください．'.format(period, response.status_code)

        post.slacker_simple_message(channel='bot', msg=msg, _type='error')
        return

    weekly_events = response.json()
    wod = dict(zip(list(range(7)), ['月', '火', '水', '木', '金', '土', '日']))
    wod_colors = dict(zip(list(range(7)), list(map(lambda x: '#{}'.format(x), conf['gcalendar']['colors']))))
    attachments = []

    for elapsed_days in range(7):
        date_events = weekly_events.get(str(elapsed_days))
        if date_events is None:
            continue

        date = start_date + timedelta(days=elapsed_days)
        text = '*{0:02d}日 ({1})*\n'.format(date.day, wod[date.weekday()])

        for tmp_event_time, event_title in date_events.items():
            event_time = '終日' if tmp_event_time == '00:00~00:00' else tmp_event_time
            text += '{0} - {1}\n'.format(event_time, event_title)

        attc = dict(text=text, color=wod_colors[date.weekday()])
        attachments.append(attc)

    channel = conf['gcalendar']['channel']
    msg = '<!channel>\n{}\n\n'.format(conf['gcalendar']['msg'])
    msg += '*【今週({})のイベント】*\n'.format(period)
    post.slacker_custom_message(channel=channel, attachments=attachments, text=msg)


if __name__ == '__main__':
    main()

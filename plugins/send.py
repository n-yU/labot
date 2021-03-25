from config import get_config, get_slack


def send_slackbot(msg: str, _type: str):
    pass


def send_slacker(channel: str, msg: str, _type: str):
    conf = get_config()
    slack, uname, icon = get_slack(), conf['name'], conf['icon']

    if _type == 'info':
        attachments = [dict(text=msg, color='#56a764')]
    else:
        if _type != 'error':
            msg = 'エラー'
        attachments = [dict(text=msg, color='#c93a40')]
    slack.chat.post_message(channel, '', as_user=False, username=uname, icon_url=icon, attachments=attachments)

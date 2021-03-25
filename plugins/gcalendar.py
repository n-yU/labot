from logging import getLogger, StreamHandler, DEBUG, Formatter
from config import get_config, get_member, get_slack
from plugins.send import send_slacker

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False
handler.setFormatter(Formatter('[labot] %(message)s'))


def main():
    send_slacker(channel='bot', msg='aiueo', _type='info')


if __name__ == '__main__':
    main()

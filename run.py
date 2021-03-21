from logging import getLogger, StreamHandler, DEBUG, Formatter
from slackbot.bot import Bot
from config import get_config

CONFIG = None

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False
handler.setFormatter(Formatter('[labot] %(message)s'))


def main():
    global CONFIG

    CONFIG = get_config()
    bot = Bot()
    bot.run()
    logger.info('Botの起動に成功しました')


if __name__ == '__main__':
    main()

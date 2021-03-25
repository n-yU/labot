from logging import getLogger, StreamHandler, DEBUG, Formatter
import os
from pathlib import Path
from slackbot.bot import Bot
from config import get_config, CrontabControl

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False
handler.setFormatter(Formatter('[labot] %(message)s'))


def main():
    os.environ['PYTHONPATH'] = '{0}:{1}'.format(
        os.environ.get('PYTHONPATH'), str(Path('./').resolve()))
    conf = get_config()

    crocon = CrontabControl(tabfile=Path('./config/job.txt'))
    crocon.write_job(command='python3 ./plugins/gcalendar.py', time_config=conf['gcalendar']['time'])
    crocon.monitor()

    bot = Bot()
    bot.run()
    logger.info('Botの起動に成功しました')


if __name__ == '__main__':
    main()

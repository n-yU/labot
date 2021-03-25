from logging import getLogger, StreamHandler, DEBUG, Formatter
import os
from pathlib import Path
from joblib import Parallel, delayed
from slackbot.bot import Bot
from config import get_config, CrontabControl


def process(step: int):
    if step == 0:
        conf = get_config()
        crocon = CrontabControl(tabfile=Path('./config/job.txt'))
        crocon.write_job(command='python3 ./plugins/gcalendar.py', time_config=conf['gcalendar']['time'])
        crocon.monitor()
    elif step == 1:
        bot = Bot()
        bot.run()
    else:
        logger = getLogger(__name__)
        handler = StreamHandler()
        handler.setLevel(DEBUG)
        logger.setLevel(DEBUG)
        logger.addHandler(handler)
        logger.propagate = False
        handler.setFormatter(Formatter('[labot] %(message)s'))

        logger.debug('Botの起動に成功しました')


def main():
    os.environ['PYTHONPATH'] = '{0}:{1}'.format(
        os.environ.get('PYTHONPATH'), str(Path('./').resolve()))

    Parallel(n_jobs=3)([delayed(process)(step=step) for step in range(3)])


if __name__ == '__main__':
    main()

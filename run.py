from logging import getLogger, StreamHandler, DEBUG, Formatter
import os
from pathlib import Path
from joblib import Parallel, delayed
from slackbot.bot import Bot
from config import get_config, CrontabControl

VERSION = '1.0.0-alpha'


def process(step: int) -> None:
    """プロセスを並列実行する

    Args:
        step (int): 実行ステップ
    """
    global VERSION

    if step == 1:    # step.1 - ジョブ定期実行のためのCrontabの実行
        conf = get_config()
        crocon = CrontabControl(tabfile=Path('./config/job.txt'))   # Crontabインスタンス生成
        # gcalendarプラグインの定期実行ジョブ設定
        crocon.write_job(command='python3 ./plugins/gcalendar.py', time_config=conf['gcalendar']['time'])
        crocon.monitor()    # ジョブ監視開始
    elif step == 2:  # step.2 - slackbot稼働
        bot = Bot()
        bot.run()
    else:            # step.3 - Bot起動成功通知
        logger = getLogger(__name__)
        handler = StreamHandler()
        handler.setLevel(DEBUG)
        logger.setLevel(DEBUG)
        logger.addHandler(handler)
        logger.propagate = False
        handler.setFormatter(Formatter('[labot] %(asctime)s - %(message)s'))

        logger.debug('labot (v{0}) を起動しました'.format(VERSION))


def main():
    # 自作パッケージ用環境変数設定
    os.environ['PYTHONPATH'] = '{0}:{1}'.format(
        os.environ.get('PYTHONPATH'), str(Path('./').resolve()))

    # crontabとslackbotの実行
    Parallel(n_jobs=3)([delayed(process)(step=step) for step in [1, 2, 3]])


if __name__ == '__main__':
    main()

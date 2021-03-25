from logging import getLogger, StreamHandler, DEBUG, Formatter
from sys import exit
from typing import Dict, Any
from pathlib import Path
import yaml
from slacker import Slacker
from crontab import CronTab

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False
handler.setFormatter(Formatter('[labot] %(message)s'))


class CrontabControl:
    # ref.) https://miyabikno-jobs.com/python-crontab-library/
    def __init__(self, tabfile: Path):
        self.cron = CronTab()
        self.job = None
        self.tabfile = tabfile

    def get_schedule_by_time(self, time_config: str) -> str:
        dows = dict(zip(['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'], list(range(7))))
        try:
            dow = dows[time_config[:3]]
        except KeyError:
            logger.error('指定した曜日"{0}"は無効です'.format(time_config[:3]))
        hour = int(time_config[3])

        schedule = '* {0} * * {1}'.format(hour, dow)
        return schedule

    def write_job(self, command: str, time_config: str) -> None:
        self.job = self.cron.new(command=command)
        schedule = self.get_schedule_by_time(time_config=time_config)
        self.job.setall(schedule)
        self.cron.write(self.tabfile)

    def read_job(self) -> None:
        self.cron = CronTab(tabfile=self.tabfile)

    def monitor(self) -> None:
        self.read_job()
        for result in self.cron.run_scheduler():
            logger.debug('スケジュール設定されたジョブを実行しました')


def get_config() -> Dict[str, Any]:
    config_path = Path('./config/config.yml')

    try:
        with open(config_path) as f:
            conf = yaml.safe_load(f)
    except Exception as e:
        logger.error('コンフィグの読み込みに失敗しました')
        logger.error('フォーマットに問題がある可能性があります')
        logger.error(e)
        exit()

    return conf


def get_member() -> Dict[str, Dict[str, Any]]:
    member_path = Path('./config/member.yml')

    try:
        with open(member_path) as f:
            member = yaml.safe_load(f)
    except Exception as e:
        logger.error('メンバーデータの読み込みに失敗しました')
        logger.error('フォーマットに問題がある可能性があります')
        logger.error(e)
        exit()

    return member


def get_slack() -> Slacker:
    slack = Slacker(get_config()['token'])
    return slack

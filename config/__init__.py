from logging import getLogger, StreamHandler, DEBUG, Formatter
from sys import exit
from typing import Dict, Any
from pathlib import Path
import yaml

from slacker import Slacker
from crontab import CronTab

# ロガー設定
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False
handler.setFormatter(Formatter('[labot] %(message)s'))


class CrontabControl():
    # Crontab管理
    # ref.) https://miyabikno-jobs.com/python-crontab-library/
    def __init__(self, tabfile: Path):
        self.cron = CronTab()
        self.job = None
        self.tabfile = tabfile

    def get_schedule_by_time(self, time_config: str) -> str:
        """time設定からcron用スケジュール文字列を取得する

        Args:
            time_config (str): time設定（曜日（アルファベット３文字）+時間（整数最大2桁））

        Returns:
            str: cron用スケジュール文字列
        """
        dows = dict(zip(['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'], list(range(7))))
        try:
            dow = dows[time_config[:3]]
        except KeyError:
            logger.error('指定した曜日"{0}"は無効です'.format(time_config[:3]))
        hour = int(time_config[3])

        schedule = '* {0} * * {1}'.format(hour, dow)
        return schedule

    def write_job(self, command: str, time_config: str) -> None:
        """タブファイルへジョブを書き込む

        Args:
            command (str): ジョブ実行コマンド
            time_config (str): time設定
        """
        self.job = self.cron.new(command=command)   # 新ジョブ生成
        schedule = self.get_schedule_by_time(time_config=time_config)
        self.job.setall(schedule)       # ジョブスケジュール設定
        self.cron.write(self.tabfile)   # タブファイルへの書き込み

    def read_job(self) -> None:
        """タブファイルのジョブ読み込み
        """
        self.cron = CronTab(tabfile=self.tabfile)

    def monitor(self) -> None:
        """ジョブ監視開始
        """
        self.read_job()
        for result in self.cron.run_scheduler():
            # ジョブスケジュール時に以下実行
            logger.debug('スケジュール設定されたジョブを実行しました')


def get_config() -> Dict[str, Any]:
    """bot設定ファイル（yml形式）を読み込む

    Returns:
        Dict[str, Any]: bot設定
    """
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
    """研究室メンバー設定ファイル（yml形式）を読み込む

    Returns:
        Dict[str, Dict[str, Any]]: 研究室メンバー
    """
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
    """Slackerインスタンス（Python interface for the Slack API）を取得する

    Returns:
        Slacker: Slackerインスタンス
    """
    # ref.) https://github.com/os/slacker

    # インスタンス生成時に設定ファイル記載のAPIトークン参照
    slack = Slacker(get_config()['token'])
    return slack

from logging import getLogger, StreamHandler, DEBUG, Formatter
from sys import exit
from typing import Dict, Any
from pathlib import Path
import yaml

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False
handler.setFormatter(Formatter('[labot] %(message)s'))


def get_config() -> Dict[str, Any]:
    config_path = Path('./config/config.yml')

    try:
        with open(config_path) as f:
            config = yaml.safe_load(f)
    except Exception as e:
        logger.error('コンフィグの読み込みに失敗しました')
        logger.error('フォーマットに問題がある可能性があります')
        logger.error(e)
        exit()

    return config


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

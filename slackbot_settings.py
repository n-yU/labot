# slackbotの設定はすべての設定はconfig.ymlから取得されるため，このファイルの編集は不要です

from config import get_config

config = get_config()

# APIトークン
API_TOKEN = config['token']
# プラグインパッケージ
PLUGINS = ['config', 'plugins']
# Botアイコン
BOT_ICON = config['icon']

# DEFAULT_REPLY = 'デフォルトメッセージ'
# BOT_EMOJI = ':apple:'

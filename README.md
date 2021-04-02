# labot
[v1.0.0] 研究室用スラックボット - *Slack Bot for Laboratory*

- 研究室用のSlackワークスペースを利用している方に便利なSlackボットです．
- 私が所属する大学研究室のSlackワークスペースで以前から実際に稼働していたボットがベースです．
- パブリックなリポジトリは初めてなので，READMEに何を書くか，ディレクトリ構成をどのようにすれば良いか，といった作法的なことがあまりよくわかってません．気になる点がありましたらご指摘いただけると幸いです．
- プルリク大歓迎です．また追加希望等ございましたら，適宜イシューを立てて貰えればと思います．

<!-- ref.) https://github.com/technote-space/toc-generator/blob/master/README.ja.md -->
<!-- START doctoc -->
<!-- END doctoc -->


## 環境
開発環境で，以下では動作確認済みという意味です．特別なことはしてないので3系であれば動くかと思います．

- Python 3.8.2
- [requirements_dev.txt](./requirements_dev.txt)
- まずはお好きな3系バージョンで[requirements.txt](./requirements.txt)のライブラリを入れてみてください（使い方参照）．


## ディレクトリ構成
```
.
├── LICENSE                 ライセンス
├── README.md               今閲覧しているファイル
├── config                  設定関連（詳細は以下設定等参照）
│   ├── __init__.py         設定処理スクリプト
│   ├── _config.yml         Bot設定
│   ├── _gcalendar.gs       Googleカレンダープラグイン用スクリプト
│   ├── _icon.png           Botアイコン
│   ├── _member.yml         研究室メンバー設定
│   ├── setting.py          設定読み書きスクリプト
│   └── [ignore] job.txt    Crontabファイル（自動生成）
├── requirements.txt        必須Pythonパッケージ
├── requirements_dev.txt    必須Pythonパッケージ（開発環境）
├── guide.md                Bot初期設定説明
├── plugins                 Botプラグイン
│   ├── __init__.py         パッケージ用
│   ├── gcalendar.py        プラグイン:Googleカレンダー
│   ├── group.py            プラグイン:グループ分け
│   ├── order.py            プラグイン:順番シャッフル
│   └── post.py             メッセージ投稿
├── run.py                  Bot起動スクリプト
└── slackbot_settings.py    slackbot設定ファイル（編集不要）
```

## 起動までの流れ
1. **本リポジトリをクローンする**
    - 研究室用のサーバーなど，常時稼働できる環境をオススメします．システムへの負担はほとんどないと思います．
    - SSHの場合（鍵設定を別途行ってください）
        ```
        git clone --depth 1 git@github.com:n-yU/labot.git
        ```
    - HTTPSの場合
        ```
        git clone --depth 1 https://github.com/n-yU/labot.git
        ```
    - `--depth 1` はshallow cloneで，リポジトリの最新版のみ取得するオプションです
2. **Pythonインストール＆以下コマンド実行**
    - Pythonのインストール方法は省略します．dockerやvenv等使って用意してください．
    - `3.8.2` で動作確認済みですが，多少バージョンが違っても多分動きます．
        ```
        pip install -r requirements.txt
        ```
3. **初期設定する**
    - 詳細は[guide.md](./guide.md)を確認してください
    - 一部項目は最初に必ず設定しないとBotが全く動作しません

4. **起動する**
    - 通常
        ```
        python3 run.py
        ```
    - サーバーにSSHで接続してBotを常時稼働させたい場合
        ```
        nohup python3 run.py &
        ```
    - 終了時は `ctrl+c` や `kill` など使ってください
    - `config.yml` の設定は再起動の必要なくすぐに反映されます．ただし，APIトークンやGoogleカレンダープラグインのスケジュール設定など，Bot起動時に必要な設定を変更した場合は再起動が必要です．

## 設定
初期設定については[guide.md](./guide.md)をご確認ください．

### Bot設定 - [config.yml](./_config.yml)
```yml
token: x***-********-********-****************
name: bot
icon: https://****.**/***/***.png
order:
  text: DEFAULT
group:
  text: DEFAULT
gcalendar:
  gas: https://script.google.com/macros/s/******/exec
  channel: calendar
  time: mon9
  colors: [f8e352, d5848b, 7b9ad0, 51a1a2, ae8dbc, c08e47, e5ab47]
  text: お疲れ様です！今週も頑張っていきましょう！
```

- `token` - Slack API トークン（[guide.md](./guide.md)参照）
- `name` - Botの名前．Botからメッセージが返される際に適用されます．
- `icon` - Botのアイコン画像ファイル直リンク．Botからメッセージが返される際に適用されます．
- `order` - "プラグイン:順番シャッフル"に関連する設定
    - `text` - シャッフル順番結果メッセージ投稿時の冒頭テキスト
- `group` - "プラグイン:グループ分け"に関連する設定
    - `text` - グループ分け結果メッセージ投稿時の冒頭テキスト
- `gcalendar` - "プラグイン:Googleカレンダー"に関連する設定
    - `gas` - GASウェブアプリURL（[guide.md](./guide.md)参照）
    - `channel` - ウィークイベント投稿チャンネル名
    - `time` - ウィークイベント投稿曜日＆時間（ex. `mon9`）
    - `colors` - 投稿メッセージに使用する曜日カラー．16進数カラーコードで指定する（シャープ不要）．デフォルトカラーは以下の通り．

        <!-- - ref.) https://qiita.com/suin/items/1f3898c1fa108b1e47b1 -->
        ![](https://via.placeholder.com/16/f8e352/FFFFFF/?text=%20) `月 `
        ![](https://via.placeholder.com/16/d5848b/FFFFFF/?text=%20) `火 `
        ![](https://via.placeholder.com/16/7b9ad0/FFFFFF/?text=%20) `水 `
        ![](https://via.placeholder.com/16/51a1a2/FFFFFF/?text=%20) `木 `
        ![](https://via.placeholder.com/16/ae8dbc/FFFFFF/?text=%20) `金 `
        ![](https://via.placeholder.com/16/c08e47/FFFFFF/?text=%20) `土 `
        ![](https://via.placeholder.com/16/e5ab47/FFFFFF/?text=%20) `日 `      
    - `text` - ウィークイベント投稿時の冒頭テキスト

### 研究室メンバー設定 - [member.yml](./_member.yml)
```yml
FamilyName:
  name: LastName
  class: [studen, teacher, B3, B4, M1, M2]
```

- `Family Name` - メンバー姓．順番シャッフルやグループ分けの結果を表示する際に使用されます．キャピタライズしてください．
    - `name` - メンバー名
    - `class`
        - メンバーが所属するクラス．
        - 順番シャッフルやグループ分け時にクラスを指定することで，限定したメンバー集合に対する操作が可能です．- カンマ区切りで1メンバーに対して複数のクラスを設定できます．
        - 学生には必ず `student` クラスを割り当ててください．順番シャッフル時にクラスを指定しない場合，自動的に `student` クラスに所属するメンバー集合が対象になります（進捗報告ゼミを想定した機能です）．
        - `all` というクラス名は与えないでください．


## プラグイン
- このBotには現在以下のプラグイン（機能）が用意されてます．
- コマンド入力時は頭に `!` を必ずつけてください（`/` ではありません）

### [**order**](./plugins/order.py) - 順番シャッフル
- `member.yml` で設定済みのメンバーに対し，指定クラスに所属するメンバーの順番をシャッフルして投稿します．
- 進捗報告ゼミでの発表順や懇親会での話題提供などの順番を決める際に使えます．
- コマンド
    - `!shuffle [class]`
        - `class`: メンバークラス名
    - 例: `student` クラスに所属するメンバー（学生）の順番をシャッフルして投稿します．
        ```
        !shuffle
        ```
    - 例: `!shuffle [class]` の場合，`class`に所属するメンバーがシャッフル対象になります．`student`をクラス名とした場合，上記コマンドと同じ挙動になります．
        ```
        !shuffle M1
        ```
    - 例: クラス名を `all` にすると，`member.yml` に登録されている全メンバーが対象になります．
        ```
        !shuffle all
        ```

### [**group**](./plugins/group.py) - グループ分け
- `member.yml`で設定済みのメンバーに対し，指定クラスに所属するメンバーをグループ分けして投稿します．
- ZoomのBoRの割り当てを決めたいときなどに使えます．
- グループ間のメンバー数差が最小になるように分けられます．
- グループ分けの基準として，グループ数や1グループメンバー数が指定できます．
- コマンド
    - `!group [standard][value] [class]`
        - `standard`: グループ分け基準（`n`:グループ数 / `s`:1グループメンバー数）
        - `value`: グループ分け基準の設定値
        - `class`: メンバークラス名（`all` にすると全メンバーが対象）
    - 例: `student` クラスに所属するメンバー（学生）を3つのグループに分けます．
        ```
        !group n3 student
        ```
    - 例: 全メンバーを対象に2人のグループ（ペア）を作ります．
        ```
        !group n2 all
        ```

### [**gcalendar**](./plugins/gcalencar.py) - Googleカレンダー
- GASで登録したGoogleカレンダーから取得日を含む1週間分のイベント（ウィークイベント）を取得し，投稿します．
- Googleカレンダー登録の詳細は[guide.md](./guide.md)を確認してください．
- ウィークイベントは `config.yml` で指定した曜日＆時間に自動的に毎週投稿されます．

## お問い合わせ
- 本リポジトリについて質問等ありましたら，[Twitter](https://twitter.com/nyu923)へのリプライが最も反応が早いです（DMはご遠慮ください）．
- イシューを立てて頂いても結構です．

# 初期設定ガイド
- labotの初期設定をまとめています．
- 設定を行わない場合，ボットが正常に動作しないため，初回起動の前に必ず行ってください．
- 初期設定の前に，[起動までの流れ](#%E8%B5%B7%E5%8B%95%E3%81%BE%E3%81%A7%E3%81%AE%E6%B5%81%E3%82%8C)の2まで完了していることを確認してください．
- 所要時間は目安です．

## 【1】設定ファイルのコピー
所要時間 - 1分

`labot/config/` にある3つのファイルのコピーを同じ場所に作ってください．`__init__.py` および `setting.py` のコピーは作成しないでください．
- `_config.yml` - ボット全般の設定
- `_member.yml` - 研究室メンバー設定
- `_gcalendar.gs` - Googleカレンダープラグイン用GAS

コピーした各ファイルを以下のように名前変更してください．正しくファイル名が設定されていない場合，ボットが正常に動作しません．なお，変更前のファイル名は例です．
- `_config_copy.yml` -> `config.yml`
- `_member_copy.yml` -> `member.yml`
- `_gcalendar_copy.gs` -> `gcalendar.gs`

アンダースコアから始まるファイルは設定をリセットする際に使用します．設定をリセットする際は，再度ファイルのコピー＆リネームを行ってください．したがって，これらファイルはクローン時の状態から編集しないでください．

`config.yml` には次のステップでボットのAPIトークンを書き込みます．APIトークンを知っているとボットの操作が可能になるため，管理には十分気をつけてください．特に，不特定多数がアクセス可能な環境には絶対にファイルを置かないようにしてください．

## 【2】ワークスペースへのボット追加
所要時間 - 10分

*一部参考 - https://miyabikno-jobs.com/slackbot-api-token/*

- このステップではワークスペースにボットを追加し，labotがボットを操作するためにAPIトークンを取得するところまで行います．
- ボットを追加したいワークスペースは予め用意しておいてください．
- ワークスペースにアプリを追加できる権限を持つユーザが行ってください．

以降説明のために掲載するスクリーンショットは以下環境によるものです．
```
- OS        macOS Big Sur v11.2.2
- Browser   Google Chrome v89.0.4389.114
- Slack     4.14.0
```

まず，Slackでボットを追加したいワークスペースを開いてください．サイドメニューからAppsを見つけ（見つからない場合，Preferencesで表示させる設定が必要），緑丸のエリアにカーソルを乗せると表示される「+」をクリックして，Apps一覧を右に表示させてください．そして，赤丸で囲ったアイコンをクリックしてください（ブラウザが開きます）．

![01_access_apps](https://user-images.githubusercontent.com/51310314/113472594-51526f80-949f-11eb-882e-d6d3b6a2121c.png)

「slack app directory」というサイトにアクセスされます．赤丸で囲った検索バーに `hubot` と入力してください．すると，候補としてスクリーンショットのように表示されますのでクリックしてください．

![02_search_hubot](https://user-images.githubusercontent.com/51310314/113472605-64653f80-949f-11eb-8227-cb41fce9cf63.png)

Hubotのページにアクセスしたところで，右上にボットを稼働したいワークスペースが表示されているか確認してください．もし異なる場合は変更してください．問題なければ，赤丸で囲った「Add to Slack」をクリックしてください．

![03_select_hubot](https://user-images.githubusercontent.com/51310314/113472607-662f0300-949f-11eb-9be3-78346b857c21.png)

ワークスペースへの追加直前にUsername（ボット名）を設定する必要があります（青丸）．ボットの名前を好きなように設定してください．ここで設定したボット名は，ボットからメッセージが送信される際に表示されるものになります．なお，ボット名はいつでも変更できます．

入力が完了したところで，赤丸の「Add Hubot Integration」をクリックしてください．

![04_add_hubot](https://user-images.githubusercontent.com/51310314/113472608-66c79980-949f-11eb-9571-1c675616b51a.png)

ブラウザは閉じず，一旦Slackに戻ってボットを稼働したいワークスペースを開いてください．サイドメニューのAppsに先に指定した名前のHubotが追加されているか確認してください．もし見つからない場合，他のワークスペースに追加されている可能性があります．

![05_check_added](https://user-images.githubusercontent.com/51310314/113472609-67603000-949f-11eb-8873-6dd2c97a8557.png)

ブラウザに戻ると，先ほどのページから以下のようなページに遷移しているはずです．赤丸で囲った部分にボットのAPIトークンが表示されているはずです．

「Setup Instructions」の `HUBOT_SLACK_TOKEN=`のあとに表示されているトークンと，「Integration Settings」の「API Token」に表示されているトークンは同じです．このどちらかをコピーしてください（`HUBOT_SLACK_TOKEN=` は不要です）．

![06_check_token](https://user-images.githubusercontent.com/51310314/113472611-68915d00-949f-11eb-8660-2f3a43a31005.png)

トークンは `x` から始まる文字列のはずです．コピーしたトークンを `config/config.yml` の1行目の `token: ` の後にペーストしてください．この際 `x***-********-********-****************` はダミーなので消してください．

※各行の `:` の後には必ず半角スペースを空けてください．
```yml
token: x***-********-********-****************
...
```

次にボットのアイコンの設定をします．同じページを少し下にスクロールすると「Customize Icon」という項目があるので好きなアイコンや絵文字を設定してください．

![07_customize_icon](https://user-images.githubusercontent.com/51310314/113472612-69c28a00-949f-11eb-83c2-67c1c7bcc760.png)


最後に `config.yml` のボット名とアイコンの設定を行います．先にブラウザ上で設定したボット名とアイコンと同じものを，2,3行目の `name` と `icon` にそれぞれ設定してください．なお，アイコンは画像ファイルへの直リンクを貼ってください（GoogleドライブやDropboxなど活用してください）．
```yml
token: x***-********-********-****************
name: bot
icon: https://****.**/***/***.png
...
```

ここまでの設定が完了したところで，[起動までの流れ](#%E8%B5%B7%E5%8B%95%E3%81%BE%E3%81%A7%E3%81%AE%E6%B5%81%E3%82%8C)の4を行ってボットを起動してみてください．そして，ボットをチャンネルに追加するか，Appsのボットを選択して（ボット宛のダイレクトメッセージ）， `!version` というメッセージを送信してみてください．メンションは不要です．

ボットの稼働に成功していれば，versionコマンドに反応して，間もなくボットからlabotのバージョンのメッセージが送られてくるはずです！


## 【3】設定ファイルの編集
所要時間 - 5分


## 【4】Googleカレンダープラグインの設定
所要時間 - 10分

![01_open_calendar](https://user-images.githubusercontent.com/51310314/113472627-7e9f1d80-949f-11eb-978c-0dae27acfc18.png)
![02_check_id](https://user-images.githubusercontent.com/51310314/113472628-819a0e00-949f-11eb-8dce-b880c3ecbae4.png)
![03_access_gas](https://user-images.githubusercontent.com/51310314/113472629-82cb3b00-949f-11eb-8888-453f07177307.png)
![04_open_editor](https://user-images.githubusercontent.com/51310314/113472630-8363d180-949f-11eb-97e6-ebcca194cc83.png)
![05_open_deploy](https://user-images.githubusercontent.com/51310314/113472632-83fc6800-949f-11eb-99d1-5101680a94cc.png)
![06_select_type](https://user-images.githubusercontent.com/51310314/113472634-8494fe80-949f-11eb-9b25-5181b6ec7039.png)
![07_edit_deploy](https://user-images.githubusercontent.com/51310314/113472635-8494fe80-949f-11eb-9abd-0e29abcf3e9f.png)
![08_copy_url](https://user-images.githubusercontent.com/51310314/113472637-852d9500-949f-11eb-970e-b2e27256d438.png)


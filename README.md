# Ohuro-challenge
おふろチャレンジの Slack bot

Slack に「おふろチャレンジ成功」と書き込んだら褒めてくれる

## おふろチャレンジとは？

面倒なおふろにがんばって入るチャレンジ。おふろに入った人はとてもえらい。

おふろに入ったら成功。このbotがいるチャンネルに「おふろチャレンジ成功」と書き込むと褒めてくれる。

その他の反応は以下の通り
- 「おふろチャレンジ進捗」：これまで何回成功したかを教えてくれる
- 「おふろチャレンジ失敗」：応援してくれる
- 「にゃーん」：にゃーん

## 使い方
リポジトリをクローン

1. Socket Mode の Slack アプリを作成し、ワークスペースにインストール、チャンネルに招待する

2. `.env_example` を複製して `.env` に名前を変更

3. `.env` の内容を編集
  - SLACK_BOT_TOKEN: Slack のアプリの Bot User OAuth Token
  - SLACK_APP_TOKEN: Slack のアプリの App Level Token

4. 以下のコマンドを実行

```bash
docker compose up -d
```
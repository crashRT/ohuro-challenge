import logging
import os
from slack_sdk import WebClient
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.DEBUG)

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

@app.message("おふろチャレンジ成功")
def message_clear(message, say):
    say("えらいにゃ！！")

@app.message("おふろチャレンジ失敗")
def message_fail(message, say):
    say("がんばれにゃ！！")

@app.message("にゃーん")
def message_nyan(message, say):
    say("にゃーん")

if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
    handler.start()
import logging
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
import re

from model import OhuroRecords

OHURO = "(おふろ|お風呂)チャレンジ"

load_dotenv()
logging.basicConfig(level=logging.DEBUG)
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))


@app.message(re.compile(OHURO + "成功"))
def message_clear(message, say):
    user = message["user"]

    # DB に記録
    record = OhuroRecords(user)
    record.save_recprd()

    say("えらいにゃ！！")


@app.message(re.compile(OHURO + "失敗"))
def message_fail(message, say):
    say("がんばれにゃ！！")


@app.message(re.compile(OHURO + "進捗"))
def message_progress(message, say):
    user = message["user"]

    # DB から取得
    records_all = OhuroRecords.get_all_progress(user)
    records_weekly = OhuroRecords.get_weekly_progress(user)

    formatted_records_weekly = OhuroRecords.format_records(records_weekly)

    say(f"今までのおふろチャレンジ成功回数は {len(records_all)} にゃ！")
    say(f"1週間の成功記録は以下のとおりにゃ！")
    say(f">>> {formatted_records_weekly}")
    say(f"1週間のおふろチャレンジ成功率は {round(len(records_weekly) / 7 * 100)}% にゃ！")


@app.message("にゃーん")
def message_nyan(message, say):
    say("にゃーん")


if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
    handler.start()

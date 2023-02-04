import logging
import os
from slack_sdk import WebClient
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()
logging.basicConfig(level=logging.DEBUG)
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

conn = sa.create_engine('sqlite:///db.sqlite3')

Base = declarative_base()
class OhuroRecords(Base):
    id = sa.Column(sa.Integer, primary_key=True)
    user = sa.Column(sa.String)
    date = sa.Column(sa.Date)
    def __init__(self, user, date):
        self.user = user
        self.date = date
    def __repr__(self):
        return "<OhuroRecords('%s', '%s')>" % (self.user, self.date)


@app.message("おふろチャレンジ成功")
def message_clear(message, say):
    user = message["user"]
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
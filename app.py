import logging
import os
from slack_sdk import WebClient
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
import sqlalchemy as sa
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()
logging.basicConfig(level=logging.DEBUG)
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

conn = sa.create_engine('sqlite:///sqlite/db.sqlite3')

Base = declarative_base()
class OhuroRecords(Base):
    __tablename__ = 'ohuro-records'
    __table_args__ = {
        'comment': 'お風呂チャレンジの成功記録'
    }

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    user = sa.Column(sa.String)
    date = sa.Column(sa.DateTime, default=sa.func.now())
    def __init__(self, user, date):
        self.user = user
        self.date = date
    def __repr__(self):
        return "<OhuroRecords('%s', '%s')>" % (self.user, self.date)

Base.metadata.create_all(conn)


@app.message("おふろチャレンジ成功")
def message_clear(message, say):
    user = message["user"]

    # DB に記録
    record = OhuroRecords(user, sa.func.now())
    Session = sessionmaker(bind=conn)
    session = Session()
    session.add(record)
    session.commit()
    
    say("えらいにゃ！！")

@app.message("おふろチャレンジ失敗")
def message_fail(message, say):
    say("がんばれにゃ！！")

@app.message("おふろチャレンジ進捗")
def message_progress(message, say):
    user = message["user"]

    # DB から取得
    Session = sessionmaker(bind=conn)
    session = Session()
    records = session.query(OhuroRecords).filter(OhuroRecords.user == user).all()
    session.commit()
    
    say(f"おふろチャレンジ成功回数は {len(records)} にゃ！")


@app.message("にゃーん")
def message_nyan(message, say):
    say("にゃーん")

if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
    handler.start()
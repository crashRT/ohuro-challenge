import json, requests
import schedule
import time
import os
from dotenv import load_dotenv

from model import OhuroRecords, Users

load_dotenv()
USER_TOKEN = os.environ.get("USER_TOKEN")

print("notify started!!!!!")

reaction_url = "https://misskey.crashrt.work/api/notes/reactions/create"
note_create_url = "https://misskey.crashrt.work/api/notes/create"
headers = {"Content-Type": "application/json"}


def request_challange():
    """
    おふろチャレンジするよう通知する
    """
    print("おふろチャレンジを通知したよ！！！")
    print(Users.get_all_users())
    users = Users.get_notify_users()
    print(users)
    if len(users) == 0:  ## 誰も登録していなかったらなにもしない
        print("だれもいなかった")
        return
    text = "おふろチャレンジ"
    for user in users:
        text = "@{} {}".format(user.username, text)
    note_data = {
        "i": USER_TOKEN,
        "text": text,
        "visibility": "specified",
        "visibleUserIds": [user.userid for user in users],
        "localOnly": False,
        "noExtractMentions": False,
        "noExtractHashtags": False,
        "noExtractEmojis": False,
    }
    r = requests.post(note_create_url, data=json.dumps(note_data), headers=headers)


# schedule.every().day.at("23:00").do(request_challange)
schedule.every(30).seconds.do(request_challange)

while True:
    schedule.run_pending()
    time.sleep(1)

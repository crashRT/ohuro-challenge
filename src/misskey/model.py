import sqlalchemy as sa
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from dateutil import tz

conn = sa.create_engine("sqlite:///sqlite/db.sqlite3")

Base = declarative_base()


class OhuroRecords(Base):
    __tablename__ = "ohuro-records"
    __table_args__ = {"comment": "お風呂チャレンジの成功記録"}

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    user = sa.Column(sa.String)
    date = sa.Column(sa.DateTime, default=sa.func.now())

    def __init__(self, user, date=sa.func.now()):
        self.user = user
        self.date = date

    def __repr__(self):
        return "<OhuroRecords('%s', '%s')>" % (self.user, self.date)

    def save_record(self):
        """
        お風呂チャレンジの成功記録を保存する
        """
        Session = sessionmaker(bind=conn, expire_on_commit=False)
        session = Session()
        session.add(self)
        session.commit()

    @staticmethod
    def get_all_progress(user_id):
        """
        お風呂チャレンジのすべての成功記録を取得する
        """
        Session = sessionmaker(bind=conn, expire_on_commit=False)
        session = Session()
        records_all = (
            session.query(OhuroRecords).filter(OhuroRecords.user == user_id).all()
        )
        session.commit()
        return records_all

    @staticmethod
    def get_weekly_progress(user_id):
        """
        1週間のお風呂チャレンジの成功記録を取得する
        """
        Session = sessionmaker(bind=conn, expire_on_commit=False)
        session = Session()
        records_weekly = (
            session.query(OhuroRecords)
            .filter(OhuroRecords.user == user_id)
            .filter(OhuroRecords.date > sa.func.date(sa.func.now(), "-7 day"))
            .all()
        )
        session.commit()
        return records_weekly

    @staticmethod
    def format_records(records):
        """
        お風呂チャレンジ記録の時刻表示を整形する
        """
        JST = tz.gettz("Asia/Tokyo")
        UTC = tz.gettz("UTC")
        return "\n".join(
            [record.date.astimezone(JST).strftime("%m/%d %H:%M") for record in records]
        )


class Users(Base):
    __tablename__ = "users"
    __table_args__ = {"comment": "ユーザー情報"}

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    userid = sa.Column(sa.String)
    username = sa.Column(sa.String)
    notify = sa.Column(sa.Boolean, default=True)

    def __init__(self, userid: str, username: str, notify: bool = False):
        self.userid = userid
        self.username = username
        self.notify = notify

    def __repr__(self):
        return "<Users('%s', '%s', '%s')>" % (self.userid, self.username, self.notify)

    def save_user(self):
        """
        ユーザー情報を保存する
        """
        Session = sessionmaker(bind=conn, expire_on_commit=False)
        session = Session()
        session.add(self)
        session.commit()

    def subscribe_notify(self):
        """
        通知設定を有効にする
        """
        Session = sessionmaker(bind=conn, expire_on_commit=False)
        session = Session()
        self.notify = True
        session.add(self)
        session.commit()

    def unsubscribe_notify(self):
        """
        通知設定を無効にする
        """
        Session = sessionmaker(bind=conn, expire_on_commit=False)
        session = Session()
        self.notify = False
        session.add(self)
        session.commit()

    @staticmethod
    def get_all_users():
        """
        すべてのユーザー情報を取得する
        """
        Session = sessionmaker(bind=conn, expire_on_commit=False)
        session = Session()
        users = session.query(Users).all()
        session.commit()
        return users

    @staticmethod
    def get_notify_users():
        """
        通知設定が有効なユーザー情報を取得する
        """
        Session = sessionmaker(bind=conn, expire_on_commit=False)
        session = Session()
        users = session.query(Users).filter(Users.notify == True).all()
        session.commit()
        return users

    @staticmethod
    def get_user(userid):
        """
        ユーザー情報を取得する
        """
        Session = sessionmaker(bind=conn, expire_on_commit=False)
        session = Session()
        user = session.query(Users).filter(Users.userid == userid).first()
        session.commit()
        return user


Base.metadata.create_all(conn)

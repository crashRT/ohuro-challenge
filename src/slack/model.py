import sqlalchemy as sa
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from datetime import datetime
from dateutil import tz

DATABASE = "mysql://%s:%s@%s/%s?charset=utf8" % (
    "ohurobot",
    "ohuro-challange",
    "0.0.0.0:33066",
    "ohuro",
)

conn = sa.create_engine(DATABASE)

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


Base.metadata.create_all(conn)

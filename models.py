import datetime

from sqlalchemy import create_engine, Integer, Text, Select, BigInteger, Delete, String, Date, desc
from sqlalchemy.dialects.postgresql import Insert
from sqlalchemy.orm import DeclarativeBase, declared_attr, Session
from sqlalchemy.orm import Mapped, mapped_column

engine = create_engine("postgresql+psycopg2://postgres:1@localhost:5432/data_base", echo=True)


class AbstractClass:
    @classmethod
    async def select(cls, **kwargs):
        with engine.connect() as conn:
            res = conn.execute(Select(cls))
            conn.commit()
            return res

    @classmethod
    async def filter(cls, *criteria):
        with engine.connect() as conn:
            res = conn.execute(Select(cls).filter(*criteria))
            conn.commit()
            return res

    @classmethod
    async def filter_order(cls, *criteria):
        with engine.connect() as conn:
            res = conn.execute(Select(cls).filter(*criteria).order_by(Answer.modul, Answer.lesson))
            conn.commit()
            return res

    @classmethod
    async def create(cls, **kwargs):
        with Session(engine) as session:
            stmt = Insert(cls).values(**kwargs).returning(*cls.__table__.columns)
            result = session.execute(stmt)
            session.commit()
            return result.fetchone()

    @classmethod
    async def order(cls, *criteria):
        with engine.connect() as conn:
            res = conn.execute(Select(cls).order_by(*criteria))
            conn.commit()
            return res

    @classmethod
    async def delete(cls, id):
        with engine.connect() as conn:
            conn.execute(Delete(cls).where(cls.id == id))
            conn.commit()

    @classmethod
    async def select_where_asc(cls, limit, *criteria):
        with engine.connect() as conn:
            res = conn.execute(Select(cls).order_by('id').where(*criteria).limit(limit))
            conn.commit()
            return res

    @classmethod
    async def select_where_desc(cls, limit, *criteria):
        with engine.connect() as conn:
            res = conn.execute(Select(cls).order_by(cls.id.desc()).where(*criteria).limit(limit))
            conn.commit()
            return res
    @classmethod
    async def last_id(cls):
        with Session(engine) as session:
            # stmt = Select(cls.id).order_by(cls.id.desc).first()
            # result = session.query(stmt)
            # session.commit()
            return session.query(cls.id).order_by(desc(cls.id)).first()

    @classmethod
    async def first_id(cls):
        with Session(engine) as session:
            # stmt = Select(cls.id).order_by(cls.id.desc).first()
            # result = session.query(stmt)
            # session.commit()
            return session.query(cls.id).first()




class Base(DeclarativeBase, AbstractClass):
    @declared_attr
    def __tablename__(self):
        result = self.__name__[0].lower()
        for i in self.__name__[1:]:
            if i.isupper():
                result += f'_{i.lower()}'
                continue
            result += i
        return result


class Answer(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    modul: Mapped[str] = mapped_column(Text)
    lesson: Mapped[str] = mapped_column(Text)
    question: Mapped[str] = mapped_column(Text)
    question_number: Mapped[int] = mapped_column(Integer)
    answer: Mapped[str] = mapped_column(Text)


class AmalyotAnswer(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    question: Mapped[str] = mapped_column(Text)
    answer: Mapped[str] = mapped_column(Text)


class PlatformaAnswer(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    question: Mapped[str] = mapped_column(Text)
    answer: Mapped[str] = mapped_column(Text)


class Question(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    question: Mapped[str] = mapped_column(Text)
    user_id: Mapped[str] = mapped_column(BigInteger)


class Complaint(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255))
    phone_number: Mapped[str] = mapped_column(String(255))
    screenshot_check: Mapped[str] = mapped_column(String(255))
    reason_cancel_course: Mapped[str] = mapped_column(String(255))


class Curator(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    curator_id: Mapped[int] = mapped_column(BigInteger)
    question_id: Mapped[int] = mapped_column(BigInteger)
    answer: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(Date)


def create_table():
    Base.metadata.create_all(engine)

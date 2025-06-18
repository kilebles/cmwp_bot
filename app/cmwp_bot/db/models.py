import enum, datetime as dt
from sqlalchemy import BigInteger, Enum, ForeignKey, JSON, Text, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.cmwp_bot.db.session import Base


class ActionType(str, enum.Enum):
    REGISTRATION_FINISHED = 'REGISTRATION_FINISHED'
    SURVEY_STARTED = 'SURVEY_STARTED'
    SURVEY_COMPLETED = 'SURVEY_COMPLETED'
    CLICK_CONTACTS = 'CLICK_CONTACTS'
    CLICK_GET_PLAN = 'CLICK_GET_PLAN'
    CLICK_DISCUSS = 'CLICK_DISCUSS'
    CLICK_MAIL = 'CLICK_MAIL'


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)

    first_name: Mapped[str | None] = mapped_column(Text)
    last_name: Mapped[str | None] = mapped_column(Text)
    company: Mapped[str | None] = mapped_column(Text)
    phone: Mapped[str | None] = mapped_column(Text)

    registered_at: Mapped[dt.datetime] = mapped_column(default=dt.datetime.utcnow)
    survey_completed_at: Mapped[dt.datetime | None]
    last_activity_at: Mapped[dt.datetime] = mapped_column(default=dt.datetime.utcnow)

    answers: Mapped[list['SurveyAnswer']] = relationship(back_populates='user', cascade='all,delete')
    actions: Mapped[list['UserAction']]   = relationship(back_populates='user', cascade='all,delete')


class SurveyAnswer(Base):
    __tablename__ = 'survey_answers'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    question_no: Mapped[int]
    answer: Mapped[str]
    created_at: Mapped[dt.datetime] = mapped_column(default=dt.datetime.utcnow)

    user: Mapped['User'] = relationship(back_populates='answers')


class UserAction(Base):
    __tablename__ = 'user_actions'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    type: Mapped[ActionType] = mapped_column(Enum(ActionType, name='action_type'), nullable=False)
    payload: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[dt.datetime] = mapped_column(default=dt.datetime.utcnow)

    user: Mapped['User'] = relationship(back_populates='actions')

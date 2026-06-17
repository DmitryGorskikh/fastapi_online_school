from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.models.base import Base


class QuestionModel(Base):
    __tablename__ = 'questions'

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    section_id: Mapped[str] = mapped_column(
        ForeignKey('sections.id', ondelete='CASCADE')
    )
    text: Mapped[str] = mapped_column(Text)
    position: Mapped[int] = mapped_column(Integer)
    question_type: Mapped[str] = mapped_column(String(50))
    max_attempts: Mapped[int] = mapped_column(Integer)
    reward_points: Mapped[int] = mapped_column(Integer)

    section: Mapped['SectionModel'] = relationship(
        'SectionModel', back_populates='questions'
    )
    answer_options: Mapped[list['AnswerOptionModel']] = relationship(
        'AnswerOptionModel',
        back_populates='question',
        cascade='all, delete-orphan',
        order_by='AnswerOptionModel.position',
    )
    attempts: Mapped[list['QuestionAttemptModel']] = relationship(
        'QuestionAttemptModel',
        back_populates='question',
        cascade='all, delete-orphan',
        order_by='QuestionAttemptModel.attempt_number',
    )

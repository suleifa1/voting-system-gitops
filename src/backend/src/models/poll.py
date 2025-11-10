from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime, ForeignKey, UniqueConstraint, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from src.database.connection import Base


class Survey(Base):
    """Модель анкеты (опроса)"""
    __tablename__ = "surveys"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), nullable=False, default="draft")  # draft, active, completed
    created_by = Column(Integer, nullable=False)  # ID пользователя (Integer из таблицы users)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    start_date = Column(DateTime(timezone=True), nullable=True)
    end_date = Column(DateTime(timezone=True), nullable=False)
    responses_count = Column(Integer, default=0, nullable=False)  # количество пользователей, прошедших анкету
    is_anonymous = Column(Boolean, default=False, nullable=False)
    
    # Relationships
    questions = relationship("Question", back_populates="survey", cascade="all, delete-orphan")
    
    # Индексы
    __table_args__ = (
        Index('ix_surveys_status', 'status'),
        Index('ix_surveys_created_by', 'created_by'),
        Index('ix_surveys_end_date', 'end_date'),
    )


class Question(Base):
    """Модель вопроса в анкете"""
    __tablename__ = "questions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    survey_id = Column(UUID(as_uuid=True), ForeignKey('surveys.id', ondelete='CASCADE'), nullable=False)
    question_text = Column(Text, nullable=False)
    question_order = Column(Integer, nullable=False)  # порядок вопроса в анкете
    allow_multiple_answers = Column(Boolean, default=False, nullable=False)  # множественный выбор
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    survey = relationship("Survey", back_populates="questions")
    options = relationship("QuestionOption", back_populates="question", cascade="all, delete-orphan")
    answers = relationship("Answer", back_populates="question", cascade="all, delete-orphan")
    
    # Индексы
    __table_args__ = (
        Index('ix_questions_survey_id', 'survey_id'),
    )


class QuestionOption(Base):
    """Модель варианта ответа на вопрос"""
    __tablename__ = "question_options"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question_id = Column(UUID(as_uuid=True), ForeignKey('questions.id', ondelete='CASCADE'), nullable=False)
    option_text = Column(Text, nullable=False)
    option_order = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    question = relationship("Question", back_populates="options")
    answers = relationship("Answer", back_populates="option", cascade="all, delete-orphan")
    
    # Индексы
    __table_args__ = (
        Index('ix_question_options_question_id', 'question_id'),
    )


class Answer(Base):
    """Модель ответа пользователя на вопрос"""
    __tablename__ = "answers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question_id = Column(UUID(as_uuid=True), ForeignKey('questions.id', ondelete='CASCADE'), nullable=False)
    option_id = Column(UUID(as_uuid=True), ForeignKey('question_options.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, nullable=False)  # ID пользователя (Integer из таблицы users)
    answered_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    question = relationship("Question", back_populates="answers")
    option = relationship("QuestionOption", back_populates="answers")
    
    # Индексы и ограничения
    __table_args__ = (
        Index('ix_answers_question_id', 'question_id'),
        Index('ix_answers_user_id', 'user_id'),
        Index('ix_answers_option_id', 'option_id'),
        UniqueConstraint('question_id', 'user_id', 'option_id', name='uq_answers_question_user_option'),
    )

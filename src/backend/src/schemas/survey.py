from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from uuid import UUID


# ===== Question Option Schemas =====
class QuestionOptionBase(BaseModel):
    option_text: str
    option_order: int


class QuestionOptionResponse(QuestionOptionBase):
    id: UUID
    
    class Config:
        from_attributes = True


# ===== Question Schemas =====
class QuestionBase(BaseModel):
    question_text: str
    question_order: int
    allow_multiple_answers: bool = False


class QuestionResponse(QuestionBase):
    id: UUID
    options: List[QuestionOptionResponse] = []
    
    class Config:
        from_attributes = True


# ===== Survey Schemas =====
class SurveyBase(BaseModel):
    title: str
    description: Optional[str] = None


class SurveyListResponse(SurveyBase):
    id: UUID
    status: str
    created_at: datetime
    end_date: datetime
    responses_count: int
    is_anonymous: bool
    
    class Config:
        from_attributes = True


class SurveyFullResponse(SurveyListResponse):
    """Полная анкета со всеми вопросами и вариантами"""
    questions: List[QuestionResponse] = []
    
    class Config:
        from_attributes = True


# ===== Answer Schemas =====
class AnswerSubmit(BaseModel):
    """Ответ пользователя на один вопрос"""
    question_id: UUID
    option_ids: List[UUID] = Field(..., min_length=1)  # список выбранных вариантов


class SurveyAnswersSubmit(BaseModel):
    """Ответы пользователя на всю анкету"""
    survey_id: UUID
    answers: List[AnswerSubmit]


class SurveyStartResponse(BaseModel):
    """Ответ при начале прохождения анкеты"""
    survey_id: UUID
    message: str
    started_at: datetime


class SurveyCompleteResponse(BaseModel):
    """Ответ при завершении анкеты"""
    survey_id: UUID
    message: str
    completed_at: datetime


# ===== Results Schemas =====
class OptionResult(BaseModel):
    """Результат по одному варианту ответа"""
    option_id: UUID
    option_text: str
    votes_count: int
    percentage: float


class QuestionResult(BaseModel):
    """Результат по одному вопросу"""
    question_id: UUID
    question_text: str
    total_answers: int
    options: List[OptionResult]


class SurveyResults(BaseModel):
    """Результаты всей анкеты"""
    survey_id: UUID
    survey_title: str
    total_responses: int
    questions: List[QuestionResult]

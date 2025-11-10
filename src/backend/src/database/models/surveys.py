from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from typing import List, Optional, Dict, Any
from uuid import UUID

from src.models.poll import Survey, Question, QuestionOption, Answer


async def get_all_surveys(
    db: AsyncSession,
    status_filter: Optional[str] = None
) -> List[Survey]:
    """Получить список всех анкет"""
    query = select(Survey)
    
    if status_filter:
        query = query.where(Survey.status == status_filter)
    
    query = query.order_by(Survey.created_at.desc())
    
    result = await db.execute(query)
    return result.scalars().all()


async def get_survey_by_id(
    db: AsyncSession,
    survey_id: UUID,
    include_questions: bool = False
) -> Optional[Survey]:
    """Получить анкету по ID"""
    query = select(Survey).where(Survey.id == survey_id)
    
    if include_questions:
        query = query.options(
            selectinload(Survey.questions).selectinload(Question.options)
        )
    
    result = await db.execute(query)
    survey = result.scalar_one_or_none()
    
    if survey and include_questions:
        # Сортируем вопросы и варианты по order
        survey.questions.sort(key=lambda q: q.question_order)
        for question in survey.questions:
            question.options.sort(key=lambda o: o.option_order)
    
    return survey


async def check_user_completed_survey(
    db: AsyncSession,
    survey_id: UUID,
    user_id: UUID
) -> bool:
    """Проверить, прошёл ли пользователь анкету"""
    result = await db.execute(
        select(Answer)
        .join(Question)
        .where(Question.survey_id == survey_id)
        .where(Answer.user_id == user_id)
        .limit(1)
    )
    
    return result.scalar_one_or_none() is not None


async def save_survey_answers(
    db: AsyncSession,
    survey_id: UUID,
    user_id: UUID,
    answers: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Сохранить ответы пользователя на анкету
    
    Args:
        db: сессия БД
        survey_id: ID анкеты
        user_id: ID пользователя
        answers: список ответов [{"question_id": UUID, "option_ids": [UUID]}]
    
    Returns:
        {"error": 0, "message": "Success"} или {"error": код, "message": "Описание ошибки"}
    """
    try:
        # Проверяем существование анкеты и загружаем вопросы
        survey = await get_survey_by_id(db, survey_id, include_questions=True)
        
        if not survey:
            return {"error": -1, "message": f"Survey with id {survey_id} not found"}
        
        if survey.status != "active":
            return {"error": -2, "message": f"Survey is not active (status: {survey.status})"}
        
        # Проверяем, что пользователь ещё не проходил анкету
        if await check_user_completed_survey(db, survey_id, user_id):
            return {"error": -3, "message": "You have already completed this survey"}
        
        # Создаём словарь вопросов для быстрого доступа
        questions_dict = {q.id: q for q in survey.questions}
        
        # Валидация и сохранение ответов
        for answer in answers:
            question_id = answer["question_id"]
            option_ids = answer["option_ids"]
            
            question = questions_dict.get(question_id)
            
            if not question:
                return {
                    "error": -4,
                    "message": f"Question {question_id} not found in survey"
                }
            
            # Проверяем множественный выбор
            if len(option_ids) > 1 and not question.allow_multiple_answers:
                return {
                    "error": -5,
                    "message": f"Question {question_id} does not allow multiple answers"
                }
            
            # Проверяем, что все опции принадлежат этому вопросу
            valid_option_ids = {opt.id for opt in question.options}
            for option_id in option_ids:
                if option_id not in valid_option_ids:
                    return {
                        "error": -6,
                        "message": f"Option {option_id} does not belong to question {question_id}"
                    }
            
            # Сохраняем ответы
            for option_id in option_ids:
                db_answer = Answer(
                    question_id=question_id,
                    option_id=option_id,
                    user_id=user_id
                )
                db.add(db_answer)
        
        # Увеличиваем счётчик прошедших анкету
        survey.responses_count += 1
        
        await db.commit()
        
        return {"error": 0, "message": "Survey completed successfully"}
    
    except Exception as e:
        await db.rollback()
        return {"error": -99, "message": f"Database error: {str(e)}"}


async def get_survey_results(
    db: AsyncSession,
    survey_id: UUID
) -> Optional[Dict[str, Any]]:
    """
    Получить результаты анкеты
    
    Returns:
        {
            "survey_id": UUID,
            "survey_title": str,
            "total_responses": int,
            "questions": [
                {
                    "question_id": UUID,
                    "question_text": str,
                    "total_answers": int,
                    "options": [
                        {
                            "option_id": UUID,
                            "option_text": str,
                            "votes_count": int,
                            "percentage": float
                        }
                    ]
                }
            ]
        }
    """
    # Загружаем анкету с вопросами и опциями
    survey = await get_survey_by_id(db, survey_id, include_questions=True)
    
    if not survey:
        return None
    
    # Собираем результаты по каждому вопросу
    questions_results = []
    
    for question in sorted(survey.questions, key=lambda q: q.question_order):
        # Подсчитываем голоса по каждой опции
        option_results = []
        total_answers = 0
        
        for option in sorted(question.options, key=lambda o: o.option_order):
            # Считаем количество ответов для этой опции
            votes_result = await db.execute(
                select(func.count(Answer.id))
                .where(Answer.option_id == option.id)
            )
            votes_count = votes_result.scalar()
            total_answers += votes_count
            
            option_results.append({
                "option_id": str(option.id),
                "option_text": option.option_text,
                "votes_count": votes_count,
                "percentage": 0.0  # Посчитаем позже
            })
        
        # Вычисляем проценты
        if total_answers > 0:
            for opt_result in option_results:
                opt_result["percentage"] = round(
                    (opt_result["votes_count"] / total_answers) * 100, 2
                )
        
        questions_results.append({
            "question_id": str(question.id),
            "question_text": question.question_text,
            "total_answers": total_answers,
            "options": option_results
        })
    
    return {
        "survey_id": str(survey.id),
        "survey_title": survey.title,
        "total_responses": survey.responses_count,
        "questions": questions_results
    }

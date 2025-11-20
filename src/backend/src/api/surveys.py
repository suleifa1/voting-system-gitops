from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID
from datetime import datetime

from src.database.connection import get_db
from src.database.models import (
    get_all_surveys,
    get_survey_by_id,
    check_user_completed_survey,
    save_survey_answers,
    get_survey_results as db_get_survey_results
)
from src.schemas.survey import (
    SurveyListResponse,
    SurveyFullResponse,
    SurveyStartResponse,
    SurveyAnswersSubmit,
    SurveyCompleteResponse,
    SurveyResults
)
from src.api.auth import get_current_user
from src.models.user import User

router = APIRouter(prefix="/surveys", tags=["surveys"])


@router.get("/", response_model=List[SurveyListResponse])
async def get_surveys_list(
    status_filter: str = None,
    db: AsyncSession = Depends(get_db)
):

    surveys = await get_all_surveys(db, status_filter)
    return surveys


@router.get("/{survey_id}", response_model=SurveyFullResponse)
async def get_survey_detail(
    survey_id: UUID,
    db: AsyncSession = Depends(get_db)
):
 
    survey = await get_survey_by_id(db, survey_id, include_questions=True)
    
    if not survey:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Survey with id {survey_id} not found"
        )
    
    return survey


@router.post("/{survey_id}/start", response_model=SurveyStartResponse)
async def start_survey(
    survey_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):

    survey = await get_survey_by_id(db, survey_id)
    
    if not survey:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Survey with id {survey_id} not found"
        )
    
    if survey.status != "active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Survey is not active (current status: {survey.status})"
        )
    

    if await check_user_completed_survey(db, survey_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already completed this survey"
        )
    
    return SurveyStartResponse(
        survey_id=survey_id,
        message="Survey started successfully",
        started_at=datetime.now()
    )


@router.post("/{survey_id}/answer", response_model=SurveyCompleteResponse)
async def submit_survey_answers(
    survey_id: UUID,
    answers_data: SurveyAnswersSubmit,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):

    if answers_data.survey_id != survey_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Survey ID in path and body do not match"
        )
    
    answers_list = [
        {
            "question_id": answer.question_id,
            "option_ids": answer.option_ids
        }
        for answer in answers_data.answers
    ]
    
    result = await save_survey_answers(db, survey_id, current_user.id, answers_list)
    
    if result["error"] == -1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=result["message"]
        )
    elif result["error"] == -2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"]
        )
    elif result["error"] == -3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"]
        )
    elif result["error"] in [-4, -5, -6]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"]
        )
    elif result["error"] == -99:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result["message"]
        )
    
    return SurveyCompleteResponse(
        survey_id=survey_id,
        message=result["message"],
        completed_at=datetime.now()
    )


@router.get("/{survey_id}/results", response_model=SurveyResults)
async def get_survey_results_endpoint(
    survey_id: UUID,
    db: AsyncSession = Depends(get_db)
):
  
    results = await db_get_survey_results(db, survey_id)
    
    if not results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Survey with id {survey_id} not found"
        )
    
    return results

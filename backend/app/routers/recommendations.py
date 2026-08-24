from fastapi import APIRouter, HTTPException, Query

from app.services.recommendation_service import (
    recommendation_service,
    VALID_METHODS
)
from app.schemas.recommendation import FriendRecommendationResponse
from app.schemas.recommendation import ClubRecommendationResponse
from app.schemas.recommendation import EventRecommendationResponse


router = APIRouter(
    prefix="/api/v1/recommendations",
    tags=["Recommendations"]
)


@router.get("/{student_id}/friends", response_model=FriendRecommendationResponse)
def recommend_friends(
    student_id: str,
    method: str = Query(
        ...,
        enum=VALID_METHODS
    ),
    top_k: int = Query(
        default=10,
        ge=1,
        le=100
    )
):

    try:
        recommendations = (
            recommendation_service.get_friend_recommendations(
                student_id=student_id,
                method=method,
                top_k=top_k
            )
        )

        return {
            "student_id": student_id,
            "method": method,
            "top_k": top_k,
            "recommendations": recommendations
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
@router.get("/{student_id}/clubs", response_model=ClubRecommendationResponse)
def recommend_clubs(student_id: str):

    recommendations = (
        recommendation_service.get_club_recommendations(
            student_id
        )
    )

    return {
        "student_id": student_id,
        "recommendations": recommendations
    }

@router.get("/{student_id}/events", response_model=EventRecommendationResponse)
def recommend_events(student_id: str):

    recommendations = (
        recommendation_service.get_event_recommendations(
            student_id
        )
    )

    return {
        "student_id": student_id,
        "recommendations": recommendations
    }
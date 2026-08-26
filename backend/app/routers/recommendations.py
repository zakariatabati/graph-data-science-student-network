from fastapi import APIRouter, HTTPException, Query

from app.services.recommendation_service import (
    recommendation_service,
    VALID_METHODS,
)

from app.schemas.recommendation import (
    FriendRecommendationResponse,
    ClubRecommendationResponse,
    EventRecommendationResponse,
)


router = APIRouter(
    prefix="/api/v1/recommendations",
    tags=["Recommendations"],
)


@router.get(
    "/{student_id}/friends",
    response_model=FriendRecommendationResponse,
    summary="Get friend recommendations",
    description="""
Returns friend recommendations for a student using a graph-based
recommendation algorithm.

Supported methods:

- `common_neighbors`
- `jaccard`
- `adamic_adar`
- `node2vec`
- `hybrid`
""",
    responses={
        200: {
            "description": "Friend recommendations retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "student_id": "1",
                        "method": "jaccard",
                        "top_k": 10,
                        "recommendations": [
                            {
                                "student_id": "25",
                                "score": 0.72
                            },
                            {
                                "student_id": "38",
                                "score": 0.65
                            }
                        ]
                    }
                }
            },
        },
        400: {
            "description": "Invalid recommendation method",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid recommendation method"
                    }
                }
            },
        },
        404: {
            "description": "Student not found"
        },
        422: {
            "description": "Invalid query parameters"
        },
    },
)
def recommend_friends(
    student_id: str,
    method: str = Query(
        ...,
        description="""
Graph-based recommendation method.

Available methods:

- `common_neighbors`
- `jaccard`
- `adamic_adar`
- `node2vec`
- `hybrid`
""",
        examples=["jaccard"],
    ),
    top_k: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Maximum number of recommendations to return.",
        examples=[10],
    ),
):

    try:
        recommendations = (
            recommendation_service.get_friend_recommendations(
                student_id=student_id,
                method=method,
                top_k=top_k,
            )
        )

        return {
            "student_id": student_id,
            "method": method,
            "top_k": top_k,
            "recommendations": recommendations,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get(
    "/{student_id}/clubs",
    response_model=ClubRecommendationResponse,
    summary="Get club recommendations",
    description="""
Returns club recommendations for a student.

The recommendations are based on the student's friendship network
and the clubs joined by their friends.
""",
    responses={
        200: {
            "description": "Club recommendations retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "student_id": "1",
                        "recommendations": [
                            {
                                "club_id": "club_10",
                                "score": 8
                            }
                        ]
                    }
                }
            },
        },
        404: {
            "description": "Student not found"
        },
    },
)
def recommend_clubs(student_id: str):

    recommendations = (
        recommendation_service.get_club_recommendations(
            student_id
        )
    )

    return {
        "student_id": student_id,
        "recommendations": recommendations,
    }


@router.get(
    "/{student_id}/events",
    response_model=EventRecommendationResponse,
    summary="Get event recommendations",
    description="""
Returns event recommendations for a student.

The recommendations are generated from graph relationships
and student participation information.
""",
    responses={
        200: {
            "description": "Event recommendations retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "student_id": "1",
                        "recommendations": [
                            {
                                "event_id": "event_15",
                                "score": 5
                            }
                        ]
                    }
                }
            },
        },
        404: {
            "description": "Student not found"
        },
    },
)
def recommend_events(student_id: str):

    recommendations = (
        recommendation_service.get_event_recommendations(
            student_id
        )
    )

    return {
        "student_id": student_id,
        "recommendations": recommendations,
    }
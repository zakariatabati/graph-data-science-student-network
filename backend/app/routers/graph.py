from fastapi import APIRouter, HTTPException, Query

from app.services.graph_service import graph_service


router = APIRouter(
    prefix="/api/v1/graph",
    tags=["Graph"],
)


@router.get(
    "/stats",
    summary="Get global graph statistics",
    description="""
Returns global statistics about the student social network graph.

The statistics include:

- Number of students
- Number of friendships
- Number of clubs
- Number of events
""",
    responses={
        200: {
            "description": "Graph statistics retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "student_count": 1500,
                        "friendship_count": 7465,
                        "club_count": 70,
                        "event_count": 300
                    }
                }
            },
        },
        500: {
            "description": "Failed to retrieve graph statistics"
        },
    },
)
def get_graph_stats():

    stats = graph_service.get_graph_stats()

    return stats


@router.get(
    "/centrality",
    summary="Get centrality rankings",
    description="""
Returns students ranked according to a selected graph centrality metric.

Supported metrics:

- `degree`: number of direct connections.
- `pagerank`: importance based on connected nodes.
- `betweenness`: importance based on shortest paths.
- `closeness`: average distance to other nodes.
""",
    responses={
        200: {
            "description": "Centrality ranking retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "metric": "degree",
                        "top_k": 10,
                        "results": [
                            {
                                "student_id": "6",
                                "name": "Student 6",
                                "score": 148.0
                            },
                            {
                                "student_id": "10",
                                "name": "Student 10",
                                "score": 147.0
                            }
                        ]
                    }
                }
            },
        },
        400: {
            "description": "Invalid centrality metric",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid centrality metric"
                    }
                }
            },
        },
        422: {
            "description": "Invalid query parameters"
        },
    },
)
def get_centrality(
    metric: str = Query(
        ...,
        description="""
Centrality metric to calculate.

Available values:

- `degree`
- `pagerank`
- `betweenness`
- `closeness`
""",
        examples=["degree"],
    ),
    top_k: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Number of top ranked students to return.",
        examples=[10],
    ),
):

    try:
        results = graph_service.get_centrality(
            metric=metric,
            top_k=top_k,
        )

        return {
            "metric": metric,
            "top_k": top_k,
            "results": results,
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )
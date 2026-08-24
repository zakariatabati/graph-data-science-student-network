from fastapi import APIRouter, HTTPException, Query

from app.schemas.community import (
    CommunityDetectionRequest,
    CommunityResponse,
    CommunityDetailResponse,
    CommunityComparisonResponse,
)
from app.services.community_service import community_service


router = APIRouter(
    prefix="/api/v1/communities",
    tags=["Communities"],
)


@router.post(
    "/detect",
    response_model=dict,
    summary="Detect communities",
    description="""
Runs a community detection algorithm on the student friendship graph.

Supported algorithms:

- `louvain`
- `leiden`
- `label_propagation`

The detected community identifier is stored on the Student nodes.
""",
    responses={
        200: {
            "description": "Communities detected successfully",
            "content": {
                "application/json": {
                    "example": {
                        "algorithm": "louvain",
                        "result": {
                            "communityCount": 12,
                            "modularity": 0.45
                        }
                    }
                }
            },
        },
        422: {
            "description": "Invalid request body",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "msg": "Invalid algorithm value"
                            }
                        ]
                    }
                }
            },
        },
        500: {
            "description": "Community detection failed"
        },
    },
)
def detect_communities(
    request: CommunityDetectionRequest,
):
    result = community_service.detect_communities(request.algorithm)

    return {
        "algorithm": request.algorithm,
        "result": result,
    }


@router.get(
    "",
    response_model=list[CommunityResponse],
    summary="Get detected communities",
    description="""
Returns all detected communities for the selected community detection algorithm.

Each result contains:

- Community identifier
- Number of students in the community
""",
    responses={
        200: {
            "description": "Communities retrieved successfully",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "community_id": 1,
                            "size": 500
                        },
                        {
                            "community_id": 2,
                            "size": 350
                        }
                    ]
                }
            },
        },
        500: {
            "description": "Failed to retrieve communities"
        },
    },
)
def get_communities(
    algorithm: str = Query(
        default="louvain",
        description="""
Community detection algorithm used to retrieve communities.

Available values:

- `louvain`
- `leiden`
- `label_propagation`
""",
        examples=["louvain"],
    ),
):
    communities = community_service.get_communities(algorithm)

    return [
        {
            "community_id": item["community_id"],
            "size": item["size"],
        }
        for item in communities
    ]


@router.get(
    "/compare",
    response_model=list[CommunityComparisonResponse],
    summary="Compare community detection algorithms",
    description="""
Returns a comparison of the available community detection algorithms.

The comparison contains the evaluation metrics produced by the
community analysis implementation.
""",
    responses={
        200: {
            "description": "Algorithms compared successfully",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "algorithm": "louvain",
                            "community_count": 12,
                            "modularity": 0.45,
                            "execution_time": 0.12
                        },
                        {
                            "algorithm": "leiden",
                            "community_count": 10,
                            "modularity": 0.47,
                            "execution_time": 0.15
                        }
                    ]
                }
            },
        },
        500: {
            "description": "Failed to compare algorithms"
        },
    },
)
def compare_communities():
    return community_service.compare_algorithms()


@router.get(
    "/{community_id}",
    response_model=CommunityDetailResponse,
    summary="Get a community and its students",
    description="""
Returns the students belonging to a specific community.

The community ID depends on the selected community detection algorithm.
""",
    responses={
        200: {
            "description": "Community retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "community_id": 42,
                        "students": [
                            {
                                "student_id": "1",
                                "name": "Student 1"
                            },
                            {
                                "student_id": "7",
                                "name": "Student 7"
                            }
                        ]
                    }
                }
            },
        },
        404: {
            "description": "Community not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Community not found"
                    }
                }
            },
        },
    },
)
def get_community(
    community_id: int,
    algorithm: str = Query(
        default="louvain",
        description="""
Community detection algorithm.

Available values:

- `louvain`
- `leiden`
- `label_propagation`
""",
        examples=["louvain"],
    ),
):
    students = community_service.get_community_by_id(
        community_id,
        algorithm,
    )

    if not students:
        raise HTTPException(
            status_code=404,
            detail="Community not found",
        )

    return {
        "community_id": community_id,
        "students": students,
    }
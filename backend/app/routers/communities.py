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


@router.post("/detect", response_model=dict)
def detect_communities(
    request: CommunityDetectionRequest,
):
    result = community_service.detect_communities(request.algorithm)

    return {
        "algorithm": request.algorithm,
        "result": result,
    }


@router.get("", response_model=list[CommunityResponse])
def get_communities(
    algorithm: str = Query(
        default="louvain",
        enum=[
            "louvain",
            "leiden",
            "label_propagation",
        ],
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


@router.get("/compare", response_model=list[CommunityComparisonResponse])
def compare_communities():
    return community_service.compare_algorithms()


@router.get("/{community_id}", response_model=CommunityDetailResponse)
def get_community(
    community_id: int,
    algorithm: str = Query(
        default="louvain",
        enum=[
            "louvain",
            "leiden",
            "label_propagation",
        ],
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
from fastapi import APIRouter, HTTPException, Query

from app.services.community_service import community_service


router = APIRouter(
    prefix="/api/v1/students",
    tags=["Students"],
)


@router.get("/{student_id}/community")
def get_student_community(
    student_id: str,
    algorithm: str = Query(
        default="louvain",
        enum=[
            "louvain",
            "leiden",
            "label_propagation",
        ],
    ),
):
    result = community_service.get_student_community(
        student_id,
        algorithm,
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Student not found",
        )

    return {
        "algorithm": algorithm,
        **result,
    }
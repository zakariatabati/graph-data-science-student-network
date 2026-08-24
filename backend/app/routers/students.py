from fastapi import APIRouter, HTTPException, Query

from app.services.community_service import community_service
from app.services.student_service import student_service


router = APIRouter(
    prefix="/api/v1/students",
    tags=["Students"],
)


@router.get("")
def get_students(
    limit: int = Query(
        default=100,
        ge=1,
        le=500,
    ),
    skip: int = Query(
        default=0,
        ge=0,
    ),
):
    students = student_service.get_students(
        limit=limit,
        skip=skip,
    )

    return {
        "count": len(students),
        "students": students,
    }


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


@router.get("/{student_id}")
def get_student(
    student_id: str,
):
    student = student_service.get_student_by_id(
        student_id
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found",
        )

    return student
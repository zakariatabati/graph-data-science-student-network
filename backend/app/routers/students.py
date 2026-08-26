from fastapi import APIRouter, HTTPException, Query

from app.services.community_service import community_service
from app.services.student_service import student_service


router = APIRouter(
    prefix="/api/v1/students",
    tags=["Students"],
)


@router.get(
    "",
    summary="Get all students",
    description="""
Returns a paginated list of students.

Use `limit` to control the number of returned students and
`skip` to skip a number of students.
""",
    responses={
        200: {
            "description": "Students retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "count": 2,
                        "students": [
                            {
                                "student_id": "1",
                                "name": "Student 1"
                            },
                            {
                                "student_id": "2",
                                "name": "Student 2"
                            }
                        ]
                    }
                }
            },
        },
        422: {
            "description": "Invalid pagination parameters"
        },
    },
)
def get_students(
    limit: int = Query(
        default=100,
        ge=1,
        le=500,
        description="Maximum number of students to return.",
        examples=[100],
    ),
    skip: int = Query(
        default=0,
        ge=0,
        description="Number of students to skip.",
        examples=[0],
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


@router.get(
    "/{student_id}/community",
    summary="Get a student's community",
    description="""
Returns the community to which a student belongs according to
the selected community detection algorithm.
""",
    responses={
        200: {
            "description": "Student community retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "algorithm": "louvain",
                        "student_id": "1",
                        "community_id": 42
                    }
                }
            },
        },
        404: {
            "description": "Student not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Student not found"
                    }
                }
            },
        },
    },
)
def get_student_community(
    student_id: str,
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


@router.get(
    "/{student_id}",
    summary="Get a student by ID",
    description="Returns detailed information about a specific student.",
    responses={
        200: {
            "description": "Student retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "student_id": "1",
                        "name": "Student 1"
                    }
                }
            },
        },
        404: {
            "description": "Student not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Student not found"
                    }
                }
            },
        },
    },
)
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
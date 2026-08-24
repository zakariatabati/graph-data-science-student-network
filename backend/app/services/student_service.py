from app.repositories.student_repository import student_repository


class StudentService:

    def get_students(
        self,
        limit: int,
        skip: int,
    ):
        return student_repository.get_students(
            limit=limit,
            skip=skip,
        )

    def get_student_by_id(
        self,
        student_id: str,
    ):
        return student_repository.get_student_by_id(
            student_id=student_id,
        )


student_service = StudentService()
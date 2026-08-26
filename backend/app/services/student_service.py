from app.repositories.student_repository import student_repository as neo4j_repository


class StudentService:

    def get_students(
        self,
        limit: int,
        skip: int,
    ):
        return neo4j_repository.get_students(limit, skip)

    def get_student_by_id(
        self,
        student_id: str,
    ):
        return neo4j_repository.get_student_by_id(student_id)


student_service = StudentService()
from app.repositories.neo4j import neo4j_repository


class StudentRepository:

    def get_students(
        self,
        limit: int = 100,
        skip: int = 0,
    ):
        query = """
        MATCH (s:Student)

        RETURN
            s.id AS student_id,
            s.nom AS name,
            s

        ORDER BY s.id
        SKIP $skip
        LIMIT $limit
        """

        with neo4j_repository.driver.session() as session:
            result = session.run(
                query,
                skip=skip,
                limit=limit,
            )

            return [record.data() for record in result]

    def get_student_by_id(
        self,
        student_id: str,
    ):
        query = """
        MATCH (s:Student {id: $student_id})

        RETURN
            s.id AS student_id,
            s.nom AS name,
            s
        """

        with neo4j_repository.driver.session() as session:
            result = session.run(
                query,
                student_id=student_id,
            )

            record = result.single()

            return record.data() if record else None


student_repository = StudentRepository()
from app.repositories.neo4j import neo4j_repository


ALGORITHM_PROPERTIES = {
    "louvain": "louvainCommunity",
    "leiden": "leidenCommunity",
    "label_propagation": "labelPropagationCommunity",
}


class CommunityRepository:

    def detect_communities(self, algorithm: str):
        queries = {
            "louvain": """
                CALL gds.louvain.write(
                    'student-friendship-graph',
                    {
                        writeProperty: 'louvain_community'
                    }
                )
                YIELD communityCount, modularity
                RETURN
                    communityCount,
                    modularity
            """,

            "leiden": """
                CALL gds.leiden.write(
                    'student-friendship-graph',
                    {
                        writeProperty: 'leiden_community'
                    }
                )
                YIELD communityCount, modularity
                RETURN
                    communityCount,
                    modularity
            """,

            "label_propagation": """
                CALL gds.labelPropagation.write(
                    'student-friendship-graph',
                    {
                        writeProperty: 'label_propagation_community'
                    }
                )
                YIELD communityCount
                RETURN communityCount
            """,
        }

        with neo4j_repository.driver.session() as session:
            result = session.run(queries[algorithm])
            return result.single().data()

    def get_communities(self, algorithm: str):
        property_name = ALGORITHM_PROPERTIES[algorithm]

        query = f"""
        MATCH (s:Student)
        WHERE s.{property_name} IS NOT NULL

        RETURN
            s.{property_name} AS community_id,
            count(s) AS size

        ORDER BY size DESC
        """

        with neo4j_repository.driver.session() as session:
            result = session.run(query)

            return [record.data() for record in result]

    def get_community_by_id(
        self,
        community_id: int,
        algorithm: str,
    ):
        property_name = ALGORITHM_PROPERTIES[algorithm]

        query = f"""
        MATCH (s:Student)
        WHERE s.{property_name} = $community_id

        RETURN
            s.id AS student_id,
            s.name AS name
        """

        with neo4j_repository.driver.session() as session:
            result = session.run(
                query,
                community_id=community_id,
            )

            return [record.data() for record in result]

    def get_student_community(
        self,
        student_id: str,
        algorithm: str,
    ):
        property_name = ALGORITHM_PROPERTIES[algorithm]

        query = f"""
        MATCH (s:Student {{id: $student_id}})

        RETURN
            s.id AS student_id,
            s.{property_name} AS community_id
        """

        with neo4j_repository.driver.session() as session:
            result = session.run(
                query,
                student_id=student_id,
            )

            record = result.single()

            return record.data() if record else None


community_repository = CommunityRepository()
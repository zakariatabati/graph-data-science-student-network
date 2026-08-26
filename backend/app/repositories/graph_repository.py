from app.repositories.neo4j import neo4j_repository


CENTRALITY_PROPERTIES = {
    "degree": "degreeCentrality",
    "pagerank": "pageRank",
    "betweenness": "betweennessCentrality",
    "closeness": "closenessCentrality",
}


class GraphRepository:

    def get_graph_stats(self):
        query = """
        MATCH (s:Student)
        WITH count(s) AS student_count

        MATCH ()-[r:EST_AMI_DE]-()
        WITH student_count, count(r) AS friendship_count

        MATCH (c:Club)
        WITH student_count, friendship_count, count(c) AS club_count

        MATCH (e:Event)
        RETURN
            student_count,
            friendship_count,
            club_count,
            count(e) AS event_count
        """

        with neo4j_repository.driver.session() as session:
            result = session.run(query)
            record = result.single()

            return record.data() if record else None

    def get_centrality(self, metric: str, top_k: int = 10):
        property_name = CENTRALITY_PROPERTIES[metric]

        query = f"""
        MATCH (s:Student)
        WHERE s.{property_name} IS NOT NULL

        RETURN
            s.id AS student_id,
            s.nom AS name,
            s.{property_name} AS score

        ORDER BY score DESC
        LIMIT $top_k
        """

        with neo4j_repository.driver.session() as session:
            result = session.run(
                query,
                top_k=top_k,
            )

            return [record.data() for record in result]


graph_repository = GraphRepository()
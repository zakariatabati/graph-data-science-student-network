from app.repositories.neo4j import neo4j_repository
from app.core.recommendation_algos.common_neighbors import compute_common_neighbors
from app.core.recommendation_algos.jaccard import compute_jaccard
from app.core.recommendation_algos.adamic_adar import compute_adamic_adar
from app.core.recommendation_algos.node2vec import compute_node2vec
from app.core.recommendation_algos.hybrid import compute_hybrid



ALGORITHM_MAP = {
    "common_neighbors": compute_common_neighbors,
    "jaccard":          compute_jaccard,
    "adamic_adar":      compute_adamic_adar,
    "node2vec":         compute_node2vec,
    "hybrid":           compute_hybrid
}


class RecommendationRepository:

    def get_friend_recommendations(self, student_id: str, method: str, top_k: int):
        algorithm = ALGORITHM_MAP[method]
        return algorithm(student_id, top_k)

    def get_club_recommendations(self, student_id: str):
        query = """
        MATCH (s:Student {id: $student_id})
        MATCH (club:Club)
        WHERE NOT (s)-[:MEMBRE_DE]->(club)
        OPTIONAL MATCH (s)-[:EST_AMI_DE]-(friend)-[:MEMBRE_DE]->(club)
        WITH club, count(friend) AS friend_count
        ORDER BY friend_count DESC
        RETURN club.id AS club_id, club.nom AS name
        LIMIT 10
        """
        with neo4j_repository.driver.session() as session:
            result = session.run(query, student_id=student_id)
            return [record.data() for record in result]

    def get_event_recommendations(self, student_id: str):
        query = """
        MATCH (s:Student {id: $student_id})
        MATCH (event:Event)
        WHERE NOT (s)-[:A_PARTICIPE_A]->(event)
        OPTIONAL MATCH (s)-[:EST_AMI_DE]-(friend)-[:A_PARTICIPE_A]->(event)
        WITH event, count(friend) AS friend_count
        ORDER BY friend_count DESC
        RETURN event.id AS event_id, event.nom AS name
        LIMIT 10
        """
        with neo4j_repository.driver.session() as session:
            result = session.run(query, student_id=student_id)
            return [record.data() for record in result]


recommendation_repository = RecommendationRepository()
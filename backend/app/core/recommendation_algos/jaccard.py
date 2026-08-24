from app.repositories.neo4j import neo4j_repository


def compute_jaccard(student_id: str, top_k: int):
    query = """
    MATCH (s:Student {id: $student_id})-[:EST_AMI_DE]-(common)-[:EST_AMI_DE]-(candidate:Student)
    WHERE candidate <> s
      AND NOT (s)-[:EST_AMI_DE]-(candidate)

    WITH s, candidate, count(common) AS common_count

    MATCH (s)-[:EST_AMI_DE]-(sNeighbor)
    WITH s, candidate, common_count, count(DISTINCT sNeighbor) AS s_degree

    MATCH (candidate)-[:EST_AMI_DE]-(cNeighbor)
    WITH candidate, common_count, s_degree, count(DISTINCT cNeighbor) AS c_degree

    WITH candidate,
         toFloat(common_count) / (s_degree + c_degree - common_count) AS score

    RETURN candidate.id AS student_id, round(score, 4) AS score, candidate.nom AS name
    ORDER BY score DESC
    LIMIT $top_k
    """
    with neo4j_repository.driver.session() as session:
        result = session.run(query, student_id=student_id, top_k=top_k)
        return [record.data() for record in result]
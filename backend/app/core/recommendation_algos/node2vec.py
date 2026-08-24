from app.repositories.neo4j import neo4j_repository


def compute_node2vec(student_id: str, top_k: int):
    """
    Uses Node2Vec embeddings already stored in Neo4j by gds.node2vec.write.
    Computes cosine similarity between the target student and all candidates
    using the embedding vectors stored as node properties.
    """
    query = """
    MATCH (s:Student {id: $student_id})
    WHERE s.embedding IS NOT NULL

    MATCH (candidate:Student)
    WHERE candidate <> s
      AND NOT (s)-[:EST_AMI_DE]-(candidate)
      AND candidate.embedding IS NOT NULL

    WITH s, candidate,
         gds.similarity.cosine(s.embedding, candidate.embedding) AS score

    RETURN candidate.id AS student_id, round(score, 4) AS score, candidate.nom AS name
    ORDER BY score DESC
    LIMIT $top_k
    """
    with neo4j_repository.driver.session() as session:
        result = session.run(query, student_id=student_id, top_k=top_k)
        return [record.data() for record in result]
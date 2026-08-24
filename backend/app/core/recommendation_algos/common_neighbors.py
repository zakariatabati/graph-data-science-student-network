from app.repositories.neo4j import neo4j_repository


def compute_common_neighbors(student_id: str, top_k: int):
    query = """
    MATCH (s:Student {id: $student_id})-[:EST_AMI_DE]-(common)-[:EST_AMI_DE]-(candidate:Student)
    WHERE candidate <> s
      AND NOT (s)-[:EST_AMI_DE]-(candidate)
    RETURN candidate.id AS student_id,
           count(common) AS score,
           candidate.nom AS name
    ORDER BY score DESC
    LIMIT $top_k
    """
    with neo4j_repository.driver.session() as session:
        result = session.run(query, student_id=student_id, top_k=top_k)
        rows = [record.data() for record in result]

    if not rows:
        return []

    max_score = max(r["score"] for r in rows) or 1
    return [
        {"student_id": r["student_id"], "score": round(r["score"] / max_score, 4), "student_name": r["name"]}
        for r in rows
    ]
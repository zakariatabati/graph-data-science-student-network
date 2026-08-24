from app.core.recommendation_algos.jaccard import compute_jaccard
from app.core.recommendation_algos.adamic_adar import compute_adamic_adar
from app.core.recommendation_algos.node2vec import compute_node2vec


ALPHA = 0.3   # Jaccard weight
BETA  = 0.3   # Adamic-Adar weight
GAMMA = 0.4   # Node2Vec weight


def compute_hybrid(student_id: str, top_k: int):
    """
    Combines Jaccard + Adamic-Adar + Node2Vec scores using weighted sum.
    All three methods return scores normalized to [0.0, 1.0].
    """
    fetch_k = top_k * 3

    jaccard_results = compute_jaccard(student_id, fetch_k)
    adamic_results = compute_adamic_adar(student_id, fetch_k)
    node2vec_results = compute_node2vec(student_id, fetch_k)

    jaccard_scores = {r["student_id"]: r["score"] for r in jaccard_results}
    adamic_scores = {r["student_id"]: r["score"] for r in adamic_results}
    node2vec_scores = {r["student_id"]: r["score"] for r in node2vec_results}

    name_map = {}
    for result in jaccard_results + adamic_results + node2vec_results:
        student_id_key = result.get("student_id")
        if student_id_key:
            name_map[student_id_key] = (
                result.get("student_name")
                or result.get("name")
                or ""
            )

    all_candidates = set(jaccard_scores) | set(adamic_scores) | set(node2vec_scores)

    combined = []
    for candidate_id in all_candidates:
        score = (
            ALPHA * jaccard_scores.get(candidate_id, 0.0)
            + BETA * adamic_scores.get(candidate_id, 0.0)
            + GAMMA * node2vec_scores.get(candidate_id, 0.0)
        )

        combined.append({
            "student_id": candidate_id,
            "score": round(score, 4),
            "student_name": name_map.get(candidate_id, "")
        })

    combined.sort(key=lambda x: x["score"], reverse=True)
    return combined[:top_k]
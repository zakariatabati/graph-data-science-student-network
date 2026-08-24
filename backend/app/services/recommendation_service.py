from app.repositories.recommendation_repository import (
    recommendation_repository
)


VALID_METHODS = [
    "common_neighbors",
    "jaccard",
    "adamic_adar",
    "node2vec",
    "hybrid"
]


class RecommendationService:

    def get_friend_recommendations(
        self,
        student_id: str,
        method: str,
        top_k: int
    ):

        if method not in VALID_METHODS:
            raise ValueError(
                f"Invalid method: {method}"
            )

        return recommendation_repository.get_friend_recommendations(
            student_id=student_id,
            method=method,
            top_k=top_k
        )
    def get_club_recommendations(
    self,
    student_id: str
    ):
        return recommendation_repository.get_club_recommendations(
            student_id=student_id
        )
    def get_event_recommendations(
    self,
    student_id: str
    ):
     return recommendation_repository.get_event_recommendations(
         student_id=student_id
        )

recommendation_service = RecommendationService()
from app.repositories.community_repository import (
    community_repository,
    ALGORITHM_PROPERTIES,
)


class CommunityService:

    def detect_communities(self, algorithm: str):
        return community_repository.detect_communities(algorithm)

    def get_communities(self, algorithm: str):
        return community_repository.get_communities(algorithm)

    def get_community_by_id(
        self,
        community_id: int,
        algorithm: str,
    ):
        return community_repository.get_community_by_id(
            community_id,
            algorithm,
        )

    def get_student_community(
        self,
        student_id: str,
        algorithm: str,
    ):
        return community_repository.get_student_community(
            student_id,
            algorithm,
        )

    def compare_algorithms(self):
        comparison = []

        for algorithm in ALGORITHM_PROPERTIES:
            communities = self.get_communities(algorithm)

            comparison.append({
                "algorithm": algorithm,
                "community_count": len(communities),
            })

        return comparison


community_service = CommunityService()
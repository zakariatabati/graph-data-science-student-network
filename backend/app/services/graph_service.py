from app.repositories.graph_repository import (
    graph_repository,
    CENTRALITY_PROPERTIES,
)


class GraphService:

    def get_graph_stats(self):
        return graph_repository.get_graph_stats()

    def get_centrality(
        self,
        metric: str,
        top_k: int,
    ):
        if metric not in CENTRALITY_PROPERTIES:
            raise ValueError(
                f"Invalid centrality metric: {metric}"
            )

        return graph_repository.get_centrality(
            metric=metric,
            top_k=top_k,
        )


graph_service = GraphService()
from unittest.mock import patch

from app.services.graph_service import graph_service


@patch(
    "app.services.graph_service.neo4j_repository.get_graph_stats"
)
def test_get_graph_stats(mock_get_stats):

    expected_stats = {
        "student_count": 1500,
        "friendship_count": 7465,
    }

    mock_get_stats.return_value = expected_stats

    result = graph_service.get_graph_stats()

    assert result == expected_stats


@patch(
    "app.services.graph_service.neo4j_repository.get_centrality"
)
def test_get_degree_centrality(mock_get_centrality):

    expected_result = [
        {
            "student_id": "6",
            "score": 148.0,
        }
    ]

    mock_get_centrality.return_value = expected_result

    result = graph_service.get_centrality(
        metric="degree",
        top_k=10,
    )

    assert result == expected_result
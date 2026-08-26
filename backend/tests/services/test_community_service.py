from unittest.mock import patch

from app.services.community_service import community_service


@patch(
    "app.services.community_service.neo4j_repository.detect_communities"
)
def test_detect_communities(mock_detect):

    expected_result = {
        "community_count": 12,
        "modularity": 0.45,
    }

    mock_detect.return_value = expected_result

    result = community_service.detect_communities(
        "louvain"
    )

    assert result == expected_result


@patch(
    "app.services.community_service.neo4j_repository.get_communities"
)
def test_get_communities(mock_get_communities):

    expected_communities = [
        {
            "community_id": 1,
            "size": 500,
        }
    ]

    mock_get_communities.return_value = expected_communities

    result = community_service.get_communities(
        "louvain"
    )

    assert result == expected_communities
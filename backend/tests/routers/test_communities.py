from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


@patch(
    "app.routers.communities.community_service.detect_communities"
)
def test_detect_communities_success(mock_detect):

    mock_detect.return_value = {
        "community_count": 12,
        "modularity": 0.45,
    }

    response = client.post(
        "/api/v1/communities/detect",
        json={
            "algorithm": "louvain",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["algorithm"] == "louvain"

    mock_detect.assert_called_once_with(
        "louvain"
    )


def test_detect_communities_invalid_algorithm():

    response = client.post(
        "/api/v1/communities/detect",
        json={
            "algorithm": "invalid_algorithm",
        },
    )

    assert response.status_code == 422


@patch(
    "app.routers.communities.community_service.get_communities"
)
def test_get_communities_success(mock_get_communities):

    mock_get_communities.return_value = [
        {
            "community_id": 1,
            "size": 500,
        },
        {
            "community_id": 2,
            "size": 300,
        },
    ]

    response = client.get(
        "/api/v1/communities",
        params={
            "algorithm": "louvain",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["community_id"] == 1
    assert data[0]["size"] == 500


@patch(
    "app.routers.communities.community_service.compare_algorithms"
)
def test_compare_communities(mock_compare):

    mock_compare.return_value = [
        {
            "algorithm": "louvain",
            "community_count": 12,
        },
        {
            "algorithm": "leiden",
            "community_count": 10,
        },
    ]

    response = client.get(
        "/api/v1/communities/compare"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2


@patch(
    "app.routers.communities.community_service.get_community_by_id"
)
def test_get_community_success(mock_get_community):

    mock_get_community.return_value = [
        {
            "student_id": "1",
            "name": "Student 1",
        },
        {
            "student_id": "2",
            "name": "Student 2",
        },
    ]

    response = client.get(
        "/api/v1/communities/1",
        params={
            "algorithm": "louvain",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["community_id"] == 1
    assert len(data["students"]) == 2


@patch(
    "app.routers.communities.community_service.get_community_by_id"
)
def test_get_community_not_found(mock_get_community):

    mock_get_community.return_value = []

    response = client.get(
        "/api/v1/communities/999",
        params={
            "algorithm": "louvain",
        },
    )

    assert response.status_code == 404

    assert response.json()["detail"] == "Community not found"
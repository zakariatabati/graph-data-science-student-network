from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


@patch("app.routers.graph.graph_service.get_graph_stats")
def test_get_graph_stats_success(mock_get_graph_stats):

    mock_get_graph_stats.return_value = {
        "student_count": 1500,
        "friendship_count": 7465,
        "club_count": 70,
        "event_count": 300,
    }

    response = client.get("/api/v1/graph/stats")

    assert response.status_code == 200

    data = response.json()

    assert data["student_count"] == 1500
    assert data["friendship_count"] == 7465

    mock_get_graph_stats.assert_called_once()


@patch("app.routers.graph.graph_service.get_centrality")
def test_get_centrality_success(mock_get_centrality):

    mock_get_centrality.return_value = [
        {
            "student_id": "6",
            "score": 148.0,
        },
        {
            "student_id": "10",
            "score": 147.0,
        },
    ]

    response = client.get(
        "/api/v1/graph/centrality",
        params={
            "metric": "degree",
            "top_k": 10,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["metric"] == "degree"
    assert data["top_k"] == 10
    assert len(data["results"]) == 2

    mock_get_centrality.assert_called_once_with(
        metric="degree",
        top_k=10,
    )


def test_get_centrality_missing_metric():

    response = client.get(
        "/api/v1/graph/centrality"
    )

    assert response.status_code == 422


def test_get_centrality_invalid_top_k():

    response = client.get(
        "/api/v1/graph/centrality",
        params={
            "metric": "degree",
            "top_k": 0,
        },
    )

    assert response.status_code == 422


@patch("app.routers.graph.graph_service.get_centrality")
def test_get_centrality_service_error(mock_get_centrality):

    mock_get_centrality.side_effect = ValueError(
        "Invalid metric"
    )

    response = client.get(
        "/api/v1/graph/centrality",
        params={
            "metric": "invalid",
        },
    )

    assert response.status_code == 400

    data = response.json()

    assert data["detail"] == "Invalid metric"
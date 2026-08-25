from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


@patch(
    "app.routers.recommendations.recommendation_service.get_friend_recommendations"
)
def test_recommend_friends_success(mock_recommend):

    mock_recommend.return_value = [
        {
            "student_id": "25",
            "score": 0.72,
        },
        {
            "student_id": "38",
            "score": 0.65,
        },
    ]

    response = client.get(
        "/api/v1/recommendations/1/friends",
        params={
            "method": "jaccard",
            "top_k": 10,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["student_id"] == "1"
    assert data["method"] == "jaccard"
    assert len(data["recommendations"]) == 2


def test_recommend_friends_missing_method():

    response = client.get(
        "/api/v1/recommendations/1/friends"
    )

    assert response.status_code == 422


@patch(
    "app.routers.recommendations.recommendation_service.get_friend_recommendations"
)
def test_recommend_friends_invalid_method(mock_recommend):

    mock_recommend.side_effect = ValueError(
        "Invalid recommendation method"
    )

    response = client.get(
        "/api/v1/recommendations/1/friends",
        params={
            "method": "invalid",
        },
    )

    assert response.status_code == 400


@patch(
    "app.routers.recommendations.recommendation_service.get_club_recommendations"
)
def test_recommend_clubs_success(mock_recommend):

    mock_recommend.return_value = [
        {
            "club_id": "club_1",
            "score": 5,
        }
    ]

    response = client.get(
        "/api/v1/recommendations/1/clubs"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["student_id"] == "1"
    assert len(data["recommendations"]) == 1


@patch(
    "app.routers.recommendations.recommendation_service.get_event_recommendations"
)
def test_recommend_events_success(mock_recommend):

    mock_recommend.return_value = [
        {
            "event_id": "event_1",
            "score": 3,
        }
    ]

    response = client.get(
        "/api/v1/recommendations/1/events"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["student_id"] == "1"
    assert len(data["recommendations"]) == 1
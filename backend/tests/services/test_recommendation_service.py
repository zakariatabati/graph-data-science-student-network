from unittest.mock import patch

from app.services.recommendation_service import (
    recommendation_service,
)


@patch(
    "app.services.recommendation_service.neo4j_repository.get_friend_recommendations"
)
def test_friend_recommendations(mock_recommend):

    expected_recommendations = [
        {
            "student_id": "25",
            "score": 0.72,
        }
    ]

    mock_recommend.return_value = expected_recommendations

    result = recommendation_service.get_friend_recommendations(
        student_id="1",
        method="jaccard",
        top_k=10,
    )

    assert result == expected_recommendations


def test_invalid_recommendation_method():

    import pytest

    with pytest.raises(ValueError):
        recommendation_service.get_friend_recommendations(
            student_id="1",
            method="invalid_method",
            top_k=10,
        )
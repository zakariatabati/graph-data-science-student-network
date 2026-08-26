from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


@patch(
    "app.routers.students.student_service.get_students"
)
def test_get_students_success(mock_get_students):

    mock_get_students.return_value = [
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
        "/api/v1/students",
        params={
            "limit": 100,
            "skip": 0,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["count"] == 2
    assert len(data["students"]) == 2


@patch(
    "app.routers.students.student_service.get_student_by_id"
)
def test_get_student_success(mock_get_student):

    mock_get_student.return_value = {
        "student_id": "1",
        "name": "Student 1",
    }

    response = client.get(
        "/api/v1/students/1"
    )

    assert response.status_code == 200

    assert response.json()["student_id"] == "1"


@patch(
    "app.routers.students.student_service.get_student_by_id"
)
def test_get_student_not_found(mock_get_student):

    mock_get_student.return_value = None

    response = client.get(
        "/api/v1/students/999"
    )

    assert response.status_code == 404

    assert response.json()["detail"] == "Student not found"


@patch(
    "app.routers.students.community_service.get_student_community"
)
def test_get_student_community_success(
    mock_get_community
):

    mock_get_community.return_value = {
        "student_id": "1",
        "community_id": 42,
    }

    response = client.get(
        "/api/v1/students/1/community",
        params={
            "algorithm": "louvain",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["algorithm"] == "louvain"
    assert data["community_id"] == 42


@patch(
    "app.routers.students.community_service.get_student_community"
)
def test_get_student_community_not_found(
    mock_get_community
):

    mock_get_community.return_value = None

    response = client.get(
        "/api/v1/students/999/community"
    )

    assert response.status_code == 404
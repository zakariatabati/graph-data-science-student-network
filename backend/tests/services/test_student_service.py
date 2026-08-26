from unittest.mock import patch

from app.services.student_service import student_service


@patch(
    "app.services.student_service.neo4j_repository.get_students"
)
def test_get_students(mock_get_students):

    expected_students = [
        {
            "student_id": "1",
            "name": "Student 1",
        },
        {
            "student_id": "2",
            "name": "Student 2",
        },
    ]

    mock_get_students.return_value = expected_students

    result = student_service.get_students(
        limit=100,
        skip=0,
    )

    assert result == expected_students

    mock_get_students.assert_called_once_with(
        100,
        0,
    )
@patch(
    "app.services.student_service.neo4j_repository.get_student_by_id"
)
def test_get_student_by_id(mock_get_student):

    expected_student = {
        "student_id": "1",
        "name": "Student 1",
    }

    mock_get_student.return_value = expected_student

    result = student_service.get_student_by_id("1")

    assert result == expected_student

    mock_get_student.assert_called_once_with("1")
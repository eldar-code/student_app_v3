from unittest.mock import patch, Mock

import pytest

from app.service import ServiceAppLogicError as ServiceError
from app import service
from app.db import DbNotFoundError as DBError


# {'id': 1, 'name': 'John Doe', 'age': 20}
@patch("app.service.db.get_student")
def test_get_student_positive(mock_get_student: Mock):
    # AAA
    # Arrange - set up the mock object
    mock_get_student.return_value = {'id': 1, 'name': 'Mock Student'}
    # Act - use the mock
    result = service.get_student(1)
    # Assert
    assert result == {'id': 1, 'name': 'Mock Student'}
    # Validation - make sure we actually used the mock
    mock_get_student.assert_called_once_with(1)


@patch("app.service.db.get_student")
def test_get_student_negative(mock_get_student: Mock):
    # arrange
    mock_get_student.side_effect = KeyError("not found: 1")
    # act, assert
    with pytest.raises(KeyError):
        service.get_student(111)
    # Validation - make sure we actually used the mock
    mock_get_student.assert_called_once_with(111)


@patch("app.service.db.add_student")
@pytest.mark.parametrize(
    "student",
    [
        pytest.param({'name': 'Dan', 'age': 35}, id="normal_values"),
        pytest.param({'name': 'Da', 'age': 18}, id="min_values"),
        pytest.param({'name': 'Long John Silver', 'age': 120}, id="max_values"),
    ]
)
def test_add_student_positive(mock_add_student: Mock, student):
    # arrange
    mock_add_student.return_value = {'name': student.get("name"), 'age': student.get("age"), 'id': 101}

    # act
    result = service.add_student(student)
    # assert
    assert result["id"] == 101
    assert result["name"] == student.get("name")
    assert result["age"] == student.get("age")

    # validate
    mock_add_student.assert_called_once()


@patch("app.service.db.add_student")
def test_add_student_too_young(self, mock_add_student: Mock):
    mock_add_student.side_effect = ServiceError("add student failed - too young")
    students = (
        {'name': 'Mock Student', 'age': 17, 'id': 101},
        {'name': 'Mock Student', 'age': 0, 'id': 101},
        {'name': 'Mock Student', 'age': -5, 'id': 101}
    )
    for student in students:
        self.assertRaises(ServiceError, service.add_student, student)
    mock_add_student.assert_not_called()


@patch("app.service.db.add_student")
def test_add_student_too_old(self, mock_add_student: Mock):
    mock_add_student.side_effect = ServiceError("add student failed - too old")
    self.assertRaises(ServiceError, service.add_student, {'name': 'Mock Student', 'age': 121, 'id': 101})
    self.assertRaises(ServiceError, service.add_student, {'name': 'Mock Student', 'age': 130, 'id': 101})
    mock_add_student.assert_not_called()


@patch("app.service.db.add_student")
def test_add_student_name_illegal(self, mock_add_student: Mock):
    mock_add_student.side_effect = ServiceError("add student failed on name")
    self.assertRaises(ServiceError, service.add_student, {'name': '', 'age': 20, 'id': 101})
    self.assertRaises(ServiceError, service.add_student, {'name': None, 'age': 20, 'id': 101})
    mock_add_student.assert_not_called()


@patch("app.service.db.get_students")
def test_get_students_positive(self, mock_get_students: Mock):
    expected_data = [
        {"id": 1, "name": "Mock Student"},
        {"id": 2, "name": "Mock Student"}, ]
    mock_get_students.return_value = expected_data
    result = service.get_students()
    self.assertEqual(2, len(result))
    self.assertEqual(expected_data, result)
    mock_get_students.assert_called_once()


@patch("app.service.db.get_students")
def test_get_students_negative(self, mock_get_students: Mock):
    mock_get_students.side_effect = DBError("Database error")
    self.assertRaises(DBError, service.get_students)
    with self.assertRaises(DBError) as context:
        service.get_students()
    self.assertEqual("Database error", str(context.exception))
    self.assertEqual(2, mock_get_students.call_count)


@patch("app.service.db.update_student")
def test_edit_student_positive(self, mock_edit_student: Mock):
    mock_edit_student.return_value = {'name': 'XYZ', 'age': 26, 'id': 101}

    students = [
        {'name': 'AAA', 'age': 18, 'id': 101},
        {'name': 'Dani', 'age': 30, 'id': 101},
        {'name': 'Yosi', 'age': 120, 'id': 101}]

    for student in students:
        # act
        result = service.update_student(student)
        # assert
        self.assertEqual({'name': 'XYZ', 'age': 26, 'id': 101}, result)

    self.assertEqual(3, mock_edit_student.call_count)


@patch("app.service.db.update_student")
def test_update_student_negative(self, mock_update_student: Mock):
    # Arrange
    mock_update_student.side_effect = ServiceError("Illegal student values!")

    students = (
        {'name': '', 'age': 18, 'id': 101},
        {'name': '', 'age': 50, 'id': 101},
        {'name': '', 'age': 120, 'id': 101},
        {'name': None, 'age': 18, 'id': 101},
        {'name': None, 'age': 50, 'id': 101},
        {'name': None, 'age': 20, 'id': 101},
        {'name': 'AAA', 'age': 17, 'id': 101},
        {'name': 'AAA', 'age': 121, 'id': 101},
    )

    for student in students:
        # act & assert
        with self.assertRaises(ServiceError) as context:
            service.update_student(student)
        msg = str(context.exception)
        self.assertIn(
            msg,
            [
                f'Student age is out of range: {student["age"]}',
                f'Student name is too short: {student["name"]}'
            ]
        )

    # mock call validation
    mock_update_student.assert_not_called()

import pytest

from app.service import add_student, ServiceAppLogicError, get_student
from unittest.mock import patch


# marker for testing the SAQC-1 story in Jira
@pytest.mark.jira_key("SAV-1")
@patch("app.service.db.get_student", return_value={"id": 101, "name": "Eldar", "age": 35})
def test_sav_1_get_student_positive(mock_get_student):
    student = get_student(101)
    assert student.get("id") == 101
    assert student.get("name") == "Eldar"
    assert student.get("age") == 35


@pytest.mark.jira_key("SAV-1")
@patch("app.service.db.add_student", side_effect=ServiceAppLogicError("Student age is out of range"))
def test_sav_1_add_student_underage_fail(mock_add_student):
    invalid_student = {"name": "Eldar", "age": 17}
    with pytest.raises(ServiceAppLogicError) as excinfo:
        add_student(invalid_student)
    assert "Student age is out of range" in str(excinfo.value)

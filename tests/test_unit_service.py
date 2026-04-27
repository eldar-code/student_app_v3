import pytest
from app.service import add_student, ServiceAppLogicError


# @pytest.mark.jira_key("SAQC-1")
def test_saqc_1_add_student_underage_fail():
    invalid_student = {"name": "Eldar", "age": 17}
    with pytest.raises(ServiceAppLogicError) as excinfo:
        add_student(invalid_student)
    assert "Student age is out of range" in str(excinfo.value)


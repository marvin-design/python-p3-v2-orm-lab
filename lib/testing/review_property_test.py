import pytest
from review import Review
from department import Department
from employee import Employee

@pytest.fixture
def employee():
    Department.drop_table()
    Employee.drop_table()
    Review.drop_table()

    Department.create_table()
    Employee.create_table()
    Review.create_table()

    dept = Department.create("Eng", "HQ")
    return Employee.create("Jamie", "Engineer", dept.id)

def test_valid_year(employee):
    r = Review(2023, "Solid performer", employee.id)
    assert r.year == 2023

def test_invalid_year(employee):
    with pytest.raises(ValueError):
        Review(1999, "Too early", employee.id)

def test_valid_summary(employee):
    r = Review(2024, "Good", employee.id)
    assert r.summary == "Good"

def test_invalid_summary(employee):
    with pytest.raises(ValueError):
        Review(2024, "", employee.id)

def test_valid_employee_id(employee):
    r = Review(2025, "Effective", employee.id)
    assert r.employee_id == employee.id

def test_invalid_employee_id():
    with pytest.raises(ValueError):
        Review(2025, "Bad ID", 9999)  # ID that doesn't exist

import pytest
from review import Review
from employee import Employee
from department import Department

@pytest.fixture
def setup():
    Review.drop_table()
    Employee.drop_table()
    Department.drop_table()

    Department.create_table()
    Employee.create_table()
    Review.create_table()

    dept = Department.create("QA", "Building T")
    emp = Employee.create("Alex", "Tester", dept.id)

    return emp

def test_create_and_find_review(setup):
    emp = setup
    review = Review.create(2023, "Outstanding tester", emp.id)

    assert isinstance(review, Review)
    assert review.id is not None

    found = Review.find_by_id(review.id)
    assert found.year == 2023
    assert found.summary == "Outstanding tester"
    assert found.employee_id == emp.id

def test_update_review(setup):
    emp = setup
    review = Review.create(2022, "Good", emp.id)
    review.summary = "Improved performance"
    review.update()

    updated = Review.find_by_id(review.id)
    assert updated.summary == "Improved performance"

def test_delete_review(setup):
    emp = setup
    review = Review.create(2021, "To be deleted", emp.id)
    review.delete()

    assert review.id is None
    assert Review.find_by_id(review.id) is None

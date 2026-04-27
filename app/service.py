# application logic
import app.db as db


class ServiceAppLogicError(Exception): pass
class ServiceNotFoundError(Exception): pass

def validate_student(student):
    if not 18 <= student["age"] <= 120:
        raise ServiceAppLogicError(f'Student age is out of range: {student["age"]}')

    if not student["name"] or len(student["name"]) < 2:
        raise ServiceAppLogicError(f'Student name is too short: {student["name"]}')

def add_student(student):
    """Add a student to the system. student age must be in the range 18 - 120"""
    validate_student(student)
    return db.add_student(student)


def get_students():
    return db.get_students()


def get_student(student_id):
    try:
        return db.get_student(student_id)
    except db.DbNotFoundError as e:
        raise ServiceNotFoundError(str(e))


def update_student(student):
    try:
        validate_student(student)
        return db.update_student(student)
    except db.DbNotFoundError as e:
        raise ServiceNotFoundError(str(e))


def delete_student(student_id):
    try:
        return db.delete_student(student_id)
    except db.DbNotFoundError as e:
        raise ServiceNotFoundError(str(e))

if __name__ == "__main__":
    result = get_student(1)
    print(result)

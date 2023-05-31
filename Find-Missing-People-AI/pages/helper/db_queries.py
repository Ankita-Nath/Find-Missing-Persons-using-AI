import uuid
import json

from .postgres_conn import PostgresConnection
from .data_models import NewCaseDetails, UserSubmission


def save_new_case(new_case_details: NewCaseDetails):
    with PostgresConnection() as conn:
        cursor = conn.cursor()

        query = "insert into submitted_cases(submitted_by, name, father_name, age, mobile, face_encoding, status, case_id, birth_marks, adhaar_card, address, last_seen) values(\
                                           %(submitted_by)s, %(name)s, %(father_name)s, %(age)s, %(mobile)s,\
                                           %(face_encoding)s, %(status)s, %(case_id)s, %(birth_marks)s, %(adhaar_card)s, %(address)s, %(last_seen)s)"

        cursor.execute(
            query,
            {
                "submitted_by": new_case_details.submitted_by,
                "name": new_case_details.name,
                "father_name": new_case_details.fathers_name,
                "age": new_case_details.age,
                "mobile": new_case_details.mobile_number,
                "face_encoding": json.dumps(new_case_details.face_embedding),
                "status": "NF",
                "case_id": new_case_details.id,
                "birth_marks": new_case_details.birth_marks,
                "adhaar_card": new_case_details.adhaar_card,
                "address": new_case_details.address,
                "last_seen": new_case_details.last_seen,
            },
        )

        return {"status": "success"}


def fetch_submitted_cases(submitted_by: str, status: str = "NA") -> tuple[int, list]:
    query = "select case_id, name, age, status, last_seen, mobile, matched_with from submitted_cases where submitted_by=%(submitted_by)s"
    status = {"Not Found": "NF", "Found": "F", "Closed": "C", "All": "All"}[status]
    if status != "All":
        query = query + " and status=%(status)s"

    with PostgresConnection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, {"submitted_by": submitted_by, "status": status})

        count = cursor.rowcount
        cases = cursor.fetchall()
        return count, cases


def get_not_confirmed_cases(submitted_by: str):
    query = f"select * from submitted_cases where submitted_by='{submitted_by}' and status='NF'"
    with PostgresConnection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()


def get_last_seen_areas(submitted_by: str):
    query = f"select last_seen from submitted_cases where submitted_by='{submitted_by}'"
    with PostgresConnection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()


def get_training_data(submitted_by: str):
    query = "select case_id, face_encoding from submitted_cases where submitted_by='{}'".format(
        submitted_by
    )
    query = query + "and status='NF'"
    with PostgresConnection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()


def get_usr_submission():
    query = f"select id, face_encoding from user_submissions"
    with PostgresConnection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()


def make_user_submission(user_submission: UserSubmission):
    query = "insert into user_submissions(id, submitted_by, face_encoding,\
              location, mobile, status, birth_marks) values(%(id)s, %(name)s, %(face_encoding)s,\
              %(address)s, %(mobile)s, %(status)s, %(birth_marks)s)"
    print("hey " ,user_submission.birth_marks)
    with PostgresConnection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            query,
            {
                "id": str(uuid.uuid4()),
                "name": user_submission.name,
                "face_encoding": json.dumps(user_submission.face_encoding),
                "address": user_submission.address,
                "mobile": user_submission.mobile,
                "status": "NR",
                "birth_marks": user_submission.birth_marks
            },
        )
    return {"status": True}


def user_submission_details(case_id: str):
    query = "select location, submitted_by, mobile, birth_marks from user_submissions where id=%(case_id)s"
    with PostgresConnection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, {"case_id": case_id})
        return cursor.fetchall()


def change_found_status(case_id: str, submitted_by: str):
    query = "update submitted_cases set status='F', matched_with=%(matched_with)s where case_id=%(case_id)s"
    with PostgresConnection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, {"case_id": case_id, 'matched_with': submitted_by})
    return {"status": True}


def get_confirmed_cases(submitted_by: str):
    query = "select name, age, adhaar_card, mobile from submitted_cases where submitted_by=%(submitted_by)s and status=%(status)s"
    with PostgresConnection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, {"submitted_by": submitted_by, "status": "F"})
        return cursor.fetchall()


def get_case_details(case_id: str):
    query = "select name, mobile, age, last_seen, birth_marks from submitted_cases where case_id=%(case_id)s"
    with PostgresConnection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, {"case_id": case_id})
        return cursor.fetchall()

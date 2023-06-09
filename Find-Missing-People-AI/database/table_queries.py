user_submission_table = """
    create table if not exists user_submissions
    (
        id varchar(64) not null
            constraint user_submissions_pk
                primary key,
        submitted_by varchar(64),
        face_encoding jsonb,
        location varchar(64) not null,
        mobile varchar(12),
        status varchar(16),
        birth_marks varchar(512),
        submitted_on timestamp default CURRENT_TIMESTAMP not null
    )"""

submitted_cases_table = """
    create table if not exists submitted_cases
    (
        case_id varchar(64) not null primary key,
        submitted_by varchar(24) not null,
        name varchar(64) not null,
        father_name varchar(64) not null,
        age integer not null,
        mobile varchar(12),
        face_encoding jsonb,
        submitted_on timestamp default CURRENT_TIMESTAMP not null,
        updated_on timestamp default CURRENT_TIMESTAMP not null,
        status varchar(24) not null,
        last_seen varchar(128),
        address varchar(512),
        birth_marks varchar(512),
        adhaar_card varchar(32),
        complainant_name varchar(128),
        complainant_phone varchar(12),
        matched_with varchar(64)
    )"""

users_tables = """
    create table if not exists users
    (
        username varchar(20) not null constraint users_pk primary key,
        password varchar(64) not null,
        role varchar(10) not null
    )"""

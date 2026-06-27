import json
import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

def get_connection():

    database_url = os.getenv("DATABASE_URL")

    if database_url:
        conn = psycopg2.connect(database_url)
    else:

        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
    print('database_conn : ', conn)
    return conn


def initialize_database():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        age INTEGER NOT NULL,
        diagnosis TEXT,
        concerns TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS therapy_plans (
        id SERIAL PRIMARY KEY,
        patient_id INTEGER NOT NULL,
        plan JSONB NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        CONSTRAINT fk_therapy_patient
        FOREIGN KEY (patient_id)
        REFERENCES patients(id)
        ON DELETE CASCADE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id SERIAL PRIMARY KEY,
        patient_id INTEGER NOT NULL,
        report_type VARCHAR(50) NOT NULL,
        report_content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        CONSTRAINT fk_report_patient
        FOREIGN KEY (patient_id)
        REFERENCES patients(id)
        ON DELETE CASCADE
    );
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_patients_name
    ON patients(name);
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_therapy_patient
    ON therapy_plans(patient_id);
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_reports_patient
    ON reports(patient_id);
    """)

    conn.commit()

    cursor.close()
    conn.close()

    print("Database initialized successfully.")
    

def save_patient(patient_info):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO patients (
        name,
        age,
        diagnosis,
        concerns
    )
    VALUES (%s, %s, %s, %s)
    RETURNING id;
    """

    cursor.execute(
        query,
        (
            patient_info["name"],
            patient_info["age"],
            patient_info["diagnosis"],
            ", ".join(patient_info["concerns"])
        )
    )

    patient_id = cursor.fetchone()[0]

    conn.commit()

    cursor.close()
    conn.close()

    return patient_id


def get_patient(patient_id):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        id,
        name,
        age,
        diagnosis,
        concerns
    FROM patients
    WHERE id = %s;
    """

    cursor.execute(
        query,
        (patient_id,)
    )

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if not row:
        return None

    return {
        "id": row[0],
        "name": row[1],
        "age": row[2],
        "diagnosis": row[3],
        "concerns": row[4].split(", ") if row[4] else []
    }


def search_patients(search_text):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        id,
        name,
        age,
        diagnosis
    FROM patients
    WHERE LOWER(name)
    LIKE LOWER(%s)
    ORDER BY name;
    """

    cursor.execute(
        query,
        (
            f"%{search_text}%",
        )
    )

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [
        {
            "id": row[0],
            "name": row[1],
            "age": row[2],
            "diagnosis": row[3]
        }
        for row in rows
    ]

def save_therapy_plan(patient_id, patient_info, therapy_plan):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO therapy_plans (
        patient_id,
        plan
    )
    VALUES (%s, %s)
    RETURNING id;
    """

    cursor.execute(
        query,
        (
            patient_id,
            json.dumps(
                {
                    "patient_info": patient_info,
                    "therapy_plan": therapy_plan
                }
)
        )
    )

    plan_id = cursor.fetchone()[0]

    conn.commit()

    cursor.close()
    conn.close()

    return plan_id


def save_report(
    patient_id: int,
    report_type: str,
    report_content: str
):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO reports (
        patient_id,
        report_type,
        report_content
    )
    VALUES (%s, %s, %s)
    RETURNING id;
    """

    cursor.execute(
        query,
        (
            patient_id,
            report_type,
            report_content
        )
    )

    report_id = cursor.fetchone()[0]

    conn.commit()

    cursor.close()
    conn.close()

    return report_id


def get_patient_plans(patient_id):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        id,
        created_at
    FROM therapy_plans
    WHERE patient_id = %s
    ORDER BY created_at DESC;
    """

    cursor.execute(
        query,
        (patient_id,)
    )

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [
        {
            "id": row[0],
            "created_at": row[1]
        }
        for row in rows
    ]


def get_therapy_plan(plan_id):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT plan
    FROM therapy_plans
    WHERE id = %s;
    """

    cursor.execute(
        query,
        (plan_id,)
    )

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if not row:
        return None

    return row[0]


# Before generating a new plan, update the patient record

def update_patient(
    patient_id: int,
    patient_info
):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE patients
    SET
        name = %s,
        age = %s,
        diagnosis = %s,
        concerns = %s
    WHERE id = %s;
    """

    cursor.execute(
        query,
        (
            patient_info["name"],
            patient_info["age"],
            patient_info["diagnosis"],
            ", ".join(patient_info["concerns"]),
            patient_id
        )
    )

    conn.commit()

    cursor.close()
    conn.close()
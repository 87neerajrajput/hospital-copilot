import json

from tools.db_tools import get_connection


# ==========================================================
# SEARCH PATIENT BY NAME
# ==========================================================

def search_patients(search_text):

    conn = get_connection()

    try:
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
        ORDER BY id DESC;
        """

        cursor.execute(
            query,
            (
                f"%{search_text}%",
            )
        )

        rows = cursor.fetchall()

        return [
            {
                "id": row[0],
                "name": row[1],
                "age": row[2],
                "diagnosis": row[3]
            }
            for row in rows
        ]
    finally:
        cursor.close()
        conn.close()

        

# ==========================================================
# GET PATIENT BY ID
# ==========================================================

def get_patient(patient_id: int):

    print(f"[MCP] get_patient({patient_id})")

    conn = get_connection()

    try:
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

        if not row:
            return None

        return {
            "id": row[0],
            "name": row[1],
            "age": row[2],
            "diagnosis": row[3],
            "concerns": row[4].split(", ") if row[4] else []
        }
    
    finally:
        cursor.close()
        conn.close()



# ==========================================================
# GET ALL THERAPY PLANS
# ==========================================================

def get_patient_plans(patient_id: int):

    conn = get_connection()

    try:
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

        return [
            {
                "id": row[0],
                "created_at": row[1]
            }
            for row in rows
        ]

    finally:

        cursor.close()
        conn.close()


# ==========================================================
# GET THERAPY PLAN
# ==========================================================

def get_therapy_plan(plan_id):

    conn = get_connection()

    try:
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

        if not row:
            return None

        return row[0]
    
    finally:

        cursor.close()
        conn.close()


# ==========================================================
# UPDATE PATIENT
# ==========================================================

def update_patient(
    patient_id: int,
    patient_info: dict,
):

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE patients
            SET
                name = %s,
                age = %s,
                diagnosis = %s,
                concerns = %s
            WHERE id = %s
            """,
            (
                patient_info["name"],
                patient_info["age"],
                patient_info["diagnosis"],
                ", ".join(patient_info["concerns"]),
                patient_id,
            ),
        )

        conn.commit()

        return {
            "success": True,
            "message": "Patient updated successfully."
        }

    except Exception as e:

        conn.rollback()

        return {
            "success": False,
            "message": str(e)
        }

    finally:

        cursor.close()
        conn.close()


# ==========================================================
# SAVE PATIENT
# ==========================================================

def save_patient(patient_info: dict):

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO patients
            (
                name,
                age,
                diagnosis,
                concerns
            )
            VALUES (%s,%s,%s,%s)
            RETURNING id
            """,
            (
                patient_info["name"],
                patient_info["age"],
                patient_info["diagnosis"],
                ", ".join(patient_info["concerns"]),
            ),
        )

        patient_id = cursor.fetchone()[0]

        conn.commit()

        return {
            "success": True,
            "patient_id": patient_id,
            "message": "Patient created successfully."
        }

    except Exception as e:

        conn.rollback()

        return {
            "success": False,
            "message": str(e)
        }

    finally:

        cursor.close()
        conn.close()


# ==========================================================
# SAVE THERAPY PLAN
# ==========================================================

def save_therapy_plan(
    patient_id: int,
    patient_info: dict,
    therapy_plan: dict,
):

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO therapy_plans
            (
                patient_id,
                plan
            )
            VALUES (%s,%s)
            RETURNING id
            """,
            (
                patient_id,
                json.dumps(
                    {
                        "patient_info": patient_info,
                        "therapy_plan": therapy_plan,
                    }
                ),
            ),
        )

        plan_id = cursor.fetchone()[0]

        conn.commit()

        return {
            "success": True,
            "plan_id": plan_id,
            "message": "Therapy plan saved successfully."
        }

    except Exception as e:

        conn.rollback()

        return {
            "success": False,
            "message": str(e)
        }

    finally:

        cursor.close()
        conn.close()


# ==========================================================
# SAVE REPORT
# ==========================================================

def save_report(
    patient_id: int,
    report_type: str,
    report_content: str,
):

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO reports
            (
                patient_id,
                report_type,
                report_content
            )
            VALUES (%s,%s,%s)
            RETURNING id
            """,
            (
                patient_id,
                report_type,
                report_content,
            ),
        )

        report_id = cursor.fetchone()[0]

        conn.commit()

        return {
            "success": True,
            "report_id": report_id,
            "message": "Report saved successfully."
        }

    except Exception as e:

        conn.rollback()

        return {
            "success": False,
            "message": str(e)
        }

    finally:

        cursor.close()
        conn.close()
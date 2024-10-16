from flask import Blueprint, jsonify
import cx_Oracle
import os

sql_api_bp = Blueprint('sql_api_bp', __name__)

username = "admin"
DB_PASSWORD = os.environ.get("DB_PASSWORD")
hostname = os.environ.get("DB_PASSWORD")
service_name = "your_service"

def get_db_connection():
    connection = cx_Oracle.connect(
        user=username,
        password=DB_PASSWORD,
        dsn=f"{hostname}/{service_name}"
    )
    return connection

@sql_api_bp.route('/employees', methods=['GET'])
def get_employees():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM employees")  # Example query
    rows = cursor.fetchall()

    # Process rows into JSON format
    employees = [
        {"employee_id": row[0], "first_name": row[1], "last_name": row[2]}
        for row in rows
    ]

    cursor.close()
    connection.close()

    return jsonify(employees)

@sql_api_bp.route('/employee/<int:emp_id>', methods=['GET'])
def get_employee(emp_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM employees WHERE employee_id = :emp_id", {"emp_id": emp_id})
    row = cursor.fetchone()

    if row:
        employee = {"employee_id": row[0], "first_name": row[1], "last_name": row[2]}
        response = jsonify(employee)
    else:
        response = jsonify({"error": "Employee not found"}), 404

    cursor.close()
    connection.close()

    return response


if __name__ == '__main__':
    sql_api_bp.run(debug=True)

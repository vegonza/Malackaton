from flask import Blueprint, jsonify
from app.api.DBHandler import DBHandler
import os

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

sql_api_bp = Blueprint('sql_api_bp', __name__)

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
DB_ID = os.environ.get("DB_ID")

db_handler = DBHandler(CLIENT_ID, CLIENT_SECRET, DB_ID)

@sql_api_bp.route("/test")
def test_db():
    try:
        response = db_handler.get("test")
    except Exception as exc:
        print("Error while testing db", repr(exc))
        return jsonify({"error": "Error while testing db"}), 500
    
    return response


if __name__ == "__main__":
    response = test_db()
    print("returned:", response)
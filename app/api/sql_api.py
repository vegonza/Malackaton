from flask import Blueprint, jsonify,request
from app.api.DBHandler import DBHandler
import os

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

sql_api_bp = Blueprint('sql_api_bp', __name__)

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
DB_ID = os.environ.get("DB_ADDRESS")
API_NAME = os.environ.get("API_NAME")

db_handler = DBHandler(CLIENT_ID, CLIENT_SECRET, DB_ID, API_NAME)

@sql_api_bp.route("/test")
def test_db():
    try:
        response = db_handler.request("GET", "test")
    except Exception as exc:
        print("Error while testing db", repr(exc))
        return jsonify({"error": "Error while testing db"}), 500
    
    return response

@sql_api_bp.route('/embalses_cords', methods=['POST'])
def embalses_cords():
    items = db_handler.request("GET", "embalses?limit=1000")['items']
    embalses_cords = [{"lat": item['x'], "lng":item['y']} for item in items]
    
    return jsonify({"embalses": embalses_cords})

@sql_api_bp.route('/embalses', methods=['GET'])
def get_embalses():
    try:
        # Recoger filtros opcionales de la solicitud
        comunidad_autonoma = request.args.get("comunidad_autonoma")
        provincia = request.args.get("provincia")
        electrico = request.args.get("electrico")
        agua = request.args.get("agua")

        # Construir el diccionario de filtros
        filters = {}
        if comunidad_autonoma:
            filters["comunidad_autonoma"] = comunidad_autonoma
        if provincia:
            filters["provincia"] = provincia
        if electrico:
            filters["electrico"] = bool(int(electrico))  # Asume que electrico es 0 o 1
        if agua:
            filters["agua"] = agua

        # Solicitar embalses aplicando los filtros
        embalses = db_handler.request("GET", "/embalses", filter=filters)

        # Devolver la respuesta en formato JSON
        return jsonify(embalses), 200

    except Exception as exc:
        print("Error al obtener los embalses:", repr(exc))
        return jsonify({"error": "Error al obtener los embalses"}), 500


if __name__ == "__main__":
    response = test_db()
    print("returned:", response)
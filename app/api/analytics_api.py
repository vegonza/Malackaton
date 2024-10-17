from flask import Flask, jsonify, Blueprint, request
import csv

analytics_api_bp = Blueprint('analytics_api_bp', __name__)

def load_data_id(id):
    data = []
    with open('agua.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['ID'] and int(row['ID']) == id:
                data.append({
                    "FECHA": row["FECHA"],
                    "AGUA_ACTUAL": int(row["AGUA_ACTUAL"]) if row["AGUA_ACTUAL"] else 0
                })
    return data

def load_data():
    data = []
    with open('embalses_combinado.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            item = {
                    "id": int(row["ID"]) if row["ID"] else None,
                    "ambito_nombre": row["AMBITO_NOMBRE"],
                    "embalse_nombre": row["EMBALSE_NOMBRE"],
                    "agua_total": float(row["AGUA_TOTAL"]) if row["AGUA_TOTAL"] else None,
                    "electrico_flag": int(row["ELECTRICO_FLAG"]) if row["ELECTRICO_FLAG"] else None,
                    "codigo": row["CODIGO"],
                    "nombre": row["NOMBRE"],
                    "embalse": row["EMBALSE"],
                    "lat": float(row["X"].replace(',', '.')) if row["X"] else None,
                    "lng": float(row["Y"].replace(',', '.')) if row["Y"] else None,
                    "demarc": row["DEMARC"],
                    "cauce": row["CAUCE"],
                    "google": row["GOOGLE"],
                    "openstreetmap": row["OPENSTREETMAP"],
                    "wikidata": row["WIKIDATA"],
                    "provincia": row["PROVINCIA"],
                    "ccaa": row["CCAA"],
                    "tipo": row["TIPO"],
                    "cota_coron": float(row["COTA_CORON"].replace(',', '.')) if row["COTA_CORON"] else None,
                    "alt_cimien": float(row["ALT_CIMIEN"].replace(',', '.')) if row["ALT_CIMIEN"] else None,
                    "informe_url": row["INFORME"],
                }
            data.append(item)
    return data

@analytics_api_bp.route('/load_data_id', methods=['GET'])
def get_data_id():
    id = request.args.get('id')
    if not id:
        return jsonify({"error": "ID parameter is required"}), 400
    data = load_data_id(int(id))
    return jsonify(data)

@analytics_api_bp.route('/load_data', methods=['GET'])
def get_data():
    data = load_data()
    return jsonify(data)

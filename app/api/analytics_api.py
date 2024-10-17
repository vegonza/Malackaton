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
    with open('listadoUTF8-3.tsv', newline='', encoding='utf-8') as tsvfile:
        reader = csv.DictReader(tsvfile, delimiter='\t')
        for row in reader:
            item = {
                "codigo": row["CODIGO"],
                "nombre": row["NOMBRE"],
                "embalse": row["EMBALSE"],
                "lat": float(row["X"].replace(',', '.')),
                "lng": float(row["Y"].replace(',', '.')),
                "demarc": row["DEMARC"],
                "cauce": row["CAUCE"],
                "provincia": row["PROVINCIA"],
                "ccaa": row["CCAA"],
                "tipo": row["TIPO"],
                "cota_coron": row["COTA_CORON"],
                "alt_cimien": row["ALT_CIMIEN"],
                "informe_url": row["INFORME"]
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

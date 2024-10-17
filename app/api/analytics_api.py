from flask import Flask, jsonify, Blueprint, request
import csv

analytics_api_bp = Blueprint('analytics_api_bp', __name__)

def load_data(id):
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

@analytics_api_bp.route('/load_data', methods=['GET'])
def get_data():
    id = request.args.get('id')
    if not id:
        return jsonify({"error": "ID parameter is required"}), 400
    data = load_data(int(id))
    return jsonify(data)



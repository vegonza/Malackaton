from flask import Flask, request, jsonify, Blueprint
import requests
import os
import fingerprint_pro_server_api_sdk
from datetime import datetime, timedelta

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

bot_detection_api_bp = Blueprint('bot_detection_api_bp', __name__)

# Diccionario en memoria para almacenar los visitantes bloqueados
# Formato: {'visitor_id': 'timestamp_de_desbloqueo'}
blocked_visitors = {}
BLOCK_DURATION = timedelta(minutes=10)

configuration = fingerprint_pro_server_api_sdk.Configuration(
  api_key=os.environ.get("FINGERPRINT_KEY"),
  region="eu"
)
api_client = fingerprint_pro_server_api_sdk.FingerprintApi(configuration)

def is_blocked(visitor_id):
    """Verifica si un visitante está actualmente bloqueado."""
    unblock_time = blocked_visitors.get(visitor_id)
    if unblock_time and datetime.now() < unblock_time:
        return True
    elif unblock_time:
        # Si el tiempo de bloqueo ha expirado, elimina al visitante de la lista
        del blocked_visitors[visitor_id]
    return False

def block_visitor(visitor_id):
    """Bloquea al visitante por el tiempo especificado."""
    blocked_visitors[visitor_id] = datetime.now() + BLOCK_DURATION

def get_visit_history(visitor_id):
    visits = api_client.get_visits(visitor_id, limit=10)
    return visits.visits if visits else []

# Función para verificar si el evento pertenece a un bot o no
def check_event(visit):
    request_id = visit.request_id
    if not request_id:
        return None
    
    # Obtener los detalles del evento para verificar el estado del bot
    event = api_client.get_event(request_id)

    # Acceder al producto `botd` y verificar el atributo `bot.result`
    botd_data = event.products.botd
    if botd_data and hasattr(botd_data, "bot"):
        # Verificar si el resultado es 'bad', indicando un bot detectado
        bot_result = botd_data.bot.result
        return bot_result == "bad"
    
    return False

@bot_detection_api_bp.route('/verify_behavior', methods=['POST'])
def verify_behavior():
    data = request.get_json()
    visitor_id = data.get('visitorId')

    if not visitor_id:
        return jsonify({"error": "Falta el visitorId"}), 400
    
    if is_blocked(visitor_id):
        return jsonify({"error": "Acceso denegado: bot detectado y bloqueado temporalmente"}), 403

    # Obtén el historial de visitas del visitante
    try:
        visit_history = get_visit_history(visitor_id)
    except Exception as e:
        return jsonify({"error": f"Error al obtener historial de visitas: {e}"}), 500

    # Verifica cada visita para detectar eventos de bots
    for visit in visit_history:
        try:
            is_bot = check_event(visit)
            if is_bot:
                block_visitor(visitor_id)
                return jsonify({"message": "Bot detectado y bloqueado temporalmente"}), 403
        except Exception as e:
            return jsonify({"error": f"Error al verificar evento: {e}"}), 500

    return jsonify({"message": "Humano detectado"}), 200

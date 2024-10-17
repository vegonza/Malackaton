import requests

class DBHandler:
    def __init__(self, client_id, client_secret, db_id):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = f"https://{db_id}-dymdb.adb.eu-madrid-1.oraclecloudapps.com/ords/admin/oauth/token"
        self.api_url = f"https://{db_id}-dymdb.adb.eu-madrid-1.oraclecloudapps.com/ords/admin/api/v1/"
        self.token = None
        self.obtener_token()

    def obtener_token(self):
        data = {"grant_type": "client_credentials"}
        response = requests.post(self.token_url, data=data, auth=(self.client_id, self.client_secret))
        
        if response.status_code == 200:
            self.token = response.json().get("access_token")
            print("Token obtenido exitosamente.")
        else:
            raise Exception("Error al obtener el token:", response.status_code)

    def get(self, endpoints):
        url = self.api_url + endpoints
        
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(url, headers=headers)

        # token expired
        if response.status_code == 401:
            print("Token caducado. Obteniendo un nuevo token...")
            self.obtener_token()
            headers["Authorization"] = f"Bearer {self.token}"
            response = requests.get(url, headers=headers)

        return response

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())
    
    # Ejemplo de uso
    client_id = os.environ.get("CLIENT_ID")
    client_secret = os.environ.get("CLIENT_SECRET")
    db_id = os.environ.get("DB_ID")
    
    auth_handler = DBHandler(client_id, client_secret, db_id)

    api_url = "test"
    response = auth_handler.get(api_url)

    if response.status_code == 200:
        print("Conexión exitosa:", response.json())
    else:
        print("Error en la conexión:", response.status_code)
            
import requests
import json

class DBHandler:
    def __init__(self, client_id: str, client_secret: str, db_address: str, api_name: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = f"https://{db_address}.oraclecloudapps.com/ords/admin/oauth/token"
        self.api_url = f"https://{db_address}.oraclecloudapps.com/ords/admin/{api_name}"
        self.session = requests.Session()
        self.token = None
        self._get_token()

    def _get_token(self):
        data = {"grant_type": "client_credentials"}
        response = self.session.post(self.token_url, data=data, auth=(self.client_id, self.client_secret))
        
        if response.status_code == 200:
            self.token = response.json().get("access_token")
            self.session.headers.update({"Authorization": f"Bearer {self.token}"})
        else:
            raise Exception(f"Failed to obtain token: {response.status_code}")

    def _refresh_token_if_needed(self, response: requests.Response) -> bool:
        if response.status_code == 401:
            self._get_token()
            return True
        return False

    def request(self, method: str, endpoint: str, filter:dict={}, **kwargs) -> dict: 
        url = self.api_url + endpoint
        if filter:
            url += f"?q={json.dumps(filter)}"
            
        response = self.session.request(method, url, **kwargs)

        if self._refresh_token_if_needed(response):
            response = self.session.request(method, url, **kwargs)

        if not response.ok:
            raise Exception(f"API Request failed: {response.status_code}")

        
        return response.json()

if __name__ == '__main__':
    import os
    from dotenv import load_dotenv, find_dotenv

    load_dotenv(find_dotenv())

    client_id = os.environ.get("CLIENT_ID")
    client_secret = os.environ.get("CLIENT_SECRET")
    db_id = os.environ.get("DB_ADDRESS")
    api_name = os.environ.get("API_NAME")

    if not all([client_id, client_secret, db_id, api_name]):
        raise EnvironmentError("Missing environment variables for CLIENT_ID, CLIENT_SECRET, or DB_ID")

    db_handler = DBHandler(client_id, client_secret, db_id, api_name)

    try:
        response = db_handler.request("GET", "agua", filter={"id":18})
        print("Success:", response)
    except Exception as exc:
        print("Error:", exc)
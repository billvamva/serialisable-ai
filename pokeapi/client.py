import requests

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, endpoint):
        if ('https' in endpoint ):
            url = endpoint
        else:
           url = self.base_url + endpoint
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for any HTTP error
            return response.json()
        except requests.exceptions.RequestException as e:
            print("Error:", e)
            return None  # Return None or handle the error as needed


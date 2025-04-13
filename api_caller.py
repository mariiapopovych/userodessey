import requests

class APICaller:
    def __init__(self):
        self.data = {}
        self.request_data()
        
    def request_data(self):
        url = 'https://hackathon-api.mlo.sehlat.io/game/start'

        payload = {
            "player_name": "Diversity^2"
        }

        headers = {
            'Content-Type': 'application/json',
            'x-api-key': 'JCxPX6QZXq_weqg49FcbB4zI6vyZz79MtG9Xwd73UyM'
        }

        # Send the POST request
        response = requests.post(url, json=payload, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            
            # Extract relevant fields
            message = data.get('message')
            session_id = data.get('session_id')
            player_id = data.get('player_id')
            client_id = data.get('client_id')
            client_data = data.get('client_data', {})
            passport = client_data.get('passport')
            profile = client_data.get('profile')
            description = client_data.get('description')
            account = client_data.get('account')
            score = data.get('score')
            self.data = {
                "message": message,
                "session_id": session_id,
                "player_id": player_id,
                "client_id": client_id,
                "client_data": {
                    "passport": passport,
                    "profile": profile,
                    "description": description,
                    "account": account
                },
                "score": score
            }

    def get_account(self):
        return self.data.get("client_data").get("account")
        
    def get_passport(self):
        return self.data.get("client_data").get("passport")
    
    def get_profile(self):
        return self.data.get("client_data").get("profile")
    
    def get_description(self):
        return self.data.get("client_data").get("description")

    def send_decision(self, decision="Accept"):
        url = 'https://hackathon-api.mlo.sehlat.io/game/decision'
        headers = {
            "x-api-key": "JCxPX6QZXq_weqg49FcbB4zI6vyZz79MtG9Xwd73UyM"
        }
        payload = {
            "decision": decision,
            "session_id": self.data.get("session_id"),
            "client_id": self.data.get("client_id")
        }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            score = data.get('score')
            status = data.get('status')
            return status, score
        else:
            print(response.json())

if __name__=="__main__":
    caller = APICaller()
    caller.request_data()
    print(caller.send_decision())
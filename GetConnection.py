import datetime
import hashlib
import hmac
import json
import pickle
import time
import sys
import socket
import re
import json

import requests
import urllib3

class GetConnection():
    def __init__(self):
        self.URL_BASE = 'https://mafreebox.freebox.fr/api/v10/'
        self.APP_ID = 'fr.freebox.apf'
        self.APP_NAME = 'autoportforward'
        self.APP_VERSION = '1'
        self.DEVICE_NAME = 'apf'
        self.TOKEN = 'jduARJYIWM27yRSia1VZzdChGMyHEmhuM43y5iPJJmaemoKZHVdHgSpe1TCMXI1o'
        self.TRACK_ID = '6'

        self.session = requests.Session()
        self.session.verify = False
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


    def fancy_print(data):
        print(json.dumps(data, indent=2, separators=(',', ': ')))

    def connexion_post(self, method, data=None, session=None):
        url = self.URL_BASE + method
        if data: data = json.dumps(data)
        return json.loads(session.post(url, data=data).text)

    def connexion_get(self, method, session=None):
        url = self.URL_BASE + method
        return json.loads(session.get(url).text)
    
    def connexion_delete(self, method, session=None):
        url = self.URL_BASE + method
        return json.loads(session.delete(url).text)
    
    def connexion_close(self, session):
        result = self.connexion_post("/login/logout/", session=session)
        if result["success"] != True:
            print("Error while closing session")
    
    
    def register(self):
        global TOKEN, TRACK_ID
        payload = {'app_id': self.APP_ID, 'app_name': self.APP_NAME, 'app_version': self.APP_VERSION, 'device_name': self.DEVICE_NAME}
        content = self.connexion_post('login/authorize/', payload)
        TOKEN = str(content["result"]["app_token"])
        TRACK_ID = str(content["result"]["track_id"])


    def create_session(self):
        global TOKEN
        session = requests.session()
        session.verify = False
        challenge = str(self.connexion_get("login/", session)["result"]["challenge"])
        token_bytes = bytes(self.TOKEN, 'latin-1')
        challenge_bytes = bytes(challenge, 'latin-1')
        password = hmac.new(token_bytes, challenge_bytes, hashlib.sha1).hexdigest()
        data = {
            "app_id": self.APP_ID,
            "app_version": self.APP_VERSION,
            "password": password
        }
        content = self.connexion_post("login/session/", data, session)
        session.headers = {"X-Fbx-App-Auth": content["result"]["session_token"]}
        return session
        
    def get_config(self, file_path):
        config_data = {}

        with open('config/'+file_path, 'r') as file:
            for line in file:
                match = re.match(r'(\w+)=(\S+)', line)
                if match:
                    key, value = match.groups()
                    config_data[key] = value
        return config_data



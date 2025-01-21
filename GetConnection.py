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
import configparser


class GetConnection():
    def __init__(self):
        self.config_path = '/etc/freebox-port-forwarding.conf'

        self.load_config()

        self.session = requests.Session()
        self.session.verify = False
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def load_config(self):
        config = configparser.ConfigParser()
        try:
            config.read(self.config_path)
            self.URL_BASE = config.get('CONFIG', 'URL_FREEBOX')+'/api/v'+config.get('CONFIG', 'API_MAJOR_VERSION')+'/'
            self.APP_ID = config.get('CONFIG', 'APP_ID')
            self.APP_NAME = config.get('CONFIG', 'APP_NAME')
            self.APP_VERSION = config.get('CONFIG', 'APP_VERSION')
            self.DEVICE_NAME = config.get('CONFIG', 'APP_DEVICE_NAME')
            self.TOKEN = config.get('CONFIG', 'APP_TOKEN')
            self.TRACK_ID = config.get('CONFIG', 'TRACK_ID')
            self.API_VERSION = config.get('CONFIG', 'API_VERSION')
            self.API_MAJOR_VERSION = config.get('CONFIG', 'API_MAJOR_VERSION')
        except FileNotFoundError:
            print(f"Configuration file {self.config_path} not found. Using default values.")
        except configparser.Error as e:
            print(f"Error reading configuration file {self.config_path}: {e}. Using default values.")
        except KeyError as e:
            print(f"Missing required configuration key: {e}. Using default values.")
        
    def fancy_print(data):
        print(json.dumps(data, indent=2, separators=(',', ': ')))

    def connexion_post(self, method, data=None, session=None):
        url = self.URL_BASE + method
        if data: data = json.dumps(data)
        return json.loads(session.post(url, data=data).text)
    
    def connexeion_put(self, method, data=None, session=None):
        url = self.URL_BASE + method
        if data: data = json.dumps(data)
        return json.loads(session.put(url, data=data).text)

    def connexion_get(self, method, session=None):
        url = self.URL_BASE + method
        return json.loads(session.get(url).text)
    
    def connexion_delete(self, method, session=None):
        url = self.URL_BASE + method
        return json.loads(session.delete(url).text)
    
    def connexion_close(self, session):
        result = self.connexion_post("/login/logout/", session=session)
        print(result)
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



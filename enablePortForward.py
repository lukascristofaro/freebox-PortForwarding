import socket
from GetConnection import GetConnection

import sys
import json

class EnablePortForward():
    def __init__(self):
        self.connection = GetConnection()
        self.currentSession = self.connection.create_session()
        self.ip = "192.168.1.151"
        self.argv = sys.argv

    def argumentToJson(self):
        if len(self.argv) == 2:
            return int(self.argv[1])
        else:
            print("ID is required.")
            return
    def enablePortForward(self,info, enable : bool = True):
        method = "/fw/redir/" + str(info)
        data = {
            'enabled': enable
        }
        result = self.connection.connexeion_put(method, data, self.currentSession)
        if result.get('success'):
            if enable:
                print(f"Port forwarding rule {info} successfully enabled.")
            else:
                print(f"Port forwarding rule {info} successfully disabled.")
        else:
            print(f"Failed to disable port forwarding rule {info}.")
    def disablePortForward(self):
        self.enablePortForward(False)
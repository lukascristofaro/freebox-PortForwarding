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
    def enablePortForward(self, enable : bool = True):
        jsonARGV = self.argumentToJson()
        method = "/fw/redir/" + str(jsonARGV)
        data = {
            'enabled': enable
        }
        result = self.connection.connexeion_put(method, data, self.currentSession)
        if result.get('success'):
            if enable:
                print(f"Port forwarding rule {jsonARGV} successfully enabled.")
            else:
                print(f"Port forwarding rule {jsonARGV} successfully disabled.")
        else:
            print(f"Failed to disable port forwarding rule {jsonARGV}.")
    def disablePortForward(self):
        self.enablePortForward(False)

        
if __name__ == "__main__":
    enablePortForward = EnablePortForward()
    enablePortForward.enablePortForward()
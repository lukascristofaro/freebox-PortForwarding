import socket
from GetConnection import GetConnection

import sys
import json

class AddPortForward():
    def __init__(self):
        self.connection = GetConnection()
        self.currentSession = self.connection.create_session()
        self.ip = "192.168.1.151"
        self.argv = sys.argv
    
    def addPortForwardingWithInput(self):
        try:
            name = input("Enter the name of the port forwarding: ")
            port = int(input("Enter the port you want to forward: "))
            wan_port_start = int(input("Enter the start of the wan port range: "))
            wan_port_end = int(input("Enter the end of the wan port range: "))
            proto = input("Enter the protocol (tcp/udp): ")
            src_ip = input("Enter the source ip: ")
            info = {
                "name": name,
                "port": port,
                "wan_port_start": wan_port_start,
                "wan_port_end": wan_port_end,
                "proto": proto,
                "src_ip": src_ip
            }
            self.addportforwarding(info)
        except:
            print("An error occurred")
            return
        self.connection.connexion_close(self.currentSession)

    
    def addportforwarding(self, info):
        try:
            method = "/fw/redir/"
            data = {
                'enabled': True,
                "comment": info['name'],
                "lan_port": info['port'],
                "wan_port_end": info['wan_port_end'],
                "wan_port_start": info['wan_port_start'],
                "lan_ip": self.ip,
                "ip_proto": info['proto'],
                "src_ip": info['src_ip']
            }
            result = self.connection.connexion_post(method, data, self.currentSession)
            if result['success'] == True:
                print("port forwarding added successfully")
            else:
                print("error code:", result['error_code'], "\n", result['msg'])
            self.connection.connexion_close(self.currentSession)
        except Exception as e:
            print("An error occurred:", str(e))
            return "error"

    def get_portforwarding(self):
        try:
            method = "/fw/redir/"
            result = self.connection.connexion_get(method, self.connection.create_session())
            return result
        except:
            print('error while fetching portforwarding')

    def wanPortUsed(self):
        listePort = []
        data = self.get_portforwarding()
        if 'result' in data:
            for i in range(len(data['result'])):
                listePort.append(data['result'][i]['wan_port_start'])
                listePort.append(data['result'][i]['wan_port_end'])
        return listePort

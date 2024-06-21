from GetConnection import GetConnection

import sys
import json

class AddPortForward():
    def __init__(self):
        self.connection = GetConnection()
        self.currentSession = self.connection.create_session()
        self.ip = "192.168.1.151"
        self.argv = sys.argv

    def argumentToJson(self):
        if len(self.argv) == 2:
            return self.connection.get_config(self.argv[1])
        else:
            print('the argument has to be : \n \'{\"port\":xxxx, \"wan_port_end\":xxxxx, \"wan_port_start\":xxxxx, \"proto\":"tcp/udp", \"src_ip\":\"x.x.x.x\"}\'')
            return
        
    def scan_ports(self):
        target = self.ip
        start_port = 1
        end_port = 65535
        open_ports = []
        for port in range(start_port, end_port + 1):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target, port))
            if result == 0:
                open_ports.append(port)
            sock.close()
        print(open_ports)
        return open_ports

    def isvalidport(self, port):
        if type(port) != int:
            return "port has to be an integer"
        else:
            if port < 1 and port > 65535:
                return "the port has to be in the range 1-65535"
            elif port in scan_ports():
                return "this port is already used"
        return True

    def addportforwarding(self):
        jsonARGV = self.argumentToJson()
        listePort = self.wanPortUsed()
        if jsonARGV['wan_port_start'] in listePort or jsonARGV["wan_port_end"] in listePort:
            print('this wan port is already used')
            return
        try:
            method = "/fw/redir/"
            data = {'enabled' :True, "comment": jsonARGV['name'], "lan_port" : jsonARGV['port'], "wan_port_end" : jsonARGV['wan_port_end'], "wan_port_start" : jsonARGV['wan_port_start'], "lan_ip": self.ip, "ip_proto" : jsonARGV['proto'], "src_ip" : jsonARGV['src_ip']}
            print(data)
            result = self.connection.connexion_post(method, data, self.connection)
            connection.connexion_close(session)
        except:
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


a = AddPortForward()
a.addportforwarding()


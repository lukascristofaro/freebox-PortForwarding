from GetConnection import GetConnection

import sys

class DeletePortForward():
    def __init__(self):
        self.connection = GetConnection()
        self.argv = sys.argv
    
    def argumentToInt(self):
        if len(self.argv) == 2:
            return self.connection.get_config(self.argv[1])['wan_port_start']
            return self.argv[1]
        else:
            print('the argument has to be : xxxx')
            return

    def get_portforwarding(self):
        try:
            method = "/fw/redir/"
            result = self.connection.connexion_get(method, self.connection.create_session())
            return result
        except:
            print('unknow')

    def deletePortForwardByWanStart(self):
        wan_port_start = self.argumentToInt()
        id = None
        data = self.get_portforwarding()
        for i in range(len(data['result'])):
            if data['result'][i]['wan_port_start'] == int(wan_port_start):
                id = data['result'][i]['id']
        try:
            method = "/fw/redir/"+str(id)
            connection.connexion_close(session)
        except:
            print('error')

a = DeletePortForward()
a.deletePortForwardByWanStart()
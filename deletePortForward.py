from GetConnection import GetConnection

import sys

class DeletePortForward():
    def __init__(self):
        self.connection = GetConnection()
        self.currentSession = self.connection.create_session()
    
    def deletePortForward(self, info):
        self.connection.connexion_delete('/fw/redir/' + info, session=self.currentSession)
        self.connection.connexion_close(self.currentSession)
        print("Port forwarding deleted.")

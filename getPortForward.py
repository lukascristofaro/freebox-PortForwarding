from GetConnection import GetConnection

connection = GetConnection()
session = connection.create_session()

method = "/fw/redir/"

result = connection.connexion_get(method, session)
print(result)
connection.connexion_close(session)
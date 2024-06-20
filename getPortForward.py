from GetConnection import GetConnection

session = GetConnection()
try:
    method = "/fw/redir/"
    result = session.connexion_get(method, session.create_session())
    print(result)
except:
    print('error fetching data')

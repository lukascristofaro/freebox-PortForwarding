from GetConnection import GetConnection

connection = GetConnection()
session = connection.create_session()

method = "/fw/redir/"

def display_port_forwarding_info(data):
    if data.get('success'):
        print("\n")
        print(f"{'Name':<15} {'Port':<10} {'WAN Port Start':<15} {'WAN Port End':<15} {'Protocol':<10} {'Source IP':<15} {'Enabled':<10}")
        print(f"{'----':<15} {'----':<10} {'-------------':<15} {'------------':<15} {'--------':<10} {'---------':<15} {'-------':<10}")
        
        results = data.get('result', [])
        for entry in results:
            name = entry.get('comment', 'N/A')
            port = entry.get('lan_port', 'N/A')
            wan_port_start = entry.get('wan_port_start', 'N/A')
            wan_port_end = entry.get('wan_port_end', 'N/A')
            proto = entry.get('ip_proto', 'N/A')
            src_ip = entry.get('src_ip', 'N/A')
            enabled = 'Yes' if entry.get('enabled') else 'No'
            print(f"{name:<15} {port:<10} {wan_port_start:<15} {wan_port_end:<15} {proto:<10} {src_ip:<15} {enabled:<10}")
        print("\n")
        
    else:
        print("Failed to retrieve port forwarding information.")




result = connection.connexion_get(method, session)
display_port_forwarding_info(result)
connection.connexion_close(session)


from enablePortForward import EnablePortForward
from getPortForward import getPortForwarding
from addPortForward import AddPortForward
from deletePortForward import DeletePortForward
import sys

def main():
    method = sys.argv[1] if len(sys.argv) > 1 else None
    info = sys.argv[2] if len(sys.argv) > 2 else None
    if len(sys.argv) < 2:
        print("Please provide an argument.")
        print("Available commands:")
        print("  get                 - Get the current port forwarding configuration")
        print("  add                 - Add a new port forwarding rule")
        print("  delete <ID>         - Delete a port forwarding rule by ID")
        print("  enable <ID>         - Enable a port forwarding rule by ID")
        print("  disable <ID>        - Disable a port forwarding rule by ID")
        return
    if method == "get":
        getPortForwarding()
    elif method == "add":
        AddPortForward().addPortForwardingWithInput()
    elif method == "delete":
        DeletePortForward().deletePortForward(info)
    elif method == "enable":
        info = validInfo(info)
        EnablePortForward().enablePortForward(info, True)
    elif method == "disable":
        info = validInfo(info)
        EnablePortForward().enablePortForward(info, False)
    else:
        print("Invalid argument.")
        return

def validInfo(info):
    if info == None:
        info = int(input("Enter the ID of the port forwarding: "))
        return info
    try :
        info = int(info)
    except:
        print("ID has to be an integer")
        return

    else :
        return info

if __name__ == "__main__":
    main()
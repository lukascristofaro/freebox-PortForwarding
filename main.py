from enablePortForward import EnablePortForward
from getPortForward import getPortForwarding
from addPortForward import AddPortForward
from deletePortForward import DeletePortForward
import sys

def main():
    method = sys.argv[1] if len(sys.argv) > 1 else None
    info = sys.argv[2] if len(sys.argv) > 2 else None
    print(sys.argv)
    if len(sys.argv) < 2:
        print("Please provide an argument.")
        return
    if method == "get":
        getPortForwarding()
    elif method == "add":
        AddPortForward().addPortForwardingWithInput()
    elif method == "delete":
        DeletePortForward().deletePortForward(info)
    elif method == "enable":
        EnablePortForward().enablePortForward(info)
    elif method == "disable":
        EnablePortForward().disablePortForward(info)
    else:
        print("Invalid argument.")
        return

if __name__ == "__main__":
    main()
# NOUR A SHARAKY 202000149
# GETTING THE IP ADDRESS OF THE DEVICE CODE

import socket
# Function to get the device's IP Address
def getIP():
    IP = socket.gethostbyname(socket.gethostname())
    return IP

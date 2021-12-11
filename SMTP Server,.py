# NOUR A SHARAKY 202000149
# SMTP/IP SERVER SIDE

# From socket module we import the required structures and constants
from socket import AF_INET, SOCK_STREAM, socket, gethostname
# Importing IP_Address file to get the devide's IP Address
import IP_Address
# Importing os.path to get the file path in which the SMTP data will be stored
import os.path
# Importing re to verify that valid email address and data format was input
import re
# Importing sys to terminate application when an error occurs
import sys
# From OS we import getpid to get the process id given by OS when we execute this code
from os import getpid

global boolean
boolean = True
Boolean = True
# Folder name in which SMTP data will be stored
save_path = 'Emails/'

# Function to extract and return the clients' MAC Addresses
def MAC(ip):
    # Opens the ARP table
    with os.popen("arp -a") as f:
        data = f.read()
    # Looks for the given IP Address  in the table
    # defines a starting point where the MAC address coresponding to the given IP Address starts
    start = data.find(ip)+len(ip)+7
    # defines an ending point where the MAC address coresponding to the given IP Address ends
    end = start + 17
    # variable where the MAC address is stored according to the starting position and the ending position
    mac_address = data[start:end]
    return mac_address

# using the getIP function in the IP_Address module to get the device's IP address
IP = IP_Address.getIP()

print("Welcome to Nour Sharaky's SMTP application - Server Side")
# getting the process id - unique identifier for the active process
print("OS assigned process id:", getpid())

# A forever loop that doesn't stop unless it is interrupted or an error occurs
while True:
    try:
      # assigning the socket's IP address and port number
      sock = (IP,25)
      # creating a TCP/IP socket  
      s = socket(AF_INET,SOCK_STREAM)
      print("TCP/IP - SMTP Socket Created")
      # getting the file descriptor no. - unique identifier for the active open file
      print("File descriptor asssigned by os:", s.fileno())
      # Binding the TCP/IP socket to the device's IP address and SMTP port 25 
      s.bind(sock)
      # displaying the socket name (IP Address & port no) to the user
      print('Server Socket is bound to %s:%d' % s.getsockname())
      # Put socket into listening state with no queueing 
      s.listen(0)
      break
    except:
        print("Socket connection error! Try again.")
        sys.exit()

# A forever loop that doesn't stop unless it is interrupted or an error occurs
# The start of the Simple Mail Transfer Protocol handshake
while Boolean:
    try:
        # Establishing a connection with the clients' socket
        client_socket, client_addr = s.accept()
        # getting the client socket's MAC address and sending it back to the client
        client_socket.send(MAC(client_addr[0]).encode())
        # sending the 220 service ready command to the client
        msg= "220 connection accepted from " + gethostname() 
        print(msg)
        client_socket.send(msg.encode())
        print("220 - Service ready command sent to client")
        print()
        # gathering and displaying some information about the client to the server's users
        # displaying the client's socket name (IP Address & port no) & MAC Address to the user
        print("Client connected from %s %d" % client_addr)
        print("Client IP Address:", client_addr[0])
        print("Client Port Number:", client_addr[1])
        print("Client MAC Address:", MAC(client_addr[0]))
        print()
    except:
        print("Socket connection error.")
        sys.exit()

    try:
        # Recieving Helo command from client
        helo = client_socket.recv(1024).decode("utf-8")
        # checks if recieved command's message starts with "HELO"
        if helo[:4] == "HELO":
            print("HELLO command recieved from client")
            # server responds to the client with the 250 OK command 
            msg=  "250 - OK,  Hello " + gethostname() + ". Pleased to meet you."
            client_socket.send(msg.encode())
            print("250 - OK command sent to client")
            boolean = True           
    except:
        # HELO command not recieved
        print("HELO error, Try again!")
        sys.exit()
    # A forever loop that doesn't stop unless it is interrupted or an error occurs
    while boolean:
        print("recieving mail from info")
        # recieve MAIL FROM command from client
        mailFrom_command= client_socket.recv(1024).decode("utf-8")
        print("MAIL FROM command recieved from client")
        # check if MAIL FROM command input is out of order
        _check1 = re.match(r'RCPT(\s+|$)TO:', mailFrom_command)
        _check2 = re.match(r'DATA', mailFrom_command)
        # reference to check if email from input format is valid or not
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        valid= re.match(regex, mailFrom_command[13:])
        # error messages in case of invalid inputs:
        if _check1:
            print("503 Bad sequence of commands")  
            client_socket.send('503 Bad sequence of commands'.encode())
            continue
        if _check2:
            print("503 Bad sequence of commands") 
            client_socket.send('503 Bad sequence of commands'.encode())
            continue
        elif not valid:
            print("501 Syntax error in parameters or arguments. Invalid mail.")
            client_socket.send('501 Syntax error in parameters or arguments'.encode())
            continue
        else:
            print("MAIL FROM command accepted")
            From = mailFrom_command.replace("MAIL FROM", "FROM")
            # When valid mail from command inout is processed, the server responds with a 250 OK command
            client_socket.send("250 - OK".encode())
            print("250 - OK command sent to client")

        _bool = True
        # lists to store To and From recepients
        to_list = []
        rcpt_list = []

        # A forever loop that doesn't stop unless it is interrupted or an error occurs
        while boolean:
            #recieve RCPT TO command from client
            rcptTo_command = client_socket.recv(1024).decode("utf-8")
            print("RCPT TO command recieved from client")
            # check if RCPT TO command input is out of order
            check = re.match(r'DATA', rcptTo_command)   
            check2 = re.match(r'MAIL(\s+|$)FROM:' , rcptTo_command)            
            # checks for valid RCPT TO inputs
            rcpt = re.match(regex, rcptTo_command[11:])
            if rcptTo_command[:7] == 'Subject':
                rcptTo_command = 'DATA'
                _bool = False
                continue
            # error messages in case of invalid inputs:
            if _bool is False:
                if check:
                    print('503 Bad sequence of commands')
                    break
                if check2:
                    print('503 Bad sequence of commands')
                    client_socket.send('503 Bad sequence of commands'.encode())
                    continue
            if not rcpt:
                print('501 Syntax error in parameters or arguments')
                client_socket.send('501 Syntax error in parameters or arguments'.encode())
                continue
            else:
                _bool = False
                # make txt files with domain names 
                # formatting file names
                file_name = rcptTo_command.replace("RCPT TO: ", "")
                file_name = file_name.strip('>')
                file_name = file_name.split('@', 1)[-1]
                to = rcptTo_command.replace("RCPT TO: ", "")
                rcpt_list.append(to)
                # saving file in the specified path name in line 21
                save_name = os.path.join(save_path, file_name)
                if not os.path.exists(save_path):
                    os.makedirs(save_path)
                # appending file names to the to list
                file1 = open(save_name+".txt", "a")
                to_list.append(file1)
                # server responds with 250 OK command to the client
                client_socket.send('250 OK'.encode())
                print("250 - OK command sent to client")
                
            # write From and To in files - formatting file inputs
            '''for files in to_list:
                file1 = files
                size = len(rcpt_list)
                file1.write("\n" + From + "\n")
                file1.write("To: ")
                for rcpt in rcpt_list:
                    size = size - 1
                    if size is 0:
                        file1.write(rcpt + "\n")
                    else:
                        file1.write(rcpt + ", ")'''
            # A forever loop that doesn't stop unless it is interrupted or an error occurs
            while boolean:
                if not check:
                    # receive DATA command from client
                    DATA_command = client_socket.recv(1024).decode("utf-8")
                    print("DATA command recieved from client")
                    # check if DATA command input is out of order
                    check = re.match(r'DATA', DATA_command)
                if not check:
                    # error messages in case of invalid inputs:
                    print("500 Syntax error: command unrecognized")
                    client_socket.send('500 Syntax error: command unrecognized'.encode())
                    continue
                else:
                    # server responds with 354 start mail input command to the client
                    print("354 - Start mail input command sent to client")
                    client_socket.send('354 Start mail input; end with <CRLF>.<CRLF>'.encode())

                # A forever loop that doesn't stop unless it is interrupted or an error occurs
                while boolean:
                    # receive mail transactions until <CRLF>.<CRLF> is input -> quits      
                    data = client_socket.recv(1024).decode("utf-8")
                    print("Mail transactions recieved from client")
                    # stops mail transactions after "."
                    if data == '.':
                        # 250 OK command sent to the client once the server recievs the termination sign "."
                        client_socket.send('250 OK'.encode())
                        print("250 - OK command sent to client")
                        boolean = False
                        print("terminating command recieved from client")

                        # writing to files in list
                        for files in to_list:
                            file1 = files
                            file1.close()

                        # server recieves quit command from client
                        quitCmd = client_socket.recv(1024).decode("utf-8")
                        print("QUIT command recieved from client")
                        if re.match(r'QUIT', quitCmd):
                            # server responds to the client with the 221 connection closed command
                            client_socket.send('221 Bye'.encode())
                            print('221 - Connection closed command sent to client')
                            boolean = False
                            break
                    else:
                        client_socket.send(data.encode())
                        for files in to_list:
                            file1 = files
                            file1.write("\n" + data + "\n")
                            continue
    break
        
            
            
            
            

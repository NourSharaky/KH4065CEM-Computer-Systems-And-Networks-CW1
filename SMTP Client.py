# NOUR A SHARAKY 202000149
# SMTP/IP CLIENT SIDE

# From socket module we import the required structures and constants
from socket import AF_INET, SOCK_STREAM, socket
# From OS we import getpid to get the process id given by OS when we execute this code
from os import getpid
# Importing sys to terminate application when an error occurs
import sys
# Importing IP_Address file to get the devide's IP Address
import IP_Address

# using the getIP function in the IP_Address module to get the device's IP address
IP = IP_Address.getIP()
# assigning the client socket's IP address and port number ina variable
sock = (IP,7777)
# asking user to input server's IP Address and port no.
server_IP_address= input("Enter the SMTP server's IP Address: ")
server_port_address= int(input("Enter the SMTP server's Port Address: "))
# assigning the server socket's IP address and port number in a variable
serveraddr = (server_IP_address,server_port_address)

print()
print("Welcome to Nour Sharaky's SMTP application - Client Side")
# getting the process id - unique identifier for the active process
print("OS assigned process id:", getpid())
# creating a TCP/IP socket  
s = socket(AF_INET,SOCK_STREAM)
print("TCP/IP - SMTP Socket Created")
# Binding the TCP/IP socket to the device's IP address and port 7777 
s.bind(sock)
# displaying the client's socket name (IP Address & port no) to the user
print('Client Socket is bound to %s:%d' % s.getsockname())

# Establishing a connection with the server's socket
s.connect(serveraddr)
# gathering and displaying some information about the server and client sockets
# displaying the server's socket name (IP Address & port no) 
print('Socket Connected to %s:%d' % s.getpeername())
# recieve MAC Address details from server 
mac = s.recv(1024).decode("utf-8")
# check for handshake/connection made 
# recieving the 220 service ready command from server
msg = s.recv(1024).decode("utf-8")
if msg[:3] != '220':
    print('Unable to connect to server. Please try again later.')
    s.close()
    sys.exit()
else:
    # displays that the server is ready for SMTP transactions
    print("Server's response:", msg)
    # displays the client's MAC Address as extracted and recieved from the server
    print("Server's response: The client's MAC address is", mac)
    
# Send HELO command and print server response
heloCommand = 'HELO'
s.send(heloCommand.encode())
print("Helo command sent to server")
# recieving 250 OK command from server
recv1 = s.recv(1024).decode("utf-8")
# checks if recieved command's message starts with "250"
if recv1[:3] != '250':
    print('Unable to connect to server. Please try again later.')
    s.close()
    sys.exit() 
else:
    print("250 - OK command recieved from server")

x = 0   
# A forever loop that doesn't stop unless it is interrupted or an error occurs
while True: 
    # A forever loop that doesn't stop unless it is interrupted or an error occurs
    while True:
        # prompts user to enter email from input
        mailFrom = input('\nFrom: ')
        msg ='MAIL FROM: <' + mailFrom + '>'
        # client sends MAIL FROM command to the server
        s.send(msg.encode())
        print()
        print("MAIL FROM command sent to server")
        # recieving 250 OK command from server 
        okFrom = s.recv(1024).decode("utf-8")
        # checks if recieved command's message starts with "250"
        if okFrom[:3] != "250":
            # displays error message in case of invalid input then re-prompts user to re-input valid email address format
            print(okFrom)
            print ('Please enter a valid email address.')
            continue
        else:
            print("250 - OK command recieved from server") 
            break

    # A forever loop that doesn't stop unless it is interrupted or an error occurs
    while True:
        if x == 1:
            break
        print()
        # prompts user to enter RCPT TO input separated by comma and space
        rcptTo = input('To: ')
        # formating the RCPT TO message in case of multiple inputs        
        toList = rcptTo.split(", ")
        for tos in toList: 
            msg = 'RCPT TO: <' + tos + '>'
            # client send RCPT TO command to the server
            s.send(msg.encode())
            print()
            print("RCPT TO command sent to server")
            # recieving 250 OK command from server
            okTo = s.recv(1024).decode("utf-8")
            # checks if recieved command's message starts with "250"
            if okTo[:3] != "250":
                print ('One or more email addresses are invalid. Please re-enter')
                x = 0 
                break
            else: 
                print("250 - OK command recieved from server")
                x = 1 

    # send DATA command to server
    s.send('DATA'.encode())
    print("DATA command sent to server")  
    # recieving 354 start mail input from server
    okData = s.recv(1024).decode("utf-8")
    # checks if recieved command's message starts with "354"
    if okData[:3] != "354":
        print ('There is an error.')
    else:
        print("354 - Start mail input command recieved from server")

    # mail transactions - formatting the email content
    writeFrom = ('From: ' + mailFrom)
    s.send(writeFrom.encode())
    s.recv(1024).decode("utf-8")
    
    writeTo = ('To: ' + rcptTo)
    s.send(writeTo.encode())
    s.recv(1024).decode("utf-8")

    print()
    # prompts user to enter the email's subject input   
    readSubject = input('Subject: ')
    msg= 'Subject: ' + readSubject + '\n'
    s.send(msg.encode())
    s.recv(1024).decode("utf-8")

    # prompts user to enter message contents
    print("\n(Note: enter a new line and a "+ "." +" to end message content)\n")    
    sys.stdout.write('Message: ')
    
    # A forever loop that doesn't stop unless it is interrupted or an error occurs
    while True:
        # input mail body contents 
        readData = input()
        if readData == '':
            readData = '\r'
        s.sendall(readData.encode())
        
        # recieving 250 OK command from server indicating that a termination sign was entered "."
        okEnd = s.recv(1024).decode("utf-8")
        # checks if recieved command's message starts with "250" to terminate proccess
        if okEnd[:3] == '250':
            # Quit command sending to server
            s.send('QUIT'.encode())
            print("Terminating...\nMail content sent to server for analysing") 
            print("250 - OK command sent to server")
            # recieving 221 connection closed command from server
            quitMsg = s.recv(1024).decode("utf-8")
            # checks if recieved command's message starts with "221" to close connection
            if quitMsg[:3] != '221':
                print ('There was an error. Quitting.')
                sys.exit()
            else:
                print("221 - Connection closed command recieved from server")
                s.close()
                sys.exit()
                break
        else:
            continue    
                
                
                
        
        
        
        

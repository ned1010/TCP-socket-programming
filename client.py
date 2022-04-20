#Citations
#I refer various sources from the github to do this assignment
# 1.https://github.com/kanika2296/client-sever-password-based-authentication-in-python
# 2.https://github.com/sunilale0/python-socket-programming

import socket

PORT = 5545
IP = "127.0.0.1"
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connecting the client socket
client_socket.connect((IP, PORT))


#confirming the connection
response = client_socket.recv(1024).decode()
print(response)

# ip address of the client devices
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
client_socket.send(ip_address.encode())


# user query
query = int(input("\nEnter your query: "))
client_socket.send((str(query)).encode())


# Depending on query, we direct to 3 cases
if query == 1:
    # receving the email prompt/input from the server
    response = client_socket.recv(1024).decode()
    email = input(response)
    # if client's email is not associated ashoka, don't allow to enter!
    while "@ashoka.edu.in" not in email:
        email = input(response)
    client_socket.send(str.encode(email))

    # receiving the key word "register or registered" to determine whether the client is registered or not.
    response = client_socket.recv(1024).decode()

    # if keyword received is register, then create new registration
    if str(response) == "register":
        confirmation = client_socket.recv(1024).decode()
        # providing user with password generated from the server.
        password = client_socket.recv(1024).decode()
        print(confirmation)
        print(password)

    elif str(response) == "registered":
        # if registered, server asks for password
        response = client_socket.recv(1024).decode()
        password = input(response)
        # sending password back to server
        client_socket.send(str.encode(password))
        # confirmation of connection
        confirmation = client_socket.recv(1024).decode()
        print(confirmation)

        # voting result from the server
        voting_result = client_socket.recv(1024).decode()
        print(voting_result)

        if 'voted' in voting_result:
            client_socket.close()
        else:
            vote = input("\nYour turn to vote: ")
            # sending the selected vote to server
            client_socket.send(vote.encode())
            # acknowlodgement for voting
            response = client_socket.recv(1024).decode()
            print(response)


# query 2 will show the result only after the voting period is over
elif query == 2:
    # receving the email prompt/input from the server
    response = client_socket.recv(1024).decode()
    email = input(response)
    # if client's email is not associated ashoka, don't allow to enter!
    while "@ashoka.edu.in" not in email:
        email = input(response)
    # sending back the email to server
    client_socket.send(str.encode(email))

    # received the key word "register or registered" to determine whether the client is registered or not.
    response = client_socket.recv(1024).decode()
    if str(response) == "register":
        print("You can't view it as you have not registered!")
    elif str(response) == "registered":
        response1 = client_socket.recv(1024).decode()
        password = input(response1)
        client_socket.send(str.encode(password))
        confirmation = client_socket.recv(1024).decode()
        print(confirmation)

        result = client_socket.recv(1024).decode()
        print(result)

elif query == 3:
    response = client_socket.recv(1024).decode()
    print(response)

client_socket.close()

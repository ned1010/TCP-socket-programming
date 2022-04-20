import socket
import string
import random
import time


PORT = 5545
IP = "127.0.0.1"

# Establishing TCP connection between server and client
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((IP, PORT))
server_socket.listen(1)

print('Server is running at IP:{} and PORT:{}'.format(IP, PORT))

# dictionary for storing password and email
password_table = {}
# dictionary for counting the votes for each candidate
votes = {1: [], 2: [], 3: [], 4: []}

# characters for password generation
characters = list(string.ascii_letters.upper() + "!@#$%^&*()" +
                  string.digits + string.ascii_letters.lower())

def generate_password():
    # randomised the characters
    random.shuffle(characters)
    # makeing password list and appending
    password = []
    for i in range(5):
        password.append(random.choice(characters))
        # shuffling the resultant password
        random.shuffle(password)

    password = ("".join(password))
    return password

#registration function as well will authenticate
def authentication(connection):
    # a variable to determine whether a client authenticated or not.
    authenticated = False
    # asking for email from client
    connection.send(str.encode('Enter ashoka email: '))
    # receving client's email
    global email
    email = connection.recv(1024).decode()
    # If user has already in the database
    if email in password_table:
        # sending alert keyword that user has already registered using word "registered"
        connection.send(str.encode('registered'))
        # if registered, request for password provided early
        connection.send(str.encode('Enter  your password: '))
        # receives the password from the client
        password = connection.recv(1024).decode()
        if(password_table[email] == password):
            connection.send(str.encode('You have conected to the server!'))
            # print(email)
            authenticated = True

    # If email id is not in database, create an account for the register user
    else:
        # sending a register message to alert that client has not registered
        connection.send(str.encode('register'))
        # generating password
        password = generate_password()
        connection.send(str.encode("Hooray!, you are registered"))
        connection.send(str.encode("Your password: " + str(password)))
        password_table[email] = password
        print(password_table)
        client_socket.close()
    return authenticated



def voting(): 
    #this variable is use to decided whether client has voted or not
    voted = False
    for _, values in votes.items():
        if ip_address in values:
            # if ip address is not in the password_table, then allow to register or otherwise, don't allow same ip address again
            voted = True

    # if the client hasn't voted, allow the client to vote
    if voted == False:
        message = "Here is your voting options!\n" + "Who is your candidate for school prefect?\n" + \
            "(1) Micheal (2) Thomas (3) John (4) Kumar "
        # sending the vote options
        client_socket.send(message.encode())

        # receiving the vote option from the client
        vote = client_socket.recv(1024).decode()
        print("Client with a {} has selected {} ".format(ip_address, vote))
        # appending the ip address as value in votes dictionary
        votes[int(vote)].append((ip_address))

        # confirmation message for voting
        message = "Thank you for participating. Your response is registered against your IP Address: {}".format(ip_address) + \
            "\nYour password was " + password_table[email]
        client_socket.send(message.encode())
        client_socket.close()

    # if the client have already voted.
    else:
        message = "Already voted with ip address {}".format(ip_address)
        print(message)
        client_socket.send(message.encode())
        client_socket.close()


#Main Code
while True:
    client_socket, address = server_socket.accept()
    info = "\nWelcome! You can participate in the vote by presenting your password.\n" + \
        "Reply with a \"1\" if you want to participate now; with a \"2\" if you want to see the results;\n" + \
        "and with \"3\" otherwise."
    client_socket.send(info.encode())

    # ip_address of client. It will passed with voting function to keep record a record vote
    ip_address = client_socket.recv(1024).decode()

    # receiving query number from client
    query = client_socket.recv(1024).decode()

    if query == '3':
        client_socket.send(("You are disconnected!").encode())
        client_socket.close()

    elif query == '1':
        # finding whether client is authenticated or not when client replies 1
        permission = authentication(client_socket)
        if permission == True:
            # if client authenticated, allow them to vote!
            voting()

    elif query == '2':
        # finding whether client is authenticated or not when client replies 2
        permission = authentication(client_socket)
        if permission == True:
            now = time.localtime()
            current_time = time.strftime("%H:%M:%S", now)
            if str(current_time) >= '15:00:00':
                result = "\nthe number of responses each candidate has received: \n"
                for key, value in votes.items():
                    result = result + \
                        "answers {} : {} \n".format(key, len(value))
                # print(result)
                client_socket.send((result).encode())
            else:
                client_socket.send(
                    ("Voting is not yet close closed, results will be displayed after 3pm!").encode())
                client_socket.close()

server_socket.close()

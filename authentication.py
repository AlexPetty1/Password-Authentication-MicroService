from argon2 import PasswordHasher
import zmq

# Store port number for the program to bind to
PORT_NUM = 9999

# Store separator for input and output
SEPERATOR = '\n'

SUCCESS = 1
FAIL = 0


def argon2():
    ph = PasswordHasher()
    hash = ph.hash("s3kr3tp4ssw0rd")
    print(hash)
    print(ph.verify(hash, "s3kr3tp4ssw0rd"))



def addType(username, password):
    doesUsernameExist = False

    if(doesUsernameExist == True):
        return (FAIL, "Username already exists")
    
    ph = PasswordHasher()
    hash = ph.hash(password)

    return (SUCCESS, "Password and Username added")
    #store hash in database

def checkType(username, inputPassword):
    doesUsernameExist = False
    doesPasswordExist = False

    if(doesUsernameExist == False):
        return (FAIL, "Username does not exist")
    
    if(doesPasswordExist == False):
        return (FAIL, "Password does not exist")
    
    #get hash from database
    hash = "adadda"
    ph = PasswordHasher()
    

    if(ph.verify(hash, inputPassword)):
        return (SUCCESS, "User authenticated")
    else:
        return (FAIL, "Invalid password")


def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:" + str(PORT_NUM))

    while(True):
        message = socket.recv()
        message = message.decode()
        messageSep = message.split(SEPERATOR)
        print(messageSep)

        if(len(messageSep) != 3):
            print("Needs three inputs, seperated by new line")
        
        messageType = messageSep[0]
        username = messageSep[1]
        password = messageSep[2]

        messageBack = 0
        success = 0

        match messageType:
            case 'Add':
                (success, messageBack) = addType(username, password)
            case 'Check':
                (success, messageBack) = checkType(username, password)
            case _:
                success = FAIL
                messageBack = "Invalid type"
        
        returnMessage = str(messageType) + "\n" + str(username) + "\n" + str(success) + "\n" + messageBack
        print(returnMessage)
        socket.send_string(returnMessage)


main()
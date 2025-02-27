from argon2 import PasswordHasher
import zmq
from pymongo import MongoClient

# Store port number for the program to bind to
PORT_NUM = 9995

# Store separator for input and output
SEPERATOR = '\n'
SUCCESS = 1
FAIL = 0

#set uri equal to connection string
connectionString = "SET ME TO CONNECTION STRING"
client = MongoClient(connectionString)
mydb = client.authenticationMicroservice
userCollection = mydb.userInfo

#verifies a connection to mongoDB
try:
    client.admin.command('ping')
except Exception as e:
    print(e)
    print("Mongo could not connect")
    exit()



def isUserInDB(username):
    query = { "username": username}
    doesUserExist = userCollection.count_documents(query)

    if(doesUserExist == 0):
        return False
    
    return True


def addType(username, password):
    #user must not exist
    if(isUserInDB(username)== True):
        return (FAIL, "Username already exists")
    
    #computes hash
    ph = PasswordHasher()
    hash = ph.hash(password)

    #adds user
    user = { "username": username, "password": hash }
    userCollection.insert_one(user)

    return (SUCCESS, "Username and Password added")


def checkType(username, inputPassword):
    #user must exist
    if(isUserInDB(username) == False):
        return (FAIL, "Username does not exist")

    #get hash from database
    query = { "username": username}
    queryResults = userCollection.find_one(query)
    hash = queryResults["password"]
    print("Hash: " + str(hash))
    ph = PasswordHasher()
    
    #verifies hash
    try:
        if(ph.verify(hash, inputPassword)):
            return (SUCCESS, "User authenticated")
        else:
            return (FAIL, "Invalid password")
    except:
        return (FAIL, "Invalid password")

def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:" + str(PORT_NUM))

    while(True):
        message = socket.recv()
        message = message.decode()
        messageSep = message.split(SEPERATOR)
        print("Recieved: " + message + "\n\n")

        if(len(messageSep) != 3):
            socket.send_string("Error\n \n0\nMust have three inputs seperated by a newline character")
            continue
        
        messageType = messageSep[0]
        username = messageSep[1]
        password = messageSep[2]

        messageBack = ""
        result = 0
        match messageType:
            case 'Add':
                (result, messageBack) = addType(username, password)
            case 'Check':
                (result, messageBack) = checkType(username, password)
            case _:
                result = FAIL
                messageBack = "Invalid type"
                messageType = "Error"

        returnMessage = str(messageType) + "\n" + str(result) + "\n" + messageBack
        print("Returning: " + returnMessage)
        socket.send_string(returnMessage)


main()
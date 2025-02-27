import zmq

PORT_NUM = 9995
context = zmq.Context()

#  Socket to talk to server
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:" + str(PORT_NUM))

def instructions():
    print("Input format:")
    print(" Type (Add or Check)")
    print(" Username")
    print(" Password")

    print("\nOutput format")
    print(" Type")
    print(" Username")
    print(" Success")
    print(" Message\n")


while(True):
    inputType = input("Input the message type (Add, Check): ")
    username = input("Input username: ")
    password = input("Password: ")

    messageSent = str(inputType) + "\n" + str(username) + "\n" + str(password)
    socket.send_string(messageSent)

    #  Get the reply
    response = socket.recv()
    response = response.decode()
    responseSep = response.split("\n")

    outputType = responseSep[0]
    result = responseSep[1]
    responseMessage = responseSep[2]

    print("\nResponse:")
    print(outputType)
    print(result)
    print(responseMessage)


    #prompt new input
    decision = input("Input 1 to input another request\nInput 2 exit: ")
    while ((decision != "1") and (decision != "2")):
        decision = input("Input 1 to input another request \nInput 2 exit\n: ")

    if(decision == "2"):
        break
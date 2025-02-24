import zmq

PORT_NUM = 9999

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

    #  Do 10 requests, waiting each time for a response
    messageSent = str(inputType) + "\n" + str(username) + "\n" + str(password)
    socket.send_string(messageSent)

    #  Get the reply.
    message = socket.recv()
    message = message.decode()
    print("Message returned: \n" + message + "\n\n")

    decision = input("Input 1 to input another request\nInput 2 exit: ")
    while ((decision != "1") and (decision != "2")):
        decision = input("Input 1 to input another request \nInput 2 exit: ")

    if(decision == "2"):
        break
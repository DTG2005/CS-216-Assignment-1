import Node
import threading

Name = input("Enter your name: ")
Port = int(input("Enter your port number: "))
print("Server listening on port ", Port)

Node1 = Node.Node(Port)
threading.Thread(target=Node1.start_server).start()

while True:
    print("*** Menu ***")
    print("1. Send Message")
    print("2. Query Active Peers")
    print("3. Connect to active peers")
    print("0. Quit")

    try:
        choice = int(input())
        if(choice == 0):
            break
        elif(choice == 3):
            try:
                host = input("Enter the host: ")
                port = int(input("Enter the port: "))
            except:
                print("Invalid input")
                continue
            else:
                Node1.connect_to_peer(host, port)
                print("Connected to ", host, ":", port)
        elif(choice == 2):
            print("Active Peers: ", Node1.peers)
        elif(choice == 1):
            message = input("Enter the message: ")
            Node1.send_message(message)
        else:
            print("Invalid choice")
            continue
    except Exception as e:
        print(e)
        continue
import Node
import threading

Name = input("Enter your name: ")
Host = input("Enter your IP address: ")
Port = int(input("Enter your port number: "))

print(f"🚀 Server starting on port {Port}...")
Node1 = Node.Node(Host, Port, Name)

# Start the server thread
threading.Thread(target=Node1.start_server, daemon=True).start()

while True:
    print("\n*** Menu ***")
    print("1. Send Message")
    print("2. Query Active Peers")
    print("3. Connect to Active Peers")
    print("0. Quit")

    try:
        choice = int(input("Enter choice: "))
        
        if choice == 0:
            print("Exiting...")
            break
        
        elif choice == 3:
            try:
                host = input("Enter the peer IP: ")
                port = int(input("Enter the peer port: "))
                Node1.connect_to_peer(host, port)
            except ValueError:
                print("❌ Invalid input. Please enter a valid IP and port.")

        elif choice == 2:
            print("🔄 Active Peers:")
            Node1.query_peers()

        elif choice == 1:
            message = input("Enter your message: ")
            Node1.send_message(message)

        else:
            print("❌ Invalid choice, try again.")
    
    except Exception as e:
        print(f"⚠ Error: {e}")
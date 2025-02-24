import Node
import threading

Name = input("Enter your name: ")
Host = input("Enter your IP address: ")
Port = int(input("Enter your port number: "))

print(f"🚀 Server starting on port {Port}...")
Node1 = Node.Node(Host, Port, Name)

# Start the server thread
threading.Thread(target=Node1.start_server, daemon=True).start()

Node1.send_mandatory_messages()

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
            Node1.connect_to_active_peers()

        elif choice == 2:
            print("🔄 Active Peers:")
            Node1.query_peers()

        elif choice == 1:
            if not Node1.active_connections:
                recipient_ip = input("Enter recipient's IP: ")
                recipient_port = int(input("Enter recipient's Port: "))
            else:
                print("Active connections:")
                for i, (ip, port) in enumerate(Node1.active_connections.keys(), 1):
                    print(f"{i}. {ip}:{port}")
                choice = int(input("Choose a connection (0 for new): "))
                if choice == 0:
                    recipient_ip = input("Enter recipient's IP: ")
                    recipient_port = int(input("Enter recipient's Port: "))
                else:
                    recipient_ip, recipient_port = list(Node1.active_connections.keys())[choice - 1]
            Node1.send_message(recipient_ip, recipient_port, port)

        else:
            print("❌ Invalid choice, try again.")
    
    except Exception as e:
        print(f"⚠ Error: {e}")
# Assignment 1

## Problem Statement

Implement a peer-to-peer chat program in a language of your choice that enables simultaneous sending and receiving messages simultaneously, supports multiple peers, and allows users to query and retrieve the list of peers from which it had received messages. Multiple instances of the code can be run in seperate terminal environments to form a peer to peer chat network. We assume that:-

- The program requires the user to know the IP address and port numbers of other users beforehand.

## How to run the program

You are required to run:-

```sh
python p2p_chat.py
```

This will run the program

## Navigation

On running the following prompt will be shown:-

```sh
Enter your name: <Enter team name>
Enter your port number: <Enter port number you wish to listen to here>
Server listening on port  8080
*** Menu ***
1. Send Message
2. Query Active Peers
3. Connect to active peers
0. Quit
```

You can use option 1 to send messages to active peers, 2 to query active peers and 3 to connect to active peers.

On selecting option 3:-

```sh
Enter the host: <Enter host of the node you wish to connect to>
Enter the port: <Enter port>
```

On correctly Entering both, you will be connected to the Node running this p2p script as well.

_**Note:**_ Our code so far does **not** solve the bonus question.

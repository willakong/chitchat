""" Use TCP Sockets """
from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, socket
from threading import Thread

""" Accept new connections """
def accept_incoming_connections():
  while True:
    client, client_address = SERVER.accept()
    addresses[client] = client_address
    Thread(target=handle_client, args=(client,client_address,)).start()

""" Handles a single client """
def handle_client(client, client_address):  # Takes client socket as argument
  name = client.recv(BUFF_SIZE).decode("utf8")
  print("{0}: {1} ({2}) has connected.".format(client_address[0], client_address[1], name))

  welcome = "Welcome %s! If you ever want to quit, type \\quit to exit." % name
  client.send(bytes(welcome, "utf8"))
  msg = "{0} has joined the chat!".format(name)
  broadcast(bytes(msg, "utf8"))
  clients[client] = name
  while True:
    msg = client.recv(BUFF_SIZE)
    if msg != bytes("\\quit", "utf8"):
      broadcast(msg, name+": ")
    else:
      print("{0}: {1} ({2}) has disconnected.".format(client_address[0], client_address[1], name))
      client.close()
      del clients[client]
      broadcast(bytes("{0} has left the chat.".format(name), "utf8"))
      break

""" Broadcasts message to other clients """
def broadcast(msg, prefix=""):  # prefix is for name identification
  for sock in clients:
    sock.send(bytes(prefix, "utf8")+msg)

clients = {}
addresses = {}

HOST = ''
PORT = 33000
BUFF_SIZE = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
SERVER.bind(ADDR)

""" Entry point (if not module) """
if __name__ == "__main__":
  SERVER.listen(5)  # Listens for 5 connections max
  print("Waiting for connection...")
  ACCEPT_THREAD = Thread(target=accept_incoming_connections)
  ACCEPT_THREAD.start() # Starts the infinite loop
  ACCEPT_THREAD.join()
  SERVER.close()
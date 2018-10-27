"""
Tkinter resources:
http://effbot.org/tkinterbook/grid.htm
"""
from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, socket
from threading import Thread
import tkinter as tk

""" Save connection information and open chat """
def enter_chat(event=None):
  try:
    HOST = host_val.get()
    if not HOST:
      raise ValueError('Host input is empty', 'host')

    PORT = port_val.get()
    if not PORT:
      PORT = 33000  # Default value
    else:
      PORT = int(PORT)

    NAME = name_val.get()
    if not NAME:
      raise ValueError('Name input is empty', 'name')

    ADDR = (HOST, PORT)
    client_socket.connect(ADDR)
    client_socket.send(bytes(NAME, "utf8"))

    receive_thread = Thread(target=receive)
    receive_thread.start()

    connection_window.withdraw()
    name_val.set("")
    host_val.set("")
    port_val.set("")
    name_label.config(text="Name: " + NAME)
    host_label.config(text="Host: " + HOST)
    port_label.config(text="Port: " + str(PORT))
    chat_window.deiconify()

  except OSError:
    show_error_popup("Error connecting. Please try again.")

  except ValueError as err:
    show_error_popup("Please enter a {0}".format(err.args[1]))

""" Error popup """
def show_error_popup(message):
  win = tk.Toplevel()
  win.wm_title("Retry")
  win.geometry("+{0}+{1}".format(screen_width, screen_height))

  message_label = tk.Label(win, text=message, fg="firebrick4")
  message_label.pack()

  okay_button = tk.Button(win, text="OK", command=win.destroy, bg="firebrick1", fg="white")
  okay_button.pack()

""" Handles receiving messages """
def receive():
  while True:
    try:
      msg = client_socket.recv(BUFF_SIZE).decode("utf8")
      msg_list.insert(tk.END, msg)

    except OSError: # Possibly, the client has left the chat
      break

""" Handles sending messages """
def send(event=None): # event is passed by binders
  msg = my_msg.get()
  my_msg.set("")  # Clears input field
  client_socket.send(bytes(msg, "utf8"))
  if msg == "\\quit":
    client_socket.close()
    root.destroy()

""" Called when closing the window """
def on_closing(event=None):
  my_msg.set("\\quit")
  send()
  quit

""" Define the server connection """
client_socket = socket(AF_INET, SOCK_STREAM, 0)
client_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
BUFF_SIZE = 1024

""" Define the GUI """
root = tk.Tk()
screen_width = int(root.winfo_screenwidth()/2 - root.winfo_reqwidth()/2)
screen_height = int(root.winfo_screenheight()/2 - root.winfo_reqheight()/2)
connection_width = 200
connection_height = 100
chat_width = 400
chat_height = 300
root.withdraw()

connection_window = tk.Toplevel(root)
connection_window.wm_title("Connection")
connection_window.protocol("WM_DELETE_WINDOW", quit)
connection_window.geometry("{0}x{1}+{2}+{3}".format(connection_width, connection_height, screen_width, screen_height))

conn_host_label = tk.Label(connection_window, text="Host: ")
host_val = tk.StringVar()
conn_host_entry = tk.Entry(connection_window, textvariable=host_val)
conn_host_entry.bind("<Return>", enter_chat)
conn_port_label = tk.Label(connection_window, text="Port: ")
port_val = tk.StringVar()
conn_port_entry = tk.Entry(connection_window, textvariable=port_val)
conn_port_entry.bind("<Return>", enter_chat)
conn_name_label = tk.Label(connection_window, text="Name: ")
name_val = tk.StringVar()
conn_name_entry = tk.Entry(connection_window, textvariable=name_val)
conn_name_entry.bind("<Return>", enter_chat)
conn_host_label.grid(row=0, column=0, sticky=tk.E)
conn_host_entry.grid(row=0, column=1)
conn_port_label.grid(row=1, column=0, sticky=tk.E)
conn_port_entry.grid(row=1, column=1)
conn_name_label.grid(row=2, column=0, sticky=tk.E)
conn_name_entry.grid(row=2, column=1)

conn_button_frame = tk.Frame(connection_window)
conn_ok_button = tk.Button(conn_button_frame, text="OK", command=enter_chat, bg="medium sea green", fg="white")
conn_ok_button.pack(side=tk.LEFT)
conn_quit_button = tk.Button(conn_button_frame, text="Quit", command=quit, bg="slateblue1", fg="white")
conn_quit_button.pack(side=tk.RIGHT)
conn_button_frame.grid(row=3, column=1)

chat_window = tk.Toplevel(root)
chat_window.withdraw()
chat_window.wm_title("Chitchat")
chat_window.protocol("WM_DELETE_WINDOW", on_closing)
chat_window.geometry("{0}x{1}+{2}+{3}".format(chat_width, chat_height, screen_width, screen_height))

messages_frame = tk.Frame(chat_window)
my_msg = tk.StringVar()  # For the messages to be sent
my_msg.set("Type your messages here.")
scrollbar = tk.Scrollbar(messages_frame) # To navigate through past messages
msg_list = tk.Listbox(messages_frame, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
msg_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
messages_frame.pack(fill=tk.X)

entry_frame = tk.Frame(chat_window)
entry_field = tk.Entry(entry_frame, textvariable=my_msg)
entry_field.bind("<Return>", send)
send_button = tk.Button(entry_frame, text="Send", command=send, bg="seagreen1")
entry_field.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
send_button.pack(side=tk.RIGHT)
entry_frame.pack(fill=tk.X, expand=True)

details_frame = tk.Frame(chat_window, bg="white")
name_label = tk.Label(details_frame, text="Name: ", bg="lemon chiffon")
host_label = tk.Label(details_frame, text="Host: ", bg="pale turquoise")
port_label = tk.Label(details_frame, text="Port: ", bg="light pink")
name_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
host_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
port_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
details_frame.pack(fill=tk.X, expand=True)

root.mainloop()
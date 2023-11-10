import os
import socket
import struct

# Input Prefix Strings
CLIENT_INPUT_IP_ADDRESS_PREFIX_STR  = "Input IP Address: "
CLIENT_INPUT_PORT_NUMBER_PREFIX_STR = "Input port number: "
CLIENT_INPUT_COMMAND_PREFIX_STR     = "Input command: "
CLIENT_INPUT_REPL_PREFIX_STR        = "client: "

# Header Strings
INITIALIZE_SOCKET_HEADER_STR        = "----------------------- Initialize Socket -----------------------"
INPUT_COMMAND_HEADER_STR            = "------------------------- Input Command -------------------------"
NEXT_COMMAND_HEADER_STR             = "------------------------- Next Command --------------------------"
POST_STRING_COMMAND_HEADER_STR      = "--------- Post String Command (Type a single '&' to end) --------"
GET_COMMAND_HEADER_STR              = "-------------------------- Get Command --------------------------"

# Message Strings
CONNECT_STATUS_STR                  = "Connect status: "
SEND_STATUS_STR                     = "Send status: "
RECEIVED_MESSAGE_STR                = "---Received messages---"
POST_FILE_ERROR_FILE_NOT_FOUND_MSG  = "Error: File not found"
CONNECTION_FAIL_NOT_BUILT_MSG       = "Error: Connection is not built, please try again"

# Utility Strings
DIVIDER_STR                         = "------"

# Size Constants
MAXIMUM_FILE_SIZE_IN_BYTES = 256
BUFFER_SIZE = 4096

class BulletinBoardCommands:
  @staticmethod
  def post_string(bulletin_board_client):
    bulletin_board_client.send('POST_STRING')

  @staticmethod
  def post_file(bulletin_board_client):
    bulletin_board_client.send('POST_FILE')

  @staticmethod
  def get(bulletin_board_client):
    bulletin_board_client.send('GET')

  @staticmethod
  def exit(bulletin_board_client):
    bulletin_board_client.send('EXIT')

class BulletinBoardClient:
  def __init__(self, host, port):
    self.host = host
    self.port = port
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  def initialize(self):
    self.socket.connect((self.host, self.port))

  def send(self, message):
    self.socket.send(bytes(message, encoding='utf-8'))

  def recv(self):
    return self.socket.recv(BUFFER_SIZE).decode('utf-8')

  def z_recv(self):
    return self.socket.recv(BUFFER_SIZE)
  
  def close(self):
    self.socket.close()

if __name__ == '__main__':
  print(INITIALIZE_SOCKET_HEADER_STR)
  ip_address = input(CLIENT_INPUT_IP_ADDRESS_PREFIX_STR)
  port_number = int(input(CLIENT_INPUT_PORT_NUMBER_PREFIX_STR))
  client_socket = BulletinBoardClient(ip_address, port_number)

  client_socket.initialize()

  firstCommand = True
  while True:
    if firstCommand:
      print(INPUT_COMMAND_HEADER_STR)
    else:
      print(NEXT_COMMAND_HEADER_STR)
    command = input(CLIENT_INPUT_COMMAND_PREFIX_STR)
  
    if command == 'POST_STRING':
      print(POST_STRING_COMMAND_HEADER_STR)
      client_socket.send(command)
      post_string_msg = ''
      message_count = 0;
      while (post_string_msg != '&'):
        post_string_msg = input(CLIENT_INPUT_REPL_PREFIX_STR)
        client_socket.send(post_string_msg)
        message_count += 1
        if (post_string_msg == '&'):
          print(client_socket.z_recv().decode('utf-8'))
          print(DIVIDER_STR)
          print(f'Sent {message_count} messages to (IP Address: {ip_address}, Port Number: {port_number})')
          print(DIVIDER_STR)
      firstCommand = False
      continue

    if command == 'POST_FILE':
      client_socket.send(command)
      print(client_socket.z_recv().decode('utf-8'))
      file_path = input(CLIENT_INPUT_REPL_PREFIX_STR)

      if not os.path.isfile(file_path):
        print('Error: File not found')
        client_socket.send('close')
        print(client_socket.z_recv().decode('utf-8'))
        firstCommand = False
        continue
        
      if os.stat(file_path).st_size > MAXIMUM_FILE_SIZE_IN_BYTES:
        print('Error: File size is too large')
        client_socket.send('close')
        print(client_socket.z_recv().decode('utf-8'))
        firstCommand = False
        continue

      file_header = struct.pack('128sl', bytes(file_path, encoding='utf-8'), os.stat(file_path).st_size)
      client_socket.socket.send(file_header)
      file = open(file_path, 'rb')
      file_data = file.read(MAXIMUM_FILE_SIZE_IN_BYTES)
      file.close()
      client_socket.socket.send(file_data)

      print(client_socket.z_recv().decode('utf-8'))
      firstCommand = False
      continue

    if command == 'GET':
      print(GET_COMMAND_HEADER_STR)
      print(RECEIVED_MESSAGE_STR)
      client_socket.send(command)
      get_string_msg = ''
      while (get_string_msg != 'server: &'):
        get_string_msg = client_socket.z_recv().decode('utf-8')
        print(get_string_msg)
        if (get_string_msg == 'server: &'):
          print (DIVIDER_STR)
          print (f'IP Address: {ip_address}, Port Number: {port_number}')
          print (DIVIDER_STR)
      firstCommand = False
      continue

    if command == 'EXIT':
      client_socket.send(command)
      print(client_socket.z_recv().decode('utf-8'))
      client_socket.close()
      break
    
    client_socket.send(command)
    print(client_socket.z_recv().decode('utf-8'))
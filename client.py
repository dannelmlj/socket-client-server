import os
import socket
import struct

# Input Prefix Strings
CLIENT_INPUT_IP_ADDRESS_PREFIX_STR = 'Input IP Address: '
CLIENT_INPUT_PORT_NUMBER_PREFIX_STR = 'Input port number: '
CLIENT_INPUT_COMMAND_PREFIX_STR = 'Input command: '
CLIENT_INPUT_REPL_PREFIX_STR = 'client: '

# Header Strings
INITIALIZE_SOCKET_HEADER_STR = '---------- Initialize Socket ----------'
INPUT_COMMAND_HEADER_STR = '---------- Input Command ----------'
NEXT_COMMAND_HEADER_STR = '---------- Next Command ----------'
POST_STRING_COMMAND_HEADER_STR = "---------- Post String Command (Type a single '&' to end) ----------"

# Utility Strings
ERROR_STR = 'Error: '
DIVIDER_STR = '------'
CONNECT_STATUS_STR = 'Connect status: '
SEND_STATUS_STR = 'Send status: '

# Message Strings
POST_FILE_ERROR_FILE_NOT_FOUND_MSG = 'Error: File not found'

BUFFER_SIZE = 4096

class ClientSocket:
  def __init__(self, host, port):
    self.host = host
    self.port = port
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.connect((self.host, self.port))
  
  def send(self, message):
    self.socket.send(bytes(message, encoding='utf-8'))

  def send_file(self, file_path):
    file_header = struct.pack('128sl', bytes(file_path, encoding='utf-8'), os.stat(file_path).st_size)
    self.socket.send(file_header)
    file = open(file_path, 'rb')
    file_data = file.read(256)
    file.close()
    self.socket.send(file_data)

  def recv(self):
    return self.socket.recv(BUFFER_SIZE)
  
  def close(self):
    self.socket.close()

if __name__ == '__main__':
  print(INITIALIZE_SOCKET_HEADER_STR)
  ip_address = input(CLIENT_INPUT_IP_ADDRESS_PREFIX_STR)
  port_number = int(input(CLIENT_INPUT_PORT_NUMBER_PREFIX_STR))
  client_socket = ClientSocket(ip_address, port_number)

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
          print(client_socket.recv().decode('utf-8'))
          print(DIVIDER_STR)
          print(f'Sent {message_count} messages to (IP Address: {ip_address}, Port Number: {port_number})')
          print(DIVIDER_STR)
      firstCommand = False
      continue

    if command == 'POST_FILE':
      client_socket.send(command)
      print(client_socket.recv().decode('utf-8'))
      file_path = input(CLIENT_INPUT_REPL_PREFIX_STR)

      if os.path.isfile(file_path):
        client_socket.send_file(file_path)
      else:
        client_socket.send(POST_FILE_ERROR_FILE_NOT_FOUND_MSG)

      print(client_socket.recv().decode('utf-8'))
      firstCommand = False
      continue

    if command == 'GET':
      continue

    if command == 'EXIT':
      client_socket.close()
      break
    
    client_socket.send(command)
    print(client_socket.recv().decode('utf-8'))
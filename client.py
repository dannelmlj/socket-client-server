import os
import socket
import struct
from constants import *
from commands import BulletinBoardCommands
class BulletinBoardClient:
  def __init__(self, host, port):
    self.host = host
    self.port = port
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.commands = BulletinBoardCommands(self)

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
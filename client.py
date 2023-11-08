import socket
# Input Prefix Strings
CLIENT_INPUT_IP_ADDRESS_PREFIX_STR = ' Input IP Address: '
CLIENT_INPUT_PORT_NUMBER_PREFIX_STR = ' Input port number: '
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

BUFFER_SIZE = 4096

class ClientSocket:
  def __init__(self, host, port):
    self.host = host
    self.port = port
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.connect((self.host, self.port))
  
  def send(self, message):
    self.socket.send(bytes(message, encoding='utf-8'))

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
      #TODO: implement
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
          print (DIVIDER_STR)
          print (f'Sent {message_count} messages to (IP Address: {ip_address}, Port Number: {port_number})')
          print (DIVIDER_STR)
      firstCommand = False
      continue
    elif command == 'POST_FILE':
      #TODO: implement
      continue
    elif command == 'GET':
      #TODO: implement
      continue
    elif command == 'EXIT':
      client_socket.close()
    else:
      client_socket.send(command)
      print(client_socket.recv().decode('utf-8'))
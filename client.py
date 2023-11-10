import os
import socket
import struct

'''
  Constants
'''
# Input Prefix Strings
CLIENT_INPUT_IP_ADDRESS_PREFIX_STR  = "Input IP Address: "
CLIENT_INPUT_PORT_NUMBER_PREFIX_STR = "Input port number: "
CLIENT_INPUT_COMMAND_PREFIX_STR     = "Input command: "
CLIENT_INPUT_REPL_PREFIX_STR        = "client: "

# Header Strings
HEADER_INITIALIZE_SOCKET_STR        = "----------------------- Initialize Socket -----------------------"
HEADER_INPUT_COMMAND_STR            = "------------------------- Input Command -------------------------"
HEADER_NEXT_COMMAND_STR             = "------------------------- Next Command --------------------------"
HEADER_POST_STRING_COMMAND_STR      = "--------- Post String Command (Type a single '&' to end) --------"
HEADER_GET_COMMAND_STR              = "-------------------------- Get Command --------------------------"

# Utility Strings
DIVIDER_STR                         = "------"
CONNECT_STATUS_STR                  = "Connect status: "
SEND_STATUS_STR                     = "Send status: "
RECEIVED_MESSAGE_STR                = "---Received messages---"

# Error Strings
ERROR_POST_FILE_FILE_NOT_FOUND_STR  = "Error: File not found"
ERROR_POST_FILE_SIZE_EXCEED_STR     = "Error: File size exceeds the maximum file size"
ERROR_CONNECTION_FAIL_STR           = "Error: Connection is not built, please try again"


# Size Constants
MAXIMUM_FILE_SIZE_IN_BYTES          = 256
BUFFER_SIZE                         = 4096

# Command Constants
POST_STRING_COMMAND                 = 'POST_STRING'
POST_FILE_COMMAND                   = 'POST_FILE'
GET_COMMAND                         = 'GET'
EXIT_COMMAND                        = 'EXIT'

class BulletinBoardCommands:

  @staticmethod
  def post_string(bulletin_board_client):
    ''' POST_STRING command.
        This command allows client to send a text file to the server line by line. 
        The client must type the text (using the standard input) line-by-line. 
        The first line is the command itself (i.e. POST_STRING) and subsequent lines are treated as the text. 
        The end of the text input is signalled by  a special symbol  &. 

        Keyword arguments:
        bulletin_board_client -- BulletinBoardClient object to send the message to the server through the socket
    '''
    bulletin_board_client.send(POST_STRING_COMMAND)
    print(HEADER_POST_STRING_COMMAND_STR)
    post_string_msg = ''
    message_count = 0
    while (post_string_msg != '&'):
      post_string_msg = input(CLIENT_INPUT_REPL_PREFIX_STR)
      bulletin_board_client.send(post_string_msg)
      message_count += 1
      if (post_string_msg == '&'):
        send_status = bulletin_board_client.recv()
        print(send_status)
        print(DIVIDER_STR)
        print(f'Sent {message_count} messages to (IP Address: {bulletin_board_client.host}, Port Number: {bulletin_board_client.port})')
        print(f'{CONNECT_STATUS_STR}OK') if send_status == 'server: OK' else print(f'{CONNECT_STATUS_STR}ERROR')
        print(f'{SEND_STATUS_STR}OK') if send_status == 'server: OK' else print(f'{SEND_STATUS_STR}ERROR')
        print(DIVIDER_STR)

  @staticmethod
  def post_file(bulletin_board_client):
    ''' POST_FILE command.
        This command allows client to send a text file to the server.
        The client will supply the file path and the server will read the file and store it in the server side.

        Keyword arguments:
        bulletin_board_client -- BulletinBoardClient object to send the message to the server through the socket
    '''
    bulletin_board_client.send(POST_FILE_COMMAND)
    print(bulletin_board_client.recv())

    file_path = input(CLIENT_INPUT_REPL_PREFIX_STR)
    file_size = os.stat(file_path).st_size
    file_header = struct.pack('128sl', bytes(file_path, encoding='utf-8'), file_size)

    if not os.path.isfile(file_path):
      print(ERROR_POST_FILE_FILE_NOT_FOUND_STR)
      bulletin_board_client.send('close')
      print(bulletin_board_client.recv())
      return
    
    if file_size > MAXIMUM_FILE_SIZE_IN_BYTES:
      print(ERROR_POST_FILE_SIZE_EXCEED_STR)
      bulletin_board_client.send('close')
      bulletin_board_client.recv()
      return
    
    bulletin_board_client.socket.send(file_header)
    with open(file_path, 'rb') as file:
      file_data = file.read(MAXIMUM_FILE_SIZE_IN_BYTES)
      bulletin_board_client.socket.send(file_data)

    print(bulletin_board_client.recv())

  @staticmethod
  def get(bulletin_board_client):
    ''' GET command.
        This command will ask the server to send all previously posted messages (posted by POST_STRING command) by the client and other clients.
        Outputs all the messages received from the server line by line.
        
        Keyword arguments:
        bulletin_board_client -- BulletinBoardClient object to receive the message from the server through the socket
    '''
    bulletin_board_client.send(GET_COMMAND)
    print(HEADER_GET_COMMAND_STR)
    print(RECEIVED_MESSAGE_STR)
    get_string_msg = ''
    while (get_string_msg != 'server: &'):
      get_string_msg = bulletin_board_client.recv()
      print(get_string_msg)
      if (get_string_msg == 'server: &'):
        print(DIVIDER_STR)
        print(f'IP Address: {bulletin_board_client.host}, Port Number: {bulletin_board_client.port}')
        print(f'{CONNECT_STATUS_STR}OK')
        print(f'{SEND_STATUS_STR}OK')
        print(DIVIDER_STR)

  @staticmethod
  def exit(bulletin_board_client):
    ''' EXIT command.
        This command will ask the server to close the connection.
        Outputs the server response.

        Keyword arguments:
        bulletin_board_client -- BulletinBoardClient object to send the exit command and receive the response from the server through the socket
    '''
    bulletin_board_client.send(EXIT_COMMAND)
    print(bulletin_board_client.recv())
    bulletin_board_client.close()

  @staticmethod
  def unknown(bulletin_board_client, command):
    ''' UNKNOWN command.
        This is a utility function to handle unknown commands.

        Keyword arguments:
        bulletin_board_client -- BulletinBoardClient object to send the unknown command and receive the response from the server through the socket
        command -- the unknown command
    '''
    bulletin_board_client.send(command)
    print(bulletin_board_client.recv())

class BulletinBoardClient:
  def __init__(self, host, port):
    self.host = host
    self.port = port
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  def initialize(self):
    self.socket.connect((self.host, self.port))

  def send(self, message):
    self.socket.sendall(message.encode())

  def recv(self):
    return self.socket.recv(BUFFER_SIZE).decode()
  
  def close(self):
    self.socket.close()

def main():
  connection_established = False
  while not connection_established:
    try:
      print(HEADER_INITIALIZE_SOCKET_STR)
      ip_address = input(CLIENT_INPUT_IP_ADDRESS_PREFIX_STR)
      port_number = int(input(CLIENT_INPUT_PORT_NUMBER_PREFIX_STR))

      client_socket = BulletinBoardClient(ip_address, port_number)
      client_socket.initialize()

      connection_established = True
    except Exception:
      print(ERROR_CONNECTION_FAIL_STR)
    
  sent_commands = 0
  while True:
    if not sent_commands:
      print(HEADER_INPUT_COMMAND_STR)
    else:
      print(HEADER_NEXT_COMMAND_STR)

    command = input(CLIENT_INPUT_COMMAND_PREFIX_STR)
    sent_commands += 1

    if command == POST_STRING_COMMAND:
      BulletinBoardCommands.post_string(client_socket)
    elif command == POST_FILE_COMMAND:
      BulletinBoardCommands.post_file(client_socket)
    elif command == GET_COMMAND:
      BulletinBoardCommands.get(client_socket)
    elif command == EXIT_COMMAND:
      BulletinBoardCommands.exit(client_socket)
      break
    else:
      BulletinBoardCommands.unknown(client_socket, command)

if __name__ == '__main__':
  main()
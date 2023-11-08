import socket

CLIENT_REPL_PREFIX_STR = 'client: '
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
  client_socket = ClientSocket('172.27.160.121', 16011)

  while True:
    command = input(CLIENT_REPL_PREFIX_STR)
    
    if command == 'POST_STRING':
      #TODO: implement
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
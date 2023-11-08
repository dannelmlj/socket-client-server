import socket

class ClientSocket:
  def __init__(self, host, port):
    self.host = host
    self.port = port
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.connect((self.host, self.port))

  def send(self, msg):
    self.socket.send(bytes(msg, encoding='utf-8'))

  def recv(self):
    return self.socket.recv(4096)
  
  def close(self):
    self.socket.close()

if __name__ == '__main__':
  client = ClientSocket('localhost', 16011)
  while True:
    msg = input('')
    client.send(msg)
    print(client.recv().decode('utf-8'))
    if msg == 'EXIT':
      client.close()
      break
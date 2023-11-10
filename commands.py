from enum import Enum

class Commands(Enum):
  POST_STRING = 'POST_STRING'
  POST_FILE = 'POST_FILE'
  GET = 'GET'
  EXIT = 'EXIT'

class BulletinBoardCommands:
  def __init__(self, client_socket):
    self.client_socket = client_socket

  def post_string(self):
    self.client_socket.send(Commands.POST_STRING.value)
    pass

  def post_file(self):
    self.client_socket.send(Commands.POST_FILE.value)
    pass

  def get(self):
    self.client_socket.send(Commands.GET.value)
    pass

  def exit(self):
    self.client_socket.send(Commands.EXIT.value)
    pass
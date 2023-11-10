==================================
Bulletin Board Client 
==================================

Introduction
------------

This is an implementation of the Client Bulletin Board for a client-server application.


Usage
-----

Clients can communicate with the server through issuing different commands. 
Commands supported are:
  - POST_STRING: 
        This command allows client to send a text file to the server line by line. 
        The client must type the text (using the standard input) line-by-line. 
        The first line is the command itself (i.e. POST_STRING) and subsequent lines are treated as the text. 
        The end of the text input is signalled by  a special symbol  &
  - POST_FILE:

  - GET:
        This command will ask the server to send all previously posted messages (posted by POST_STRING command) by the client and other clients.
        Outputs all the messages received from the server line by line.
  - EXIT:
        This command will ask the server to close the connection.
        Then outputs the server response

The server runs on a specified port and supports 4 commands issued by the client: POST_STRING, POST_FILE, GET, and EXIT


Configuration
-------------

1. Run the server.py file using the command: python3 server.py
2. Run the client.py file using the command: python3 client.py

If the server is run in the same computer then:
3a. Input 'localhost' as the IP Address
else
3b. Input the IP Address of the computer running the server.py as the IP Address. Note that both computers need to be in the same network

4. Input 16011 as the port number
5. Input the 4 supported commands name to use it's respective functionality.

Authors
-------

Dannel MULJA --- 56684326
Enryl EINHARD --- 56731436

Contact
-------

dmulja2-c@my.cityu.edu.hk
eenone2-c@my.cityu.edu.hk
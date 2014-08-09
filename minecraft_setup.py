import socket

# Assume script is run from inside Minecraft server folder
hostname = socket.gethostname()
file = open('ops.txt', 'a')
file.write(hostname + "\n")

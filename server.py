import socket
import sys
import time
from Crypto.Cipher import DES3
from Crypto import Random

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #creates a socket object
#AF_INET is address family for IPv4, SOCK_STREAM is socket type for TCP
host='127.0.0.1' #host will be this system
print("Server will start on host: ",host)
port=65342 #Posrt to listen on
s.bind((host,port)) #bind the socket with host and port
print("Server done binding to host and port")
#Server is now listening to the incomming connections 
s.listen() #enables server to acept() connetions- here 1 connection
conn,addr=s.accept() #conn has socket and addr has ip address comming from client

key=conn.recv(1024) #Receiving key from client

with conn:
    #----GENERATING IV FOR CBC MODE OF ENCRYPTION------ 
    iv=Random.new().read(DES3.block_size) #initialize initialization vector(iv) randomly for mode CBC ,i.e., 8 block size
    #Sending IV to client
    conn.send(iv)
    print(addr," has connected to the server now")#print host-name or ip address of client 
    while 1:
        #Making Encrypting Object
        cipher_des3=DES3.new(key,DES3.MODE_CBC,iv) #encrypying object
        message=input(str("-->")) #input message
        while len(message)%8!=0:#length of plaintext must be multiple of 8, to make it suitable for CBC mode
            message+=" "
        message=cipher_des3.encrypt(message.encode('utf-8')) #Encrypt message with 3-des
        conn.send(message) #sending message to client

        #Making Decrypting Object
        decipher_des3=DES3.new(key,DES3.MODE_CBC,iv) #Decrypting Object
        inc_msg=conn.recv(1024) #receiving message from client
        inc_msg=decipher_des3.decrypt(inc_msg) #decryption is done here
        inc_msg=inc_msg.decode('utf-8') #Bytes to ascii conversion
        print("Client: ",inc_msg)
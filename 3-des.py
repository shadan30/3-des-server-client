from Crypto.Cipher import DES3
from Crypto import Random

#----GENERATING KEY & IV---------
k=Random.get_random_bytes(24) # 24x8=192bits 
#to adjust parity bits the key size must be 16 or 24 bytes
print("key taken=",k,"length=",len(k)) 
key=DES3.adjust_key_parity(k) #setting parity bits for 3-des
print("key after parity drop=",key,"length=",len(key)) 
iv=Random.new().read(DES3.block_size) #initialize initialization vector(iv) randomly for mode CBC ,i.e., 8 block size

#-----ENCRYPTION------
#making an object for encryption in CBC
cipher_des3=DES3.new(key,DES3.MODE_CBC,iv)
p=input(str("Enter plaintext: "))
while len(p)%8!=0:#length of plaintext must be multiple of 8, to make it suitable for CBC mode
    p+=" "
enc_text=cipher_des3.encrypt(p.encode('utf-8')) # .encode() is used to convert string to byte stream
print("encypted text = ",enc_text)

#------DECRYPTION-------
print("Decryption.....")
#making decryption object 
decipher_des3=DES3.new(key,DES3.MODE_CBC,iv)
dec_text=decipher_des3.decrypt(enc_text)
print("decypted text = ",dec_text.decode('utf-8')) # we used str() because output is in bytes
#we used .decode() to convert bytes to string
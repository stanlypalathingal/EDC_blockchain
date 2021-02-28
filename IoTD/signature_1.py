import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import base64

def encrypt(rsa_publickey,plain_text):
     cipher_text=rsa_publickey.encrypt(plain_text,32)[0]
     b64cipher=base64.b64encode(cipher_text)
     return b64cipher

def decrypt(rsa_privatekey,b64cipher):
     decoded_ciphertext = base64.b64decode(b64cipher)
     plaintext = rsa_privatekey.decrypt(decoded_ciphertext)
     return plaintext

def rsakeys():  
     length=2048  
     privatekey = RSA.generate(length, Random.new().read)  
     publickey = privatekey.publickey()  
     return privatekey, publickey

#create and save keys
# private_key,public_key=rsakeys() #generating keys

# with open('edc_pvt_key.pem', 'wb') as f:
#         f.write(private_key.exportKey('PEM'))
        
# with open('edc_pub_key.pem', 'wb') as f:
#         f.write(public_key.exportKey('PEM'))

# with open('edc_pvt_key.pem', 'r') as f:
#     private_key = RSA.importKey(f.read())

# with open('edc_pub_key.pem', 'r') as f:
#     public_key = RSA.importKey(f.read())

# text=b"""This is trial to find the lenght which can be encrypted and decrypted using RSA! \
#        This is trial to find the lenght which can be encrypted and decrypted using RSA! 
#       """ #Text to encrypt
# ct=encrypt(public_key,text)
# # print(ct)
# decrypt(private_key,ct) #decryption

# def sign(privatekey,data):
#     return base64.b64encode(str((privatekey.sign(data,''))[0]).encode())
# def verify(publickey,data,sign):
#      return publickey.verify(data,(int(base64.b64decode(sign)),))


# a=sign(private_key,text)
# # a="123"
# result=verify(public_key,text,a)

# print(result)

private_key,public_key=rsakeys() #generating keys

with open('edc_pvt_3.pem', 'wb') as f:
        f.write(private_key.exportKey('PEM'))
        
with open('edc_pub_3.pem', 'wb') as f:
        f.write(public_key.exportKey('PEM'))

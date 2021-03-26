import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import base64

def rsakeys():  
     length=2048  
     privatekey = RSA.generate(length, Random.new().read)  
     publickey = privatekey.publickey()  
     return privatekey, publickey

#create and save keys
private_key,public_key=rsakeys() #generating keys

with open('edc_pvt_key_5.pem', 'wb') as f:
        f.write(private_key.exportKey('PEM'))
        
with open('edc_pub_key_5.pem', 'wb') as f:
        f.write(public_key.exportKey('PEM'))


import paho.mqtt.subscribe as sub
import paho.mqtt.publish as pb

import pandas as pd
import datetime as dtm
import sys
import time

import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import base64
import hashlib 

HOST = sys.argv[1]
no_of_EDC = sys.argv[2]
PORT = 1883
topic = "encrypted_edc"+str(no_of_EDC)
print("This is EDC number  : ",no_of_EDC)
signature = b'dummy154value'
previous_message = previous_hash = ""
i=False

f = open("data/test.csv", "w")
f.truncate()
f.close()

with open('edc_pvt_'+str(no_of_EDC)+'.pem', 'r') as f:
    private_key = RSA.importKey(f.read())

def decrypt(rsa_privatekey,b64cipher):
     decoded_ciphertext = base64.b64decode(b64cipher)
     plaintext = rsa_privatekey.decrypt(decoded_ciphertext)
     return plaintext

def on_message_print(client, userdata, message):
    global i, previous_hash, previous_message
    # global i

    mess_bytes=(decrypt(private_key,(message.payload)))
    print(mess_bytes)

    mess=mess_bytes.decode("utf-8")
    with open('data/test.csv','a+') as f:
        f.write("\n"+str(mess))
        if i==True:
            hash_message = previous_message + previous_hash
            print(hash_message)
            result = hashlib.md5(hash_message.encode())
            hashed_value = result.hexdigest()
            f.write(hashed_value+"\n")
            print(hashed_value)   
            previous_hash = hashed_value
    f.close()
    previous_message = mess
   
    i=True
    print("\n")    

sub.callback(on_message_print, [topic], hostname=HOST, port=PORT)

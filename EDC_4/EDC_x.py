import paho.mqtt.subscribe as sub
import paho.mqtt.publish as pb

import pandas as pd
import datetime as dtm
import sys
import time

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from Crypto.Hash import SHA1
from Crypto.Signature import pkcs1_15
import hashlib 

HOST = sys.argv[1]
no_of_EDC = sys.argv[2]
PORT = 1883
topic = "encrypted_edc"+str(no_of_EDC)
print("This is EDC number  : ",no_of_EDC)
signature = b'dummy154value'
previous_message = previous_hash = ""
i=False

f = open("data/data_"+no_of_EDC+".csv", "w+")
f.truncate()
f.close()

def publishResult(value,publish_topic):
    pb.single(publish_topic, value, 0, False, HOST, PORT)

with open('data/edc_pvt_'+str(no_of_EDC)+'.pem', 'r') as f:
    private_key = RSA.importKey(f.read())

def decrypt(key,data):
    decipher = Cipher_PKCS1_v1_5.new(key)
    return decipher.decrypt(data, None).decode()

def on_message_print(client, userdata, message):
    global i, previous_hash, previous_message
    mess =(decrypt(private_key,(message.payload)))
    print(mess)

    with open("data/data_"+no_of_EDC+".csv",'a+') as f:
        f.write("\n"+str(mess))
        if i==True:
            hash_message = previous_message + previous_hash
            # print(hash_message)
            result = hashlib.sha256(hash_message.encode())
            hashed_value = result.hexdigest()
            f.write(hashed_value+"\n")
            publishResult(str(dtm.datetime.now()),"end_time")
            print(hashed_value)   
            previous_hash = hashed_value
    f.close()
    previous_message = mess
   
    i=True

sub.callback(on_message_print, [topic], hostname=HOST, port=PORT)

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

HOST = sys.argv[1]
no_of_EDC = sys.argv[2]
PORT = 1883

# mqtt_host = sys.argv[1]
signature = b'dummy154value'
print("This is the Verifier")

with open('edc_pvt_key.pem', 'r') as f:
    private_key = RSA.importKey(f.read())

with open('iotd_pub_key.pem', 'r') as f:
    public_key = RSA.importKey(f.read())

with open('edc_pub_1.pem', 'r') as f:
    public_key1 = RSA.importKey(f.read())

with open('edc_pub_2.pem', 'r') as f:
    public_key2 = RSA.importKey(f.read())

with open('edc_pub_3.pem', 'r') as f:
    public_key3 = RSA.importKey(f.read())

def decrypt(rsa_privatekey,b64cipher):
     decoded_ciphertext = base64.b64decode(b64cipher)
     plaintext = rsa_privatekey.decrypt(decoded_ciphertext)
     return plaintext

def verify(publickey,data,sign):
     return publickey.verify(data,(int(base64.b64decode(sign)),))

def publishResult(value,publish_topic):
    # host=mqtt_host 
    port=1883
    pb.single(publish_topic, value, 0, False, HOST, port)

def on_message_print(client, userdata, message):
    if message.topic == "signature":
        global signature 
        signature = message.payload
        
    elif message.topic == "encrypted":
        #print(mess)
        global no_of_EDC
        mess_encrypted = message.payload
        mess=(decrypt(private_key,(message.payload)))
        print(mess)
        validity=verify(public_key,mess,signature)

        if validity==True:
            mess=mess.decode("utf-8")
            with open('data/test.csv','a+') as f:
                f.write("\n"+str(mess))
            f.close()
            for x in range(1,int(no_of_EDC)+1):
                publishResult(mess_encrypted,"encrypted_edc"+str(x))
            print("valid signature")
        else:
            print("invalid signature")
        print("\n")    

sub.callback(on_message_print, ["encrypted", "signature"], hostname=HOST, port=PORT)

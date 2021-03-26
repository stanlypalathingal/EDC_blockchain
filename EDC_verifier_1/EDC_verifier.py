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
signature = b'dummyvalue'
print("This is the Verifier 1 and send data to  "+ no_of_EDC + "  EDC" )

with open('data/edc_pvt_key_1.pem', 'r') as f:
    private_key = RSA.importKey(f.read())

with open('data/iotd_pub_key.pem', 'r') as f:
    public_key_iotd = RSA.importKey(f.read())

def encrypt(rsa_publickey,plain_text):
     cipher_text=rsa_publickey.encrypt(plain_text,32)[0]
     b64cipher=base64.b64encode(cipher_text)
     return b64cipher

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
        
    elif message.topic == "encrypted_1":
        # print(mess)
        global no_of_EDC
        # mess_encrypted = message.payload
        mess=(decrypt(private_key,(message.payload)))
        print(mess)
        validity=verify(public_key_iotd,mess,signature)

        if validity==True:
            publishResult(str(dtm.datetime.now()),"verify_time")
            mess=mess.decode("utf-8")
            
            for x in range(1,int(no_of_EDC)+1):
                try:
                    with open('data/edc_pub_'+str(x)+'.pem', 'r') as f:
                        public_key = RSA.importKey(f.read())
                    mess_encrypted = encrypt(public_key,mess.encode())
                    publishResult(mess_encrypted,"encrypted_edc"+str(x))
                except:
                    print("\n there are only "+str (x-1)+" pairs. kindly change the number to "+str (x-1))
                    print("\n or add new public - private key pairs")
                    sys.exit()
            print("valid signature")
        else:
            print("invalid signature")
        print("\n")    

sub.callback(on_message_print, ["encrypted_1", "signature"], hostname=HOST, port=PORT)

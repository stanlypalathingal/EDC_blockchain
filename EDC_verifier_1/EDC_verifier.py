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

from Crypto_Puzzle import cipher_de

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

def encrypt(key,data):
    cipher = Cipher_PKCS1_v1_5.new(key)
    return cipher.encrypt(data.encode())

def decrypt(key,data):
    decipher = Cipher_PKCS1_v1_5.new(key)
    return decipher.decrypt(data, None).decode()

def verify(pub,message,signature):
    h = SHA1.new()
    h.update(message.encode())
    try:
        pkcs1_15.new(pub).verify(h, signature)
        publishResult(str(dtm.datetime.now()),"verify_time")
        return True
    except (ValueError, TypeError):
        return False

def publishResult(value,publish_topic):
    # host=mqtt_host 
    port=1883
    pb.single(publish_topic, value, 0, False, HOST, port)

def on_message_print(client, userdata, message):
    if message.topic == "signature":
        global signature 
        signature = message.payload
        
    elif message.topic == "encrypted_1":
        global no_of_EDC
        mess=(decrypt(private_key,(message.payload)))

        validity=verify(public_key_iotd,mess,signature)
        mess=cipher_de(mess,4)
        print(mess)
        publishResult(str(dtm.datetime.now()),"puzzle_time")

        if validity==True:

            for x in range(1,int(no_of_EDC)+1):
                try:
                    with open('data/edc_pub_'+str(x)+'.pem', 'r') as f:
                        public_key = RSA.importKey(f.read())
                    mess_encrypted = encrypt(public_key,mess)
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

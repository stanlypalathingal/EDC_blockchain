import pandas as pd
import time
import sys
from csv import reader
import paho.mqtt.client as mqtt
import paho.mqtt.publish as pb

import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import base64

mqtt_host=sys.argv[1]

number_of_rows = 0
df=pd.read_csv("data/test_data.csv")

def publishResult(value,publish_topic):
    host=mqtt_host 
    port=1883
    pb.single(publish_topic, value, 0, False, host, port)

def prepareForPublish1(fileName,publish_topic):
    with open(fileName, 'rb') as f:
        data = f.read()
    print(data)
    cipher_text =encrypt(public_key,data)
    signature = sign(private_key,data)

    publishResult(signature,"signature")
    publishResult(cipher_text,"encrypted")
    print("\n")
    time.sleep(10)
    
def sign(privatekey,data):
    return base64.b64encode(str((privatekey.sign(data,''))[0]).encode())

def encrypt(rsa_publickey,plain_text):
     cipher_text=rsa_publickey.encrypt(plain_text,32)[0]
     b64cipher=base64.b64encode(cipher_text)
     return b64cipher

def decrypt(rsa_privatekey,b64cipher):
     decoded_ciphertext = base64.b64decode(b64cipher)
     plaintext = rsa_privatekey.decrypt(decoded_ciphertext)
     return plaintext

with open('data/iotd_pvt_key.pem', 'r') as f:
    private_key = RSA.importKey(f.read())

with open('data/edc_pub_key.pem', 'r') as f:
    public_key = RSA.importKey(f.read())

while(True):
    start3 = time.time()
    a=0
    b=3
    for x in range(0,(int(df.shape[0]/3))):
        df[a:b].to_csv("data/sub_test.csv",mode='w+',index=False,header= None)
        prepareForPublish1("data/sub_test.csv","usbdata_EDC")
        a=a+3
        b=b+3

    print("send to EDC")
    end3 = time.time()
    print(end3-start3)

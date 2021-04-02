import pandas as pd
import time
import sys
from csv import reader
import paho.mqtt.client as mqtt
import paho.mqtt.publish as pb
import threading
from subprocess import call
import datetime as dtm

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from Crypto.Hash import SHA1
from Crypto.Signature import pkcs1_15

from Crypto_Puzzle import cipher_en

mqtt_host=sys.argv[1]

number_of_rows = 0
df=pd.read_csv("data/test_data.csv")

class subscribe(threading.Thread):
    def run(self):
        call(["python3", "Subscribe.py",mqtt_host])
subs = subscribe()
subs.start()

f = open("benchmark/overall_time.csv", "w+")
f.truncate()
f.close()
f = open("benchmark/puzzle_time.csv", "w+")
f.truncate()
f.close()
f = open("benchmark/verification_time.csv", "w+")
f.truncate()
f.close()

def publishResult(value,publish_topic):
    host=mqtt_host 
    port=1883
    pb.single(publish_topic, value, 0, False, host, port)

def prepareForPublish1(fileName,publish_topic):
    with open(fileName, 'rb') as f:
        data = f.read()
    print(data)
    
    f=open('data/puzzle_time.txt',"w+")
    f.write(str(dtm.datetime.now()))
    f.close()
    data = cipher_en(data.decode("utf-8"),4)

    cipher_text_1 = encrypt(public_key_1,data)

    f=open('data/e_time.txt',"w+")
    f.write(str(dtm.datetime.now()))
    f.close()
    signature = sign(private_key,data)

    publishResult(signature,"signature")
    publishResult(cipher_text_1,"encrypted_1")
    
    print("\n")
    time.sleep(10)
    overall_time = open("benchmark/overall_time.csv","a+")
    overall_time.write("\n")
    overall_time.close()

def encrypt(key,data):
    cipher = Cipher_PKCS1_v1_5.new(key)
    return cipher.encrypt(data.encode())

def sign(pvt,message):
    digest = SHA1.new()
    digest.update(message.encode())
    signer = pkcs1_15.new(pvt)
    signature = signer.sign(digest)
    return signature

with open('data/iotd_pvt_key.pem', 'r') as f:
    private_key = RSA.importKey(f.read())

with open('data/edc_pub_key_1.pem', 'r') as f:
    public_key_1 = RSA.importKey(f.read())

while(True):
    start3 = time.time()
    a=0
    b=3
    for x in range(0,(int(df.shape[0]/3))):
        f=open('data/o_time.txt',"w+")
        f.write(str(dtm.datetime.now()))
        f.close()
        df[a:b].to_csv("data/sub_test.csv",mode='w+',index=False,header= None)
        prepareForPublish1("data/sub_test.csv","usbdata_EDC")
        a=a+3
        b=b+3

    print("send to EDC")
    end3 = time.time()
    print(end3-start3)

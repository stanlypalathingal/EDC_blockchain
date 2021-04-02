import paho.mqtt.subscribe as sub
import pandas as pd
import datetime as dtm
import sys
import time

HOST = sys.argv[1]
PORT = 1883

encrypt_time=0
def on_message_print(client, userdata, message):
    
    if message.topic== "end_time":
        end_time=message.payload.decode("utf-8")
        end_time=dtm.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S.%f')

        a = open('data/o_time.txt').read().replace('\n', '')
        a = pd.to_datetime(a, infer_datetime_format=True)
        c = (end_time - a)

        overall_time = open("benchmark/overall_time.csv","a+")
        overall_time.write(str(c.total_seconds())+"\n")
        overall_time.close()
        
    elif message.topic== "verify_time":
        verify_time=message.payload.decode("utf-8")
        verify_time=dtm.datetime.strptime(verify_time, '%Y-%m-%d %H:%M:%S.%f')

        b = open('data/e_time.txt').read().replace('\n', '')
        b = pd.to_datetime(b, infer_datetime_format=True)
        d = (verify_time - b)

        verification_time = open("benchmark/verification_time.csv","a+")
        verification_time.write(str(d.total_seconds())+"\n")
        verification_time.close()

    elif message.topic== "puzzle_time":
        puzzle_time=message.payload.decode("utf-8")
        puzzle_time=dtm.datetime.strptime(puzzle_time, '%Y-%m-%d %H:%M:%S.%f')

        b = open('data/puzzle_time.txt').read().replace('\n', '')
        b = pd.to_datetime(b, infer_datetime_format=True)
        d = (puzzle_time - b)

        puzzle_time = open("benchmark/puzzle_time.csv","a+")
        puzzle_time.write(str(d.total_seconds())+"\n")
        puzzle_time.close()

sub.callback(on_message_print, ["end_time","verify_time","puzzle_time"], hostname=HOST, port=PORT)

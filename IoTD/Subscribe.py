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
        
    # elif message.topic== "decrypt_time":
    #     global number_of_records
    #     #print(message.payload.decode("utf-8"))
    #     number_of_records=message.payload.decode("utf-8")
    #     f=open('data/time.txt',"w+")
    #     f.write(str(dtm.datetime.now()))
    #     f.close()

    # elif message.topic == "usbdata_EDC":
    #     mess=(KIE.decrypt(message.payload)).decode("utf-8")
    #     #print(mess)
    #     with open('data/test.csv','a+') as f:
    #         if(operator.contains(mess,"done")):
    #             #print("All data written to file")
    #             mess=""
    #             a = open('data/time.txt').read().replace('\n', '')
    #             a = pd.to_datetime(a, infer_datetime_format=True)
    #             c = (dtm.datetime.now() - a)
    #             print("Time taken for decrypt  ", c.total_seconds())
    #             decrypt_bench = open("/benchmarking/decrypt_benchmark.csv","a+")
    #             decrypt_bench.write(str(number_of_records)+" , "+str(c.total_seconds())+"\n")
    #             decrypt_bench.close()
                
    #             encrypt_bench = open("/benchmarking/encrypt_benchmark.csv","a+")
    #             encrypt_bench.write(str(number_of_records)+" , "+str(encrypt_time)+"\n")
    #             encrypt_bench.close()
    #         f.write("\n"+str(mess))
    #     f.close()
            
sub.callback(on_message_print, ["end_time","verify_time"], hostname=HOST, port=PORT)

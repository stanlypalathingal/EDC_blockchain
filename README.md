## There are two ways in which the simulator can work 
### 1. Executing as a Python3 program
In order to execute as a python3 program one need to install three packages

a. pandas

b. pycrypto

c. paho-mqtt


To run the system locate the files in the respective folders and run the commands as follows.
all these must be executed in separete terminals
```bash
python3 iotd_data_generators.py 192.168.1.228 
python3 EDC_verifier.py 192.168.1.228 3
python3 EDC_x.py 192.168.1.228 1
python3 EDC_x.py 192.168.1.228 2
python3 EDC_x.py 192.168.1.228 3
```
* **192.168.1.228** refers to the MQTT broker. 
* **3** in the second command refers to 3 systems to which the data would be sent.
* The sucessive 1,2 and 3 are the 3 systems. 
* The received data can be viewed in the **data** folder under the name **test.csv**
* If anyone would like to increse the number of systems, then the next number should be 4 and so on.
### 2. Executing as docker containers
It requires Docker to be installed in the system and must be able to download 5 images from www.dockerhub.com 

There are two sets of images given here. One is designed to work in the normal ubuntu platform and the other is designed to work on Raspberry Pi. One can mix these entities and execute like IoTD in Cloud (ubuntu) and the rest on Raspberry Pi. The fiel to build the docker image (Dockerfile) contains the Python versions required to build in both cloud and Raspberrypi environments.


The present set up has only 3 EDC. In order to increse the number of EDC one need to create a public / privated key pairs using the file named "RSA_key_generators.py" and save with ordinal status of EDC. For example, there are three systems and if someone wants to add one more, then the number must be 4 and so on. 
* The names of public / private key pairs of the 4th EDC must be "edc_pvt_4.pem" and "edc_pub_4.pem". One must follow this pattern when a new EDC is added. 

* The public-key must be place in the "data" directory of EDC_verifier and private-key must be in the placed in the respective "data" directory of EDC_x.

* Each of these entities must run parallely in different systems or in different terminals of the same system. 

To run in a **Cloud (Ubuntu)** based system use the commands as follows 

```bash
docker run -it -v /home/ubuntu/Documents:/data stanlysac/edc_blockchain:iotd_ubuntu 192.168.1.228
docker run -it -v /home/ubuntu/Documents:/data stanlysac/edc_blockchain:edc_verifier_ubuntu 192.168.1.228 3
docker run -it -v /home/ubuntu/Documents:/data stanlysac/edc_blockchain:edc_1_ubuntu  192.168.1.228 1
docker run -it -v /home/ubuntu/Documents:/data stanlysac/edc_blockchain:edc_2_ubuntu  192.168.1.228 2
docker run -it -v /home/ubuntu/Documents:/data stanlysac/edc_blockchain:edc_3_ubuntu  192.168.1.228 3
```
* The received data can be viewed in the Documents folder under the name **test.csv**

To run in a **Raspberry Pi** (arm32v7) based system use the commands as follows 

```bash
docker run -it -v /home/pi/Documents:/data stanlysac/edc_blockchain:iotd_pi 192.168.1.228
docker run -it -v /home/pi/Documents:/data stanlysac/edc_blockchain:edc_verifier_pi 192.168.1.228 3
docker run -it -v /home/pi/Documents:/data stanlysac/edc_blockchain:edc_1_pi  192.168.1.228 1
docker run -it -v /home/pi/Documents:/data stanlysac/edc_blockchain:edc_2_pi  192.168.1.228 2
docker run -it -v /home/pi/Documents:/data stanlysac/edc_blockchain:edc_3_pi  192.168.1.228 3
```
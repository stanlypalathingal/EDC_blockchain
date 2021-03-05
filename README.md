## There are two ways in which the simulator can work 
### 1. Executing as a Python3 program
In order to execute as a python3 program one need to install three packages

a. pandas

b. pycrypto

c. paho-mqtt

### 2. Executing as docker containers
It requires Docker to be installed in the system and must be able to download 5 images from www.dockerhub.com 

There are two sets of images given here. One is designed to work in the normal ubuntu platform and the other is designed to work on Raspberry Pi. One can mix these entities and execute like IoTD in Cloud (ubuntu) and the rest on Raspberry Pi. The fiel to build the docker image (Dockerfile) contains the Python versions required to build in both cloud and Raspberrypi environments.


The present set up has only 3 EDC. In order to increse the number of EDC one need to create a public / privated key pairs using the file named "RSA_key_generators.py" and save with ordinal status of EDC. For example, there are three systems and if someone wants to add one more, then the number must be 4 and so on. The names of public / private key pairs must be <br /><br />
"edc_pvt_4.pem" and "edc_pub_4.pem"

<br />
The public-key must be place in the "data" directory of EDC_verifier and private-key must be in the placed in the respective "data" directory of EDC_x.

<br />
Each of these entities must run parallely in different systems or in different terminals of the same system. 
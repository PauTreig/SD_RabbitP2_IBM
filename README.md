# SD_RabbitP2_IBM
This is a repository the goal of which is to learn about RabbitMQ using Python.

# Getting Started

1. [How it Works](#How-it-Works)
2. [Additional Files](#Additional-Files)
3. [Installation](#Installation)
4. [Versioning of Python](#Versioning-of-Python)
5. [Authors](#Authors)

## How it Works

We only have to execute the file main with the number of maps that you want to spawn. Then inside the main file there are 2 functions, 
master and map. The master function will be executed asyncronous and will receive the number of maps in order to wait them. Meanwhile, the 
map function will be executed as times as maps we have passed by parameter and each execution will spwan a map. Now we have 1 master and 
"n" maps. The maps will communicate the master that they are active and the master will tell them how many maps there are and in a 
randomly way, it will activate all the maps in any order. Finally, the maps will communicate between them creating random values between 0 
and 1000, the result of each map will be a list that will be exactly the same list as the other maps lists, and this lists will be the 
result of each position of the list of the pywren map.

To execute the program:
```
python3 __main__.py 10
```
## Additional Files

You will need an additional file, named .pywren_config, situated in the home directori  ~/.pywren_config  or 
/homedirectory/.pywren_config. You can create it with `touch ~/.pywren_config` and the edit it with nano, gedit...
The file has to be like the following example:

```
pywren: 
    storage_bucket : <BUCKET NAME>

rabbitmq:
    amqp_url : <URL>

ibm_cf:
    endpoint    : <HOST>  # make sure to use https:// as prefix
    namespace   : <NAMESPACE>
    api_key     : <API_KEY>
   
ibm_cos:
    endpoint   : <REGION_ENDPOINT>  # make sure to use https:// as prefix
    access_key : <ACCESS_KEY>
    secret_key : <SECRET_KEY>
```

## Installation

With the sudo command or being root we will execute the following commands to install all the pluguins and modules necessaries to 
execute our code.
*First of all we have to have installed python3.7
*Secondly we need pip3
```
sudo apt-get install python3-pip
```
*Now we need the modules to connect to ibmcloud
```
sudo pip3 install awscli --upgrade --user
sudo pip3 install pyyaml --upgrade
sudo pip3 install boto3 --upgrade
sudo pip3 install -U ibm-cos-sdk --upgrade --user
```
*In addition, we will need pluguins to ibmfunctions and making a login to the cloud with the following commands:
```
sudo ibmcloud plugin install cloud-functions
sudo ibmcloud login -a cloud.ibm.com
```
*And finally, the pika module to make the connections and the pywren.
```
sudo pip3 install pika
sudo pip3 install pywren-ibm-cloud
```
*Remember to put the .pywren_config in the home directory  ~/.pywren_config  or /homedirectory/.pywren_config 

## Versioning of Python

You will need to have install python3.7 or above.

## Authors

Pau Treig Solé and Joan Jara Bosch a group of two students.

import random
import pywren_ibm_cloud as pywren
import sys
import pika 

def my_master_function(x):
	pywren_Conf =  json.loads(os.environ.get('PYWREN_CONFIG', ''))
	url = pywren_Conf['rabbitmq']['amqp_url']
	params = pika.URLParameters(url)
	connection = pika.BlockingConnection(params)
	channel = connection.channel()
	channel.queue_declare(queue = 'master')
	i=1
	while i<x+1:
		#codi llegir missatges
		method_frame, header_frame, body = channel.basic_get('master')
		if body != None:
			#codi enviar missatges
			taula = body.decode('utf-8')
			ran=random.randint(0,1000)
			channel.basic_publish(exchange='',routing_key=taula,body=str(ran))
			return body.decode('utf-8')
			i+=1
			
def my_map_function(x):
	pywren_Conf =  json.loads(os.environ.get('PYWREN_CONFIG', ''))
	url = pywren_Conf['rabbitmq']['amqp_url']
	params = pika.URLParameters(url)
	connection = pika.BlockingConnection(params)
	channel = connection.channel()
	channel.queue_declare(queue = str(x))
	#codi enviar missatges
	i=0
	channel.basic_publish(exchange='',routing_key='master',body=str(x))
	while i<1:
		method_frame, header_frame, body = channel.basic_get(str(x))
		if body != None:
			i+=1
		else:
			print('No message returned')
	return int(body.decode('utf-8'))
	#codi llegir missatges
	
	
	
	#return(random.randint(0,1001))

if len(sys.argv)==2 :
	nMaps=int(sys.argv[1])  #number of maps 
	idlist= list(range(1,nMaps+1)) #a list of the id of each map
	pw = pywren.ibm_cf_executor(rabbitmq_monitor=True)
	pw.call_async(my_master_function,nMaps)
	pw2 = pywren.ibm_cf_executor(rabbitmq_monitor=True)
	pw2.map(my_map_function, idlist)
	print(pw2.get_result())
else:
	print('You have to pass the number of maps that you want to create')

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
	channel.queue_declare(queue='master')
	listrand = []
	i=1
	while i<x+1:
		method_frame, properties, body = channel.basic_get('master')
		if body != None:
			channel.basic_ack(method_frame.delivery_tag)
			print("Soc el master i se que el node "+body.decode('utf-8')+" esta actiu")
			listrand.append(int(body.decode('utf-8')))
			i=i+1	
	i=1
	print("Soc el master i em disposo ha enviar el nombre de nodes a tothom")
	while i<x+1:
		channel.queue_declare(queue=str(i))
		channel.basic_publish(exchange='',routing_key=str(i),body=str(x))
		i=i+1
		
	while len(listrand) > 0:
		index = random.randint(0, len(listrand)-1)
		listActive = listrand.pop(index)
		channel.queue_declare(queue=str(listActive))
		print("Soc el master i activare al node "+str(listActive))
		channel.basic_publish(exchange='',routing_key=str(listActive),body='Active')
	channel.queue_delete(queue='master')
	channel.close()
	connection.close()
			
def my_map_function(x):
	pywren_Conf =  json.loads(os.environ.get('PYWREN_CONFIG', ''))
	url = pywren_Conf['rabbitmq']['amqp_url']
	params = pika.URLParameters(url)
	connection = pika.BlockingConnection(params)
	channel = connection.channel()
	channel.queue_declare(queue=str(x))
	#codi enviar missatges
	channel.queue_declare(queue='master')
	channel.basic_publish(exchange='',routing_key='master',body=str(x))
	i=1
	while i<2:
		method_frame, properties, body = channel.basic_get(str(x))
		if body != None:
			channel.basic_ack(method_frame.delivery_tag)
			sizeMaps=int(body.decode('utf-8'))
			print("Soc el node "+str(x)+" i he rebut el nombre de nodes totals "+str(sizeMaps))
			i=i+1
	i=1	
	listrand=[]
	while i<sizeMaps+2:
		method_frame, properties, body = channel.basic_get(str(x))
		if body != None:
			i=i+1
			channel.basic_ack(method_frame.delivery_tag)
			if body.decode('utf-8') == 'Active':
				j=1
				rand=random.randint(0,1000)
				print("Soc el node "+str(x)+" i he estat activat, enviare a tothom el valor aleatori "+str(rand))
				while j<sizeMaps+1:
					channel.queue_declare(queue=str(j))
					channel.basic_publish(exchange='',routing_key=str(j),body=str(rand))
					j=j+1
			else:
				listrand.append(int(body.decode('utf-8')))
				print("Soc el node "+str(x)+" i he rebut el valor aleatori "+body.decode('utf-8'))
	channel.queue_delete(queue=str(x))	
	channel.close()
	connection.close()
	return listrand

if len(sys.argv)==2 :
	nMaps=int(sys.argv[1])  #number of maps 
	idlist= list(range(1,nMaps+1)) #a list of the id of each map
	pw = pywren.ibm_cf_executor(rabbitmq_monitor=True)
	pw.call_async(my_master_function,nMaps)
	pw2 = pywren.ibm_cf_executor(rabbitmq_monitor=True)
	pw2.map(my_map_function, idlist)
	#There are 2 queues (master and slave) that stay undeleted. If you want to eliminate descoment the pw2.monitor() and the pw.monitor() but it
	#can block the connection
		#pw2.monitor()
		#pw.monitor()
	print(pw2.get_result())
	pw.clean()
	pw2.clean()
else:
	print('You have to pass the number of maps that you want to create')

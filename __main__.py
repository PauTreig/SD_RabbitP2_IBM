import random, sys, pika, json, os
import pywren_ibm_cloud as pywren

def connection():
	connection = pika.BlockingConnection(pika.URLParameters(url))
	channel = connection.channel()
	return channel

def callback(ch, method, properties, body):
    pw.map

def my_function_master(nfunctions):
	listrand[]	
	channel = connection()
	channel.queue_declare(queue='master_queue')
	i=0
	channel.basic_consume(callback, queue='master_queue', auto_ack=True)
	channel.start_consuming()
	while(i < nfunctions):
		exchange, queue, body = channel.basic_get(exchange='', queue='master_queue', body=str(body))
		
		if(body!='None'):
			i+=1
			listrand.append((int(body))

	while(len(listrand)>0):
		randnum=random.randint(0,len(listrand))
		channel.basic_publish(exchange='', routing_key=str(randnum),body='fet')
		listrand.delete(listrand[randnum])
	channel.close()


def my_map_function(x):
	listrand[]
	
	num=random.randint(0,1001)
	channel = connection()
	channel.queue_declare(queue=str(x))
	channel.basic_publish(exchange='', routing_key='master_queue', body=str(x))
	channel.close()
	
nfunctions=int(sys.argv[1])
pw_config = json.loads(os.environ.get('PYWREN_CONFIG', ''))
url=pw_config['rabbitmq']['amqp_url']
pw = pywren.ibm_cf_executor(rabbitmq_monitor=True)
pw.call_async(my_function_master, nfunctions)
pw = pywren.ibm_cf_executor(rabbitmq_monitor=True)
pw.map(my_map_function, range(nfunctions))
print(pw.get_result())


import random
import pywren_ibm_cloud as pywren
import sys

nfunctions=int(sys.argv[1])
listrand=[]
for x in range(1,nfunctions+1):
	listrand.append(x)
print(len(listrand))
print(listrand)

def my_map_function(x):
	return(random.randint(0,1001))

def my_function_master
pw = pywren.ibm_cf_executor()
pw.map(my_map_function, listrand)
print(pw.get_result())

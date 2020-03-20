#!/usr/bin/env python
import math, threading, zmq, struct

context = zmq.Context()
sock = context.socket(zmq.PUB)
sock.bind("tcp://*:9906")

class IniVar:
	def __init__(vars):
		vars.t_err = 0
Vars=IniVar()

#ouverture du scale
fd=open('/sys/bus/iio/devices/iio:device1/in_voltage-voltage_scale', 'r')
#lecture et conversion
scale=float(fd.read().split()[0])

if scale==0:
	print("erreur d'ouverture\n")
fd.close;


#ouverture valeur
fd=open('/sys/bus/iio/devices/iio:device1/in_voltage0-voltage1_raw', 'r')

def read_value():
	try:
		value=int(fd.read().split()[0])*scale
	except (IOError, IndexError):
		value=Vars.t_err
		print('IOError or opening error')
	Vars.t_err=value
	fd.seek(0);
#	R=-value*3
	R=value/0.112
	if R>0:
		ntc10k=1/(0.0012146+0.00021922*math.log(R)+0.00000015244*math.log(R)**3)-273.15
	else:
		print("Voltage error")
		ntc10k=0
#	print(ntc10k)
	ntc10ksend=struct.pack('f'.encode('utf-8'), ntc10k)
	sock.send(ntc10ksend)
#	print(ntc10ksend)
	read_value.thread = threading.Timer(0.1, read_value)
	read_value.thread.start()
read_value()

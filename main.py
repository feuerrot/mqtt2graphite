#!/usr/bin/env python
import paho.mqtt.client as mqtt_client
import graphitesend

config = {
	'mqtt_server': '172.23.148.3',
	'mqtt_port': 1883,
	'mqtt_subscriptions': [
		('sensor/temperature/room', 1),
		('sensor/28ff1ec760160328/temperature', 1),
	],
	'graphite_server': 'localhost'
}

translate = {
	'sensor/28ff1ec760160328/temperature': 'sensor/temperature/bathroom'
}

graphite = None

def mqtt_connect(client, userdata, flags, rc):
	print('[ ] connected to mqtt server')
	client.subscribe(config['mqtt_subscriptions'])

def mqtt_message(client, userdata, msg):
	if msg.topic in translate:
		msg.topic = translate[msg.topic].encode('utf-8')
	try:
		topic = msg.topic.replace('/', '.')
		data = float(msg.payload)
		graphite.send(topic, data)
	except ValueError:
		print('[!] can\'t convert {} to float'.format(msg.payload))
	except GraphiteSendException:
		print('[!] can\'t send data to graphite\n    please implement an enterprise loop!')
		exit(1)

if __name__ == '__main__':
	graphite = graphitesend.init(graphite_server=config['graphite_server'], prefix='', system_name='')
	mqtt = mqtt_client.Client()
	mqtt.on_connect = mqtt_connect
	mqtt.on_message = mqtt_message
	mqtt.connect(config['mqtt_server'], config['mqtt_port'])

	mqtt.loop_forever()

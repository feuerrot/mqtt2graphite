#!/usr/bin/env python
import paho.mqtt.client as mqtt_client
import graphitesend

config = {
	'mqtt_server': '172.23.148.3',
	'mqtt_port': 1883,
	'mqtt_subscriptions': [
		('sensor/temperature/room', 1),
	],
	'graphite_server': 'localhost'
}

graphite = None

def mqtt_connect(client, userdata, flags, rc):
	print('[ ] connected to mqtt server')
	client.subscribe(config['mqtt_subscriptions'])

def mqtt_message(client, userdata, msg):
	print('[ ] received message - topic {} payload {}'.format(msg.topic, msg.payload))
	graphite.send(msg.topic.replace('/', '.'), float(msg.payload))

if __name__ == '__main__':
	graphite = graphitesend.init(graphite_server=config['graphite_server'], prefix='', system_name='')
	mqtt = mqtt_client.Client()
	mqtt.on_connect = mqtt_connect
	mqtt.on_message = mqtt_message
	mqtt.connect(config['mqtt_server'], config['mqtt_port'])

	mqtt.loop_forever()

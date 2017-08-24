#!/usr/bin/env python
import paho.mqtt.client as mqtt_client
import graphitesend

config = {
	'mqtt_server': '172.23.148.3',
	'mqtt_port': 1883,
	'mqtt_subscriptions': [
		('sensor/temperature/room', 1),
	],
}

graphite = None

def mqtt_connect(client, userdata, flags, rc):
	client.subscribe(config['mqtt_subscriptions'])

def mqtt_message(client, userdata, msg):
	graphite.send(msg.topic.replace('/', '.'), msg.payload)

if __name__ == '__main__':
	graphite = graphitesend.init(dryrun=True)
	mqtt = mqtt_client.Client()
	mqtt.on_connect = mqtt_connect
	mqtt.on_message = mqtt_message
	mqtt.connect(config['mqtt_server'], config['mqtt_port'])

	mqtt.loop_forever()

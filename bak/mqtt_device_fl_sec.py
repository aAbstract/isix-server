#!/usr/bin/python

import sys
import paho.mqtt.client as mqtt_client
import mqtt_net_conf

devices_map = {
    'flood_sensor_7': {
        'device_name': 'flood_sensor_7',
        'msg_payload': 'FLOOD',
    },
    'security_lock_6': {
        'device_name': 'security_lock_6',
        'msg_payload': 'UNLOCKED',
    },
}

device = sys.argv[1]
_mqtt_client = mqtt_client.Client(client_id=f"isi_device.{devices_map[device]['device_name']}", clean_session=True, userdata=None)
mqtt_broker_ip = mqtt_net_conf.SERVER_IP

# connect to mqtt broker
_mqtt_client.username_pw_set('isi_muser', 'oE74zxUFEY35JX5ffyx4zUZTSauYS2zCFVhvL6gZe5bsBCQo3tP2pCS5VrH98mvX')
_mqtt_client.connect(mqtt_broker_ip, keepalive=60)
_mqtt_client.publish(f"telem/{devices_map[device]['device_name']}/notif", devices_map[device]['msg_payload'])
print('Sent notification message to the server')

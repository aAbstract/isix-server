#!/usr/bin/python

import time
import json
import time
import paho.mqtt.client as mqtt_client
import mqtt_net_conf

# create fake device connection
temp_reading = 0
humd_reading = 100
temp_device_state = 'OFF'
humd_device_state = 'OFF'
temp_device_name = 'temperature_sensor_3'
humd_device_name = 'humidity_sensor_2'
_mqtt_client = mqtt_client.Client(client_id=f"isi_device.{temp_device_name}-{humd_device_name}", clean_session=True, userdata=None)
mqtt_broker_ip = mqtt_net_conf.SERVER_IP
last_tic: float = -1


def broadcast_req_handler(msg: str):
    if msg == 'DEVICES_SCAN':
        print(f"Received MQTT scan request")
        _mqtt_client.publish(f"telem/{temp_device_name}/DEVICE_LWT", 'ONLINE')
        _mqtt_client.publish(f"telem/{humd_device_name}/DEVICE_LWT", 'ONLINE')


def command_req_handler(cmd_obj: dict, device_name: str):
    global temp_device_state
    global humd_device_state

    print(f"Executing command: {cmd_obj}")
    if cmd_obj['command'] == 'TOGGLE':
        if device_name == temp_device_name:
            temp_device_state = 'ON' if temp_device_state == 'OFF' else 'OFF'
            print(f"Temp Device new state: {temp_device_state}")

        elif device_name == humd_device_name:
            humd_device_state = 'ON' if humd_device_state == 'OFF' else 'OFF'
            print(f"Humd Device new state: {humd_device_state}")


def mqtt_read_handler(_1, _2, message: mqtt_client.MQTTMessage):
    if message.topic == 'telem/broadcast':
        broadcast_req_handler(message.payload.decode())
    else:
        command_req_handler(json.loads(message.payload.decode()), message.topic.split('/')[1])


def mqtt_loop():
    global temp_reading
    global humd_reading

    _mqtt_client.publish(f"state/{temp_device_name}/main", temp_device_state, retain=True)
    _mqtt_client.publish(f"state/{humd_device_name}/main", humd_device_state, retain=True)

    if temp_device_state != 'OFF':
        temp_reading = (temp_reading + 1) % 100
        _mqtt_client.publish(f"state/{temp_device_name}/main", temp_reading, retain=False)

    if humd_device_state != 'OFF':
        humd_reading = (humd_reading - 1) % 100
        _mqtt_client.publish(f"state/{humd_device_name}/main", humd_reading, retain=False)


# connect to mqtt broker
_mqtt_client.username_pw_set('isi_muser', 'oE74zxUFEY35JX5ffyx4zUZTSauYS2zCFVhvL6gZe5bsBCQo3tP2pCS5VrH98mvX')
_mqtt_client.connect(mqtt_broker_ip, keepalive=60)
_mqtt_client.subscribe('telem/broadcast')
_mqtt_client.subscribe(f"command/{temp_device_name}/power_0")
_mqtt_client.subscribe(f"command/{humd_device_name}/power_0")
_mqtt_client.on_message = mqtt_read_handler
_mqtt_client.publish(f"state/{temp_device_name}/main", temp_device_state, retain=True)
_mqtt_client.publish(f"state/{humd_device_name}/main", humd_device_state, retain=True)


print(f"MQTT device DHT online")
while True:
    _mqtt_client.loop(0.1)
    if time.time() - last_tic >= 1:
        last_tic = time.time()
        mqtt_loop()

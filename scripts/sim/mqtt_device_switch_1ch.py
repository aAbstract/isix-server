import sys
import paho.mqtt.client as mqtt_client
import mqtt_net_conf


# create fake device connection
device_state = 'OFF'
device_mqtt_id = sys.argv[1]
_mqtt_client = mqtt_client.Client(client_id=f"isi_device.{device_mqtt_id}", clean_session=True, userdata=None)


def broadcast_req_handler(msg: str):
    if msg == 'DEVICES_SCAN':
        print(f"Received MQTT Scan Request")
        _mqtt_client.publish(f"telem/{device_mqtt_id}/DEVICE_LWT", 'ONLINE')


def rpc_req_handler(msg_topic: str, msg_payload: str):
    global device_state

    print(f"RPC: {msg_topic} -> {msg_payload}")
    device_state = 'ON' if device_state == 'OFF' else 'OFF'
    print(f"Device New State: {device_state}")
    _mqtt_client.publish(f"state/{device_mqtt_id}/power_0", device_state, retain=True)


def mqtt_read_handler(_1, _2, message: mqtt_client.MQTTMessage):
    if message.topic == 'telem/broadcast':
        broadcast_req_handler(message.payload.decode())
    else:
        rpc_req_handler(message.topic, message.payload.decode())


# connect to mqtt broker
_mqtt_client.username_pw_set(mqtt_net_conf.MQTT_USERNAME, mqtt_net_conf.MQTT_PASSWORD)
_mqtt_client.connect(mqtt_net_conf.SERVER_IP, keepalive=60)
_mqtt_client.subscribe('telem/broadcast')

_mqtt_client.subscribe(f"rpc/{device_mqtt_id}/command_power_0")

_mqtt_client.on_message = mqtt_read_handler
_mqtt_client.publish(f"state/{device_mqtt_id}/power_0", device_state, retain=True)


print(f"MQTT Device {device_mqtt_id} Online")
while True:
    _mqtt_client.loop(0.1)

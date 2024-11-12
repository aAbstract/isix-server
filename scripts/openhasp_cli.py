# autopep8: off
import sys
import code
import time
import json
import serial
import readline
from rlcompleter import Completer
# autopep8: on


screen_port: serial.Serial = None
device_ip: str = None

openhasp_conf = {
    'wifi': {
        'ssid': 'Redmi 9',
        'password': '1234567800'
    },
    'mqtt': {
        'broker': '192.168.192.106',
        'port': 1883,
        'username': 'isi_muser',
        'password': 'oE74zxUFEY35JX5ffyx4zUZTSauYS2zCFVhvL6gZe5bsBCQo3tP2pCS5VrH98mvX'
    }
}

jl_msgbox = [{"page": 0, "id": 239, "obj": "msgbox", "text": "%ip%", "auto_close": 3000}]
jl_4sw_demo = [
    {"page": 0, "id": 1, "obj": "btn", "toggle": True, "x": 136, "y": 120, "w": 100, "h": 100, "text": "\ue6e8", "text_color": "#FFFFFF", "text_font": 32, "radius": 4},
    {"page": 0, "id": 2, "obj": "btn", "toggle": True, "x": 244, "y": 120, "w": 100, "h": 100, "text": "\ue6e8", "text_color": "#FFFFFF", "text_font": 32, "radius": 4},
    {"page": 0, "id": 3, "obj": "btn", "toggle": True, "x": 136, "y": 230, "w": 100, "h": 100, "text": "\ue6e8", "text_color": "#FFFFFF", "text_font": 32, "radius": 4},
    {"page": 0, "id": 4, "obj": "btn", "toggle": True, "x": 244, "y": 230, "w": 100, "h": 100, "text": "\ue6e8", "text_color": "#FFFFFF", "text_font": 32, "radius": 4},
    {"page": 0, "id": 5, "obj": "btn", "x": 0, "y": 440, "w": 160, "h": 40, "text": "\ue141", "text_color": "#FFFFFF", "text_font": 32, "radius": 0},
    {"page": 0, "id": 6, "obj": "btn", "x": 160, "y": 440, "w": 160, "h": 40, "text": "\ue2dc", "text_color": "#FFFFFF", "text_font": 24, "radius": 0},
    {"page": 0, "id": 7, "obj": "btn", "x": 320, "y": 440, "w": 160, "h": 40, "text": "\ue142", "text_color": "#FFFFFF", "text_font": 32, "radius": 0},
]


def device_exec(cmd: str):
    screen_port.write(cmd.encode() + b'\r\n')


def clear_pages():
    device_exec('clearpage all')


def factory_reset():
    device_exec('factoryreset')


def restart():
    device_exec('restart')


def device_logs():
    global device_ip
    while True:
        if not screen_port.in_waiting:
            continue
        _log = screen_port.readline().decode().replace('\r\n', '')
        if 'Prompt' in _log:
            _log = _log.replace('Prompt > ', '')
        _log = _log.split(']')[-1].strip()
        print(_log)
        if 'WIFI: Received IP address' in _log:
            device_ip = _log.split(' ')[-1]


def load_conf():
    # load wifi conf
    device_exec(f"ssid {openhasp_conf['wifi']['ssid']}")
    device_exec(f"pass {openhasp_conf['wifi']['password']}")

    # load mqtt conf
    device_exec(f"mqtthost {openhasp_conf['mqtt']['broker']}")
    device_exec(f"mqttuser {openhasp_conf['mqtt']['username']}")
    device_exec(f"mqttpass {openhasp_conf['mqtt']['password']}")


def load_flash_ui():
    device_exec('run /pages.jsonl')


def load_json(json_list: list[dict]):
    for json_obj in json_list:
        jsonl = json.dumps(json_obj)
        print('Loading', jsonl)
        device_exec(f"jsonl {jsonl}")
        time.sleep(0.1)


def ip():
    load_json(jl_msgbox)


def lui4sw():
    load_json(jl_4sw_demo)


if __name__ == '__main__':
    print('Connecting to Screen Port...')
    screen_port = serial.Serial(port='/dev/ttyUSB0', baudrate=115200)
    if screen_port.is_open:
        print('Connecting to Screen Port...OK')
    else:
        print('Connecting to Screen Port...ERR')
        sys.exit()
    readline.set_completer(Completer().complete)
    readline.parse_and_bind("tab: complete")
    code.interact(local=locals())

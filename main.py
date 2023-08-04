import network
from umqtt.simple import MQTTClient
from machine import Pin
from time import sleep, time

KEEP_ALIVE = 60
KEEP_ALIVE_SAFETY = 15
MQTT_SERVER = ''
CLIENT_ID = ''
USER_T = ''
PASSWORD_T = ''
TOPIC_SUB = ''
SSID = ''
WPA = ''

humi = Pin(14, Pin.OUT)
light = Pin(15, Pin.OUT)
last_ping = 0

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
client = MQTTClient(CLIENT_ID, MQTT_SERVER, user=USER_T, password=PASSWORD_T, keepalive=KEEP_ALIVE)

def reset():
    sleep(5)
    machine.reset()

def ping_to_keep_alive():
    global client, last_ping
    if (time() - last_ping) >= KEEP_ALIVE - KEEP_ALIVE_SAFETY:
        client.ping()
        last_ping = time()
        
def handleMessage(topic, message):
    try:
        global humi, light
        if message == b'humi':
            humi.high()
            sleep(1)
            humi.low()
        elif message == b'light':
            light.high()
            sleep(1)
            light.low()
    except:
        reset()
        
try:
    wlan.connect(SSID, WPA)
    sleep(5)
    
    if wlan.isconnected():
        client.set_callback(handleMessage)
        client.connect()
        client.subscribe(TOPIC_SUB)
    
    while wlan.isconnected():
        ping_to_keep_alive()
        client.check_msg()
        sleep(3)
        
except OSError as e:
    reset()
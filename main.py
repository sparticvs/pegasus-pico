import network
from machine import Pin
from collections import deque
from umqtt.simple import MQTTClient
import rp2
import machine
import time
import ujson

rp2.country('US')

wlan = network.WLAN(network.STA_IF)
# Pin 28 is the Sensor Output
p28 = Pin(28, mode=Pin.IN, pull=Pin.PULL_DOWN)

config = {}
client = None
MsgQueue = []

def doorStatusHandler(pin):
    state = machine.disable_irq()
    # Add change to queue
    MsgQueue.append(pin.value())
    machine.enable_irq(state)


# Register the handler
p28.irq(handler=doorStatusHandler, trigger=Pin.IRQ_FALLING|Pin.IRQ_RISING)


def tryWLANConnect():
    global config
    wlan.active(True)
    wlan.connect(config['wifi']['ssid'], config['wifi']['psswd'])

    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)

    if wlan.status() != 3:
        raise RuntimeError('network connection failed')
    else:
        print('connected')
        status = wlan.ifconfig()
        print('ip = ' + status[0])


def platformSetup():
    global client
    global config
    client = MQTTClient(config['mqtt']['client']['id'],
                        config['mqtt']['server']['host'],
                        config['mqtt']['server']['port'],
                        config['mqtt']['client']['user'],
                        config['mqtt']['client']['psswd'])
    print(client)


def loadConfig():
    global config
    file = open("config.json", "r")
    config = ujson.load(file)
    print(config)
    file.close()


def executiveLoop():
    global client
    global config
    # Add return value

    client.connect()

    while len(MsgQueue) > 0:
        msg = MsgQueue.pop(0)
        led = Pin("LED", Pin.OUT)
        led.value(msg)
        print(config['mqtt']['client']['topic'], msg)
        client.publish(config['mqtt']['client']['topic'], str(msg))

    client.disconnect()

#    machine.lightsleep()
#    machine.deepsleep()


if __name__ == '__main__':
    loadConfig()
    tryWLANConnect()
    platformSetup()

    while True:
        executiveLoop()
    


import machine
import time
import network

p_one = False

def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('Internet', 'Password')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())


def http_get(url):
    global p_one
    import socket
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    while True:
        data = s.recv(100)
        if data:
            line = str(data, 'utf8')
            if 'PinInfo'.lower() in line.lower():
                p_status = line.split('|')[2]
                if p_status.lower() == 'On'.lower():
                    p_one = True
                elif p_status.lower() == 'Off'.lower():
                    p_one = False
                print(p_one)
            print(line, end='')
        else:
            break
    s.close()


# Gets local files
def get_lf():
    import os
    os.listdir()


def make_file():
    try:
        f = open('data.txt', 'w')
        f.write('some data')
        f.close()
    except:
        print("Could not open file")


def read_file():
    print('reading file content')
    try:
        f = open('data.txt')
        for line in f.readlines():
            print(line)
        f.close()
    except:
        print("Could not open file")


def get_functions():
    print('Functions you may want to use:\n'
          'do_connect()\n'
          'http_get(url)\n'
          'create_html()\n'
          'get_lf() - Gets local files\n'
          'make_file()\n'
          'read_file()\n'
          'blink() - blinks led\n'
          'get_functions() - I don\'t have to tell what it does, you dummy\n'
          '\n'
          '\n')

def blink():
    global p_one
    pin = machine.Pin(13, machine.Pin.OUT)
    print(p_one)
    for i in range(2):
        if p_one:
            pin.on()
            time.sleep(0.5)
            pin.off()
            time.sleep(0.5)


blink()
do_connect()
blink()
get_functions()



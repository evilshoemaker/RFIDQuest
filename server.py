from flask import Flask, redirect, url_for, request, jsonify, render_template
import logging
import serial
from serial.tools import list_ports
import threading
from threading import Timer
import time
from pyrfid import PyRfid
import json

try:
    import RPi.GPIO as GPIO
except:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

RELAY_PIN = 8
RED_LED_PIN = 3
GREEN_LED_PIN = 5

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

gamers = {}

rfid_reader1 = None
rfid_reader2 = None

last_rfid_id = None
last_rfid_time = time.time()
is_door_open = False

admin_key = '0014003108'

def reset_game():
    gamers.clear()

    gamers['player1'] = { 'name' : '', 'hp' : 5, 'id' : '0014182826' }
    gamers['player2'] = { 'name' : '', 'hp' : 5, 'id' : '0014025591' }
    gamers['player3'] = { 'name' : '', 'hp' : 5, 'id' : '0014020111' }
    gamers['player4'] = { 'name' : '', 'hp' : 5, 'id' : '0014107774' }
    gamers['player5'] = { 'name' : '', 'hp' : 5, 'id' : '0014025594' }
    gamers['player6'] = { 'name' : '', 'hp' : 5, 'id' : '0014004755' }
    gamers['player7'] = { 'name' : '', 'hp' : 5, 'id' : '0014022421' }
    gamers['player8'] = { 'name' : '', 'hp' : 5, 'id' : '0007400163' }
    gamers['player9'] = { 'name' : '', 'hp' : 5, 'id' : '0014107095' }
    gamers['player10'] = { 'name' : '', 'hp' : 5, 'id' : '' }
    gamers['player11'] = { 'name' : '', 'hp' : 5, 'id' : '' }
    gamers['player12'] = { 'name' : '', 'hp' : 5, 'id' : '' }
    gamers['player13'] = { 'name' : '', 'hp' : 5, 'id' : '' }
    gamers['player14'] = { 'name' : '', 'hp' : 5, 'id' : '' }
    gamers['player15'] = { 'name' : '', 'hp' : 5, 'id' : '' }

def save_gamers_to_file():
    global gamers

    with open('tmp.json', 'w') as f:
        json.dump(gamers, f)

def load_gamers_from_file():
    global gamers

    try:
        with open('tmp.json', 'r') as f:
            gamers = json.load(f)
    except:
        pass

@app.route('/')
def home():
    return render_template('index.html', content=gamers)
    
@app.route('/event', methods=['POST'])
def event():
    if request.method == 'POST' and 'add_team' in request.form:
        for i in range(1, 16):
            gamers['player' + str(i)]['name'] = request.form['player' + str(i)]

        save_gamers_to_file()

    if request.method == 'POST' and 'clear_game' in request.form: 
        reset_game()
        save_gamers_to_file()

    return redirect(url_for('home'));

@app.route('/info')
def gamer_info():
    return render_template('info.html')

@app.route('/get_gamer_info')
def get_gamer_info():
    result = []
    for i in range(1, 16):
        if gamers['player' + str(i)]['name'] != '':
            result.append(
                {'name' : gamers['player' + str(i)]['name'],
                    'hp' : gamers['player' + str(i)]['hp']}
            )

    return jsonify(result);

def close_door():
    global is_door_open

    is_door_open = False
    try:
        GPIO.output(RELAY_PIN, 1)
        GPIO.output(RED_LED_PIN, 0)
        GPIO.output(GREEN_LED_PIN, 1)
        print('Close door')
    except Exception as e:
        print(e)

def open_door():
    global is_door_open

    if is_door_open == True:
        return

    is_door_open = True
    try:
        GPIO.output(RELAY_PIN, 0)
        GPIO.output(RED_LED_PIN, 1)
        GPIO.output(GREEN_LED_PIN, 0)
        print('Open door')
    except Exception as e:
        print(e)

    Timer(10, close_door, ()).start()

    pass

def rfid_reader(id):
    global last_rfid_time
    global last_rfid_id
    global gamers
    global admin_key
    global is_door_open

    if (last_rfid_id == id and (time.time() - last_rfid_time) < 10) or is_door_open == True:
        last_rfid_time = time.time()
        return
    
    last_rfid_time = time.time()
    last_rfid_id = id
    #print(id)

    if id == admin_key and id != '':
        open_door()
        return

    for key in gamers:
        if gamers[key]['id'] == id and gamers[key]['name'] != '':
            if gamers[key]['hp'] > 0:
                gamers[key]['hp'] = gamers[key]['hp'] - 1
                open_door()
            break
    
def rfid_reader1_receive_thread():
    while rfid_reader1:
        try:
            if (rfid_reader1.readTag() == True):
                rfid_reader(rfid_reader1.tagId)
        except Exception as e:
            print(e)

def rfid_reader2_receive_thread():
    while rfid_reader2:
        try:
            if (rfid_reader2.readTag() == True):
                rfid_reader(rfid_reader2.tagId)
        except Exception as e:
            print(e)

def start_rfid_reader():
    global rfid_reader1
    global rfid_reader2

    serial_port_list = list(serial.tools.list_ports.grep('ttyUSB*'))
    #print(len(serial_port_list))

    #for port in serial_port_list:
    #    print(port.device)

    if len(serial_port_list) > 0:
        print('Begin '+ serial_port_list[0].device)
        rfid_reader1 = PyRfid(serial_port_list[0].device, 9600)

    if len(serial_port_list) > 1:
        print('Begin '+ serial_port_list[1].device)
        rfid_reader2 = PyRfid(serial_port_list[1].device, 9600)

    threading.Thread(target=rfid_reader1_receive_thread).start()
    threading.Thread(target=rfid_reader2_receive_thread).start()

def gpio_init():
    try:
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(RELAY_PIN, GPIO.OUT, initial=1)
        GPIO.setup(RED_LED_PIN, GPIO.OUT, initial=0)
        GPIO.setup(GREEN_LED_PIN, GPIO.OUT, initial=1)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    gpio_init()
    start_rfid_reader()
    reset_game()
    load_gamers_from_file()
    app.run('0.0.0.0', 8080, False)
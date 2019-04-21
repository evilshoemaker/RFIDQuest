from flask import Flask, redirect, url_for, request, jsonify
from flask import render_template
import serial
import threading
import time
app = Flask(__name__)

rfidReaderSerial1 = None
rfidReaderSerial2 = None
gamers = {}

def reset_game():
    gamers.clear()
    #for i in range(1, 16):
    #    gamers['player' + str(i)] = { 'name' : '', 'hp' : 5 }
    gamers['player1'] = { 'name' : '', 'hp' : 5, 'id' : '' }
    gamers['player2'] = { 'name' : '', 'hp' : 5, 'id' : '' }
    gamers['player3'] = { 'name' : '', 'hp' : 5, 'id' : '' }
    gamers['player4'] = { 'name' : '', 'hp' : 5, 'id' : '' }
    gamers['player5'] = { 'name' : '', 'hp' : 5, 'id' : '' }
    gamers['player6'] = { 'name' : '', 'hp' : 5, 'id' : '' }
    gamers['player7'] = { 'name' : '', 'hp' : 5, 'id' : '' }
    gamers['player8'] = { 'name' : '', 'hp' : 5, 'id' : '' }
    gamers['player9'] = { 'name' : '', 'hp' : 5, 'id' : '' }
    gamers['player10'] = { 'name' : '', 'hp' : 5, 'id' : '' }
    gamers['player11'] = { 'name' : '', 'hp' : 5, 'id' : '' }
    gamers['player12'] = { 'name' : '', 'hp' : 5, 'id' : '' }
    gamers['player13'] = { 'name' : '', 'hp' : 5, 'id' : '' }
    gamers['player14'] = { 'name' : '', 'hp' : 5, 'id' : '' }
    gamers['player15'] = { 'name' : '', 'hp' : 5, 'id' : '' }

@app.route('/')
def home():
    return render_template('index.html', content=gamers)
    

@app.route('/event', methods=['POST'])
def event():
    if request.method == 'POST' and 'add_team' in request.form:
        for i in range(1, 16):
            gamers['player' + str(i)] = { 'name' : request.form['player' + str(i)], 'hp' : 5 }

    if request.method == 'POST' and 'clear_game' in request.form: 
        reset_game()

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

def rfid_reader(id):
    pass

def rfid_reader1_receive_thread():
  while rfidReaderSerial1:
    if rfidReaderSerial1.inWaiting() > 0:
      c = rfidReaderSerial1.read(1)
      print( c )
    else:
      time.sleep(0.1)

def start_serial(comPortName1, comPortName2):
    global rfidReaderSerial1
    global rfidReaderSerial2

    rfidReaderSerial1 = serial.Serial(
        port=comPortName1,
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
    )

    rfidReaderSerial2 = serial.Serial(
        port=comPortName2,
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
    )

    threading.Thread(target=rfid_reader1_receive_thread).start()
    #threading.Thread(target=ReceiveThread).start()


if __name__ == '__main__':
    reset_game()
    app.run('0.0.0.0', 80, False)
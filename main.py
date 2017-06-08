import threading
import time 
from enum import Enum 
from flask import Flask, request, jsonify

import helper
import authorization
import alexa_device

import snowboydecoder


app = Flask(__name__)

def State(Enum):
    idle = 0
    busy = 1

global device
global state
state = State.idle

def user_input_loop():
    """ This thread initializes a voice recognition event based on user input. This function uses command line
        input for interacting with the user. The user can start a recording, or quit if desired.

        This is currently the "main" thread for the device.
    """
    global device 
    global state
    while True:
        if state == State.busy:
            # if the thread is busy say that we are processing an external request,
            # please try again in 30 seconds 
            subprocess.call(['amixer', 'sset', 'PCM,0', '90%'])
            sound = AudioSegment.from_mp3("files/busy.mp3")

        if len(device.scribe.msg_q) > 0 and state == State.idle:
            state = State.busy
            curr_msg = device.scribe.msg_q.pop(0)
            device.user_initiate_audio(msg=curr_msg)
            print ('processed msg from scribe queue')
            state = State.idle
        else:
            # wake word --
            print (' would be initated from wake word once working')
            time.sleep(5)

    return ('',204)

@app.route("/Run", methods=['POST'])
def http_requests():   
    global device 
    device.scribe.msg_q.append('Tell me a joke')
    print("Added msg to scribe queue")

    return ('Successfully added message to scribe queue', 200)

def detected_callback():
    user_input_loop()
    print "hotword detected"

@app.route("/")
def main():
    return ('Home Called', 200)


if __name__ == "__main__":
    # Load configuration file (contains the authorization for the user and device information)
    config = helper.read_dict('config.dict')
    # Check for authorization, if none, initialize and ask user to go to a website for authorization.
    if 'refresh_token' not in config:
        print("Please go to http://localhost:5000")
        authorization.get_authorization()
        config = helper.read_dict('config.dict')
   
    print ('passed original credentials -- configuring device')
    
    # Set device to alexa device from configuration file
    global device
    device = alexa_device.AlexaDevice(config)

    # t = threading.Thread(target=user_input_loop)
    # t.start()

    # Start wake word detection ("Jarvis")
    detector = snowboydecoder.HotwordDetector("files/Jarives.pmdl", sensitivity=0.5, auto_gain=1)
    detector.start(detected_callback)

    # app.run(debug=True)
    app.run()
    print("Done -- Turning off Alexa")
    

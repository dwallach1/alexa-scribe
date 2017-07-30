import threading
import time 
import logging
from enum import Enum 
from flask import Flask, request, jsonify

import helper
import authorization
import alexa_device

import snowboydecoder


app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-9s) %(message)s',)
lock = threading.Lock()

def State(Enum):
    idle = 0
    busy = 1

# class Assistant(object):
#     def __init__(self):
#         self.device = None 
#         self.queue = []

#     def whenChanged(self):
#         next = self.queue.dequeue()
#         next.function()

#     def __setattr__(self, key, value):
#         self.key = value
#         self.whenChanged()


global device
global state
state = State.idle

def user_input_loop(hotword=False):
    """ This thread initializes a voice recognition event based on user input. This function uses command line
        input for interacting with the user. The user can start a recording, or quit if desired.

        This is currently the "main" thread for the device.
    """
    global device 
    global state
    # while True:
    # if we are processing a Scirbe request and the wakeword is called,
    # please try again in 30 seconds 
    if state == State.busy and hotword:
        subprocess.call(['amixer', 'sset', 'PCM,0', '90%'])
        sound = AudioSegment.from_mp3("files/busy.mp3")
        return 
    # called from a Scribe request
    if len(device.scribe.msg_q) > 0 and hotword == False:
        if state == State.idle:
            logging.debug('Waiting for a lock')
            lock.acquire()
            state = State.busy
            curr_msg = device.scribe.msg_q.pop(0)
            device.user_initiate_audio(msg=curr_msg)
            logging.debug('Processed message from Scribe')
            state = State.idle
            logging.debug('Released a lock')
            lock.release()

    else:
        # called from wake word detection
        print (' would be initated from wake word once working')
        device.user_initiate_audio()
        time.sleep(5)
    # we are done -- exit function, return nothing


@app.route("/Run", methods=['POST'])
def http_requests():  
    """
    this is the function that exposes Scribe to called from 3rd party applications -- allowing
    for a programmable interfece.

    The POST request will come with a json payload containing the message to be sent (a string).
    if no payload is sent, the function will do nothing.
    """ 
    global device 
    device.scribe.msg_q.append('Tell me a joke')
    print("Added msg to scribe queue")
    user_input_loop()
    return ('Successfully added message to scribe queue', 200)

def detected_callback():
    t = threading.Thread(target=user_input_loop, kwargs={'hotword': True})
    t.start()
    t.join()
    # user_input_loop()

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
    

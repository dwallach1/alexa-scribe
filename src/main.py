"""
Main.py
Author: David Wallach
Adapted from: nicholasjconn 

This file initalizes:
    - a logger
    - Flask app 
    - Alexa device
    - Hotword detector

Together, these are used to process user and web requests to be parsed, sent to Amazon Voice Services (AVS)
and act upon responses from AVS.

WORKFLOW
--------
Startup:
1. optional command line arguments are parsed and global variables are set based on these args
2. config.dict is parsed and the Alexa device is initalized 
3. wakeword begins running 
4. flask application begins running, exposing the package to be accessed via web reqeusts

running:
- hotword detected will run the start_services function and set the hotword parameter to True (default is False).
If the system is currently parsing a seperate request (from the Scribe queue), it will tell the user to that it is busy
and to try again. Otherwise, it will use the microphone as input and send the bytes to AVS
- A Scribe request made from an external service will spawn a new thread that blocks until the system is not busy,
and then processes the request

Main thread handles all the initalizatinon,
begin new thread for each request -->
    1. if it is a user request and the device is busy stop.
    2. if it is a Scribe request and the device is busy, spin unitl device is free and then process request
This is because I do not envision this collision happening often, can handle this better at a later time.
"""
import sys
import signal
import threading
import time 
import logging
from flask import Flask, request, jsonify
import helper
import authorization
import alexa_device
import snowboydecoder



# initalize services 
app = Flask(__name__)
logging.basicConfig(filename='../files/run.log', filemode='w', level=logging.DEBUG, 
                                        format='(%(threadName)-9s) %(message)s',)
logger = logging.getLogger(__name__)

lock = threading.Lock()

class State:
    idle, waiting, busy = range(3)

interrupted = False
state = State.idle
disable = False

def start_services(hotword=False):
    """ This thread initializes a voice recognition event based on user input. This function uses command line
        input for interacting with the user. The user can start a recording, or quit if desired.

        This is currently the "main" thread for the device.
    """
    global device 
    global state

    # if we are processing a Scirbe request and the wakeword is called, please try again in 30 seconds 
    if state == State.busy and hotword:
        subprocess.call(['amixer', 'sset', 'PCM,0', '90%'])
        sound = AudioSegment.from_mp3('../files/busy.mp3')
        return 
    
    # called from a Scribe request
    if len(device.scribe.msg_q) > 0 and hotword == False:
        if state == State.idle:
            logger.debug('Waiting for a lock')
            lock.acquire()
            state = State.busy
            curr_msg = device.scribe.msg_q.pop(0)
            device.user_initiate_audio(msg=curr_msg)
            logger.debug('Processed message from Scribe')
            state = State.idle
            logger.debug('Released a lock')
            lock.release()

    else:
        # called from wake word detection
        logger.debug('Start litsening for user input to mic')
        device.user_initiate_audio()
        logger.debug('Processed user request -- Done')
    
    # we are done -- exit function, return nothing

@app.route("/Run", methods=['POST'])
def scribe_handler():
    """
    this is the function that exposes Scribe to called from 3rd party applications -- allowing
    for a programmable interfece.

    The POST request will come with a json payload containing the message to be sent (a string).
    if no payload is sent, the function will do nothing.
    """ 
    global disable
    if disable:
        logger.warning('Scribe is turned off but request made')
        return 
    global device 
    msg = json.get_payload['command']
    if not isinstance(msg, str):
         logging.warning('Scribe message not of string format -- cannot parse it')
         return 
    device.scribe.msg_q.append(msg)
    #device.scribe.msg_q.append('Tell me a joke')
  
    logger.info('Added message to Scribe queue')
    t = threading.Thread(target=_scribe_handler, name='scribe handler thread')
    t.start()
    
    return ('Successfully processed message from scribe queue', 200)

def _scribe_handler():  
    while device.state == State.busy:
        pass
    start_services()
    logger.info('processed scribe request -- DONE')
    for resp in device.scribe.resp_q:
        logger.debug('AVS response: status: %s, type: %s, namespace: %s, name: %s' % (device.scribe.response.status,
                                                                                       device.scribe.response._type,
                                                                                       device.scribe.response.namespace,
                                                                                       device.scribe.response.name))

def listen():
    t = threading.Thread(target=start_services, kwargs={'hotword': True}, name='hotword_thread')
    t.start()
    # begin the thread, wait for it to return
    # t.join()
    # start_services()
    print ('hotword detected')

def interrupt_callback():
    global interrupted
    return interrupted

def signal_handler(signal, frame):
    global interrupted
    interrupted = True


@app.route("/")
def main():
    return ('Home Called', 200)


if __name__ == "__main__":
    
    # check configuration and detect if user needs to authorize device usage
    config = helper.read_dict('config.dict')
    if 'refresh_token' not in config:
        print("Please go to http://localhost:5000")
        authorization.get_authorization()
        config = helper.read_dict('config.dict')
   
    logger.debug('passed original credentials -- configuring device')
    
    # Set device to alexa device from configuration file
    global device
    device = alexa_device.AlexaDevice(config)

    # t = threading.Thread(target=start_services)
    # t.start()
    
    signal.signal(signal.SIGINT, signal_handler)

    # Start wake word detection ("Jarvis")
    detector = snowboydecoder.HotwordDetector("Jarvis.pmdl", sensitivity=0.6)
    print ('Jarvis is listening... Press ctrl+c to exit')
    detector.start(detected_callback=listen, 
                  interrupt_check=interrupt_callback,
                  sleep_time=0.03)

    logger.info('initalized device and hotword, running app now on localhost:5000')
    detector.terminate()
    # app.run(debug=True)
    #app.run()
    logger.debug('Done -- Turning off Alexa')
    

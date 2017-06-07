import threading
import time 
from flask import Flask, request, jsonify

import helper
import authorization
import alexa_device
from chronos_calendar import get_events

app = Flask(__name__)

global device

def user_input_loop():
    """ This thread initializes a voice recognition event based on user input. This function uses command line
        input for interacting with the user. The user can start a recording, or quit if desired.

        This is currently the "main" thread for the device.
    """
    global device 
    while True:
        print ('Looping again --- checking scribe msg queue')
        if len(device.scribe.msg_q) > 0:
            curr_msg = device.scribe.msg_q.pop(0)
            device.user_initiate_audio(msg=curr_msg)
            print ('processed msg from scribe queue')
        else:
            # wake word --
            print (' would be initated from wake word once working')
            time.sleep(5)

    return ('',204)

@app.route("/Run", methods=['POST'])
def http_requests():    
    # s = request.args.get("status")        
    # if int(s) == 0:
    #     HOME = False
    # elif int(s) == 1:
    #     HOME = True
    # elif int(s) == 3:
    #     print ("iOS synchronization test Successful")
    #     return ('iOS synchronization test Successful', 200) 
    # else:
    #     print ("Unkown POST Request")
    #     return ('', 500) 

    global device 
    device.scribe.msg_q.append('Tell me a joke')
    print("Added msg to scribe queue")
    return ('Successfully added message to scribe queue', 200)

@app.route("/")
def main():
    print ("Starting wakeword thread ... ")
    t = threading.Thread(target=user_input_loop)
    t.start()
    # user_input_loop(device)
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

    # Start Alexa 
    # start_wake_word()
    # app.run(debug=True)
    app.run()
    print("Done -- Turning off Alexa")
    

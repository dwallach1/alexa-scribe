
import helper
import authorization
import alexa_device

from flask import Flask, request, jsonify
from chronos_calendar import get_events

app = Flask(__name__)



def user_input_loop(alexa_device, home=None):
    """ This thread initializes a voice recognition event based on user input. This function uses command line
        input for interacting with the user. The user can start a recording, or quit if desired.

        This is currently the "main" thread for the device.
    """
    if home == None:
        while True:
            # Prompt user to press enter to start a recording, or q to quit
            print ('beginning manual Alexa services')
            text = input("Press enter anytime to start recording (or 'q' to quit).")
            # If 'q' is pressed
            if text == 'q':
                # Set stop event and break out of loop
                alexa_device.close()
                break
            alexa_device.user_initiate_audio(home=None)
    else:
        alexa_device.get_context()
        alexa_device.user_initiate_audio(home=home)
        return ('', 204) 
    return ('',204)

@app.route("/Run", methods=['POST'])
def _main():
    config = helper.read_dict('config.dict')
##    # Check for authorization, if none, initialize and ask user to go to a website for authorization.
    if 'refresh_token' not in config:
        print("Please go to http://localhost:5000")
        authorization.get_authorization()
        config = helper.read_dict('config.dict')

##    # Create alexa device
    alexa_devicE = alexa_device.AlexaDevice(config)
    
    s = request.args.get("status")        
    if int(s) == 0:
        HOME = False
    elif int(s) == 1:
        HOME = True
    elif int(s) == 3:
        print ("iOS synchronization test Successful")
        return ('', 204) 
    else:
        print ("Unkown GET Request")
        return ('', 204) 
    print (s)
    print (HOME)
    user_input_loop(alexa_devicE, home=HOME)
    print("Done")
    return ('', 204)

@app.route("/")
def main():
    config = helper.read_dict('config.dict')
    # Check for authorization, if none, initialize and ask user to go to a website for authorization.
    if 'refresh_token' not in config:
        print("Please go to http://localhost:5000")
        authorization.get_authorization()
        config = helper.read_dict('config.dict')
    print ('passed original credentials -- configuring device')
    # Create alexa device
    alexa_devicE = alexa_device.AlexaDevice(config)
    user_input_loop(alexa_devicE)
    print("Done")
    return ('', 204)


if __name__ == "__main__":
    # Load configuration file (contains the authorization for the user and device information)
    app.run(debug=True)
    #main()
    

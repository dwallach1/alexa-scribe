"""
this module is meant to handle the automation part of communicating with Alexa.

Future: use https requests to call main module. In post payload, include a scribe type

"""
from enum import Enum 

class alarm_type(Enum):
	SET = 0
	DELETE = 1



class Scribe:
	 """ This object handles the automation of communicating with Alexa. Acts as the foundation
	 for programmable interaction with your Alexa

    """
    def __init__(self, scribe):
        """ AlexaAudio initialization function.

        @PARAM t -- 
        """
        # Initialize scribe type
        # this lets the system know how to strucure audio messages
        # TODO: before initalizing Scribe -- ensure that it is a valid type
        self.type = scribe_type(scribe)

    def scribe_type(scribe):
    	return {
    		"ALARM": 2,
    		"MEDIA": 2,
    		"REQUEST": 1
    		"HOME_AUTO": 1
    	}[scribe]
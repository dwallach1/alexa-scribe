"""
this module is meant to handle the automation part of communicating with Alexa.

Future: use https requests to call main module. In post payload, include a scribe type

Make web request to run alexa -- if valid scribe type then
	- generate text
	- create mp3 from text (gTTS)
	- convert mp3 to wav 
	- tell program to send wav file to AVS and play response 
	
"""
import wave 
from gtts import gTTS
import speech_recognition
from pydub import AudioSegment

class Response:
    def __init__(self):
        content = None
        name = None
        namespace = None 


class Scribe(object):
    def __init__(self):
        """ AlexaAudio initialization function.

        @PARAM scribe -- the type of message 
        """
        self.msg_q = []
        self.resp_q = [] # array (queue) of Response Objects

    def generate_audio(self, msg, fname='files/command'):
    	"""takes in a file path and creates a wav file to be sent to AVS

    	@PARAM fname -- a filename to create (or replace) the new wav file

    	returns:
    		fname on success,
    		None otherwise
    	"""
    	# generate MP3
    	ext = '.mp3'
    	blank_noise = '            ' # we use blank noise to ensure our words are heard 
    	text = blank_noise + msg + blank_noise
    	tts = gTTS(text= text, lang='en')
    	f = fname + ext
    	tts.save(f)

    	# convert MP3 to wav b/c AVS needs wav file
    	self.convert_to_wav(fname)
    	return fname + '.wav'

    def convert_to_wav(self, fname):
    	ext = '.wav'
    	sound = AudioSegment.from_mp3(fname + '.mp3')
    	f = fname + ext
    	sound.export(f, format="wav")


    def read_response(self, audio, fname='files/response.wav'):
   	
        # Alexa uses the MP3 format for all audio responses
        # if fname[-4:] != '.mp3':
        #         return -1 
        r = speech_recognition.Recognizer()
        try:
            resp = r.recognize_google(audio)
            print ('Alexa responsed with %s' % resp)
            self.resp_q.append(resp)
        except r.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return -1
        except r.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            return -1
        except:
            return -1

        return 0


    def check_response(self, words):
            """checks to make sure all the words are present in the response
            from Alexa
            @PARAM words --  an array of words

            returns:
                    boolean
                    or -1 if no response in Scribe object
            """
            if len(self.resp_q) < 1:
                return -1
            resp = self.resp_q.pop(0)
            r = resp.split()
            for w in words:
                if not w in r:
                    return False
            return True


    def get_msg_q(self):
        return self.msg_q

    def get_resp_q(self):
        return self.resp_q

    """Some generic commands programs might use that ensure better successs

    #
    #   generate messages 
    #
    def custom_msg(self, msg):

        self.msg_q.append(msg)
        # self.generate_audio()

    def set_alarm(self, time, am=True):
        msg = 'set alarm at ' + time + ' A M '
        self.msg_q.append(msg)
        # self.generate_audio(fname)

    def delete_alarm(self, time,  am=True):
        msg = 'delete alarm at ' + time + ' A M '
        self.msg_q.append(msg)
        # self.generate_audio(fname)


    def play_spotify():

    def pause_spotity():

    def stop_spotify():

    def joke(): # good for testing 
	"""


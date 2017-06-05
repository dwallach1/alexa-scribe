import pyaudio
import wave
import subprocess
import time
import speech_recognition

import chronos
from gtts import gTTS
from pydub import AudioSegment
from chronos_calendar import get_events
import os

global count
count = 0

class AlexaAudio:
    """ This object handles all audio playback and recording required by the Alexa enabled device. Audio playback
        and recording both use the PyAudio package.

    """
    def __init__(self):
        """ AlexaAudio initialization function.
        """
        # Initialize pyaudio
        self.pyaudio_instance = pyaudio.PyAudio()

    def close(self):
        """ Called when the AlexaAudio object is no longer needed. This closes the PyAudio instance.
        """
        # Terminate the pyaudio instance
        self.pyaudio_instance.terminate()

    def get_audio(self, timeout=None, auto=True, home=True):
        """ Get audio from the microphone. The SpeechRecognition package is used to automatically stop listening
            when the user stops speaking. A timeout can also be specified. If the timeout is reached, the function
            returns None.

            This function can also be used for debugging purposes to read an example audio file.

        :param timeout: timeout in seconds, when to give up if the user did not speak.
        :return: the raw binary audio string (PCM)
        """
        global count
        if home != None:
            if count == 0:
                print ('FIRST MESSAGE')
                chronos.generate_files(home)
                __location__ = os.path.realpath(
                os.path.join(os.getcwd(), os.path.dirname(__file__)))
                path = os.path.join(__location__, 'alexa_wake.wav')
                with open(path, 'rb') as fd:  # open the file    
                    data = fd.read()
                raw_audio = data
                count += 1
            else:
                print ('SECOND MESSAGE')
                chronos.generate_files(home)
                __location__ = os.path.realpath(
                os.path.join(os.getcwd(), os.path.dirname(__file__)))
                path = os.path.join(__location__, 'alexa_command.wav')
                with open(path, 'rb') as fd:  # open the file    
                    data = fd.read()
                raw_audio = data

                count = 0
        else:
            r = speech_recognition.Recognizer()
            with speech_recognition.Microphone() as source:
                if timeout is None:
                    print ('you can start speaking now')
                    audio = r.listen()
                else:
                    try:
                        audio = r.listen(source, timeout=timeout)
                    except speech_recognition.WaitTimeoutError:
                        return None
            raw_audio = audio.get_raw_data()
            return raw_audio

        return raw_audio

    def play_mp3(self, raw_audio):
        """ Play an MP3 file. Alexa uses the MP3 format for all audio responses. PyAudio does not support this, so
            the MP3 file must first be converted to a wave file before playing.

            This function assumes ffmpeg is located in the current working directory (ffmpeg/bin/ffmpeg).

        :param raw_audio: the raw audio as a binary string
        """
        # Save MP3 data to a file
        with open("files/response.mp3", 'wb') as f:
            f.write(raw_audio)

        
        subprocess.call(['amixer', 'sset', 'PCM,0', '90%'])
        # Convert mp3 response to wave (pyaudio doesn't work with MP3 files)
        sound = AudioSegment.from_mp3("files/response.mp3")
        sound.export("files/response.wav", format="wav")

        # Play a wave file directly
        self.play_wav('files/response.wav')
        
    def play_wav(self, file, timeout=None, stop_event=None, repeat=False):
        """ Play a wave file using PyAudio. The file must be specified as a path.

        :param file: path to wave file
        """
        # Open wave wave
        with wave.open(file, 'rb') as wf:
            # Create pyaudio stream
            stream = self.pyaudio_instance.open(
                        format=self.pyaudio_instance.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

            # Set chunk size for playback
            chunk = 1024

            # Get start time
            start_time = time.mktime(time.gmtime())

            end = False
            while not end:
                # Read first chunk of data
                data = wf.readframes(chunk)
                # Continue until there is no data left
                while len(data) > 0 and not end:
                    if timeout is not None and time.mktime(time.gmtime())-start_time > timeout:
                        end = True
                    if stop_event is not None and stop_event.is_set():
                        end = True
                    stream.write(data)
                    data = wf.readframes(chunk)
                if not repeat:
                    end = True
                else:
                    wf.rewind()

        # When done, stop stream and close
        stream.stop_stream()
        stream.close()

# Chronos

The goal of this project is to automate your alarm system. Originally, I wanted to use my Amazon Echo; however, due to the
restrictions that Amazon imposes on third party developers, I built the system using a Raspberry Pi 3. I used code 
from [here](https://github.com/nicholasjconn/python-alexa-voice-service) as the base of this project. That repo intilaizes the connection between the Raspberry Pi and Amazon Voice Services. From there, I tweaked the main file as well as several others to 
account for automation as well as to run as a Flask App. I then added chronos.py and chronos_calendar.py.

- Chronos.py handles generating audio files based on the alarm time determined by the system
- Chronos_calendar.py checks your google calendar for upcoming events


# Workflow

- The user downloads the [iOS application](https://github.com/dwallach1/chronos-ios) that tracks their location 
and notifies the system when the user enters or exits thier home. The user is able to input their home address 
and update their sleeping preferences in order to let the system better determine their wake up time.

- The system will be using ngrok to expose our local server (local host 5000) to the web to allow our 
iOS application to post location events to the system.
 
- The inner system will be running on Flask to execute a python module (main.py) to then check the user's Google calendar 
and see their events for the next day and set their alarm based on their schedule as well as user defined preferences.

- The python module generates two wav files: (1) a wake file to trigger Alexa to begin the alarm actions and (2) a content
 file with time for the desired alarm constructor/destructor. Chronos uses gTTS to generate mp3 files and then pydub to 
 convert mp3s to wav files. From there it gets the bytes of the wav file and sends them to AVS. 

 ** For the alarm to work, AVS requires that we set up a downstream channel for back and forth communication with AVS. The 
 [inital project](https://github.com/nicholasjconn/python-alexa-voice-service) handled the communication. 

# Dependencies

 - Python3
 - CherryPy
 - gTTS
 - pydub
 - google api client


# To Do

Currently, by hacking into the program, I have disabled Alexa's general application to allow for the automation. The main next goal
is to allow for both functionalities simultaneously. 
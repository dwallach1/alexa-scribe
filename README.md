# Chronos

The goal of this project is to automate your alarm system. Originally, I wanted to use my Amazon Echo; however, due to the
restrictions that Amazon imposes on third party developers, I built the system using a Raspberry Pi 3. I used code 
from [here](https://github.com/nicholasjconn/python-alexa-voice-service) as the base of this project. That repo intilaizes the connection
between the Raspberry Pi and Amazon Voice Services. From there, I tweaked the main file as well as several others to 
account for automation as well as to run as a Flask App. I then added chronos.py and chronos_calendar.py.

- Chronos.py handles generating audio files based on the alarm time determined by the system
- Chronos_calendar.py checks your google calendar for upcoming events


# Workflow





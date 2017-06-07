# Alexa-Scribe

My aim for this project was to build a Python library that automated communcation Amazon Voice Services. 
Currently, Amazon requires that to trigger any Alexa capabilities the user either needs to initate a voice command 
(i.e. 'Hey Alexa') or use the mobile application to click and set alarms and such. I believe there is an array of
applications that can be used to automate user's liveswith data that is currently being collected. 
[Chronos'](https://github.com/dwallach1/chronos-ios) purpose is to showcase just one application that
 can be used by using alexa-scribe.


- AVS allows us to communicate with 'Alexa' on 3rd party devices, but there is yet a platform for us to programatically
communicate with AVS via code instead of voice. The idea is to enhance the traditional capabilities of the Echo by 
allowing programs to send requests 


# Dependencies

 - Python3
 - CherryPy
 - gTTS
 - pydub

# Code

```python
scribe = Scribe() # initalize a new Scribe object
time = datetime.time()	
scribe.set_alarm(time)
scribe.read_resp() # process response
```

# To Do

- Currently, by hacking into the program, I have disabled Alexa's general application to allow for the automation. 
The main next goal is to allow for both functionalities simultaneously. 
- Extract alexa-scribe from Chronos (seperate the two entities)
- Wake word start


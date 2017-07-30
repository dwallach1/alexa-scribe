# Alexa-Scribe
A text-based API built upon [this repo](https://github.com/nicholasjconn/python-alexa-voice-service/) to communicate with Amazon Voice Services 
without voice interaction. Currently, there is no way to access the Echo's capabilities without a voice trigger. Unfortunately, due to the limiations
imposed by Amazon, I was not able to a text-based API to run on a Amazon Echo and a raspberry pi is required. For that reason, the base communications with 
AVS from the raspberry pi is handled by nicholasjconn's repo mentioned prior. With this base, I was able to build a platform using [flask](http://flask-restful.readthedocs.io/en/0.3.5/)
to allow applications to communicate with an Rasperry Pi Echo through a programmatic manner, allowing for an array of applications

 __Some Examples__ 
 * [Chronos](https://github.com/dwallach1/chronos-ios) : an iOS application that automatically sets the user's alarm when they arrive home
 based on their calendar events for the next day as well as user defined preferences. When the user leaves their home, the application turns off all alarms
 * A few days back, I saw an article on TechCrunch about a very similar product [Silent Echo](https://techcrunch.com/2017/07/21/silent-echo-lets-you-chat-with-alexa-over-slack/); however, this product has no access to timers, alarms, music and other signifigant aspects of the Echo. Nonetheless, this product
 showcases a great use for this technology


# Dependencies

 - Python3
 - CherryPy
 - gTTS
 - pydub


# To Do
- Integrating wake word start -- [snowboy hotword detection](https://snowboy.kitt.ai)


import yaml
import time

import azure.cognitiveservices.speech as speechsdk

with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)

AZ_KEY = config['azure']['key']
AZ_REGION = config['azure']['region']

INPUT_FILE = config['data']['input_path']


def speech_recognize_continuous_from_file():
    """performs continuous speech recognition with input from an audio file"""

    # Configure Azure speech to text based on stream and API key
    speech_config = speechsdk.SpeechConfig(subscription=AZ_KEY, region=AZ_REGION)
    audio_config = speechsdk.audio.AudioConfig(filename=INPUT_FILE)

    # Set up speech to text connection
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    # Variables to indicate when processing complete and final result
    done = False
    final_result = ''

    # Stopping callback
    def stop_cb(evt):
        """callback that stops continuous recognition upon receiving an event `evt`"""
        speech_recognizer.stop_continuous_recognition()
        nonlocal done
        done = True
    
    def recognised_cb(evt):
        """Callback that saves text when API has recognised solution."""
        nonlocal final_result
        final_result += evt.result.text + ' '

    # Connect callbacks to the events fired by the speech recognizer
    # Unused events are recognizing, session_started, session_stopped, canceled
    speech_recognizer.recognized.connect(recognised_cb)
    # Stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start continuous speech recognition
    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.5)
    
    # Return final result once whole file converted to text
    if done:
        return final_result


speech_recognize_continuous_from_file()
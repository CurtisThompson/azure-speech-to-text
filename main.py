import yaml
import time

import azure.cognitiveservices.speech as speechsdk


def load_config_file(file='config.yml'):
    """Reads a YAML-formatted config file."""
    with open('config.yml', 'r') as f:
        config = yaml.safe_load(f)
    return config


def speech_recognize_continuous_from_file(config=load_config_file()):
    """Performs continuous speech recognition with input from a WAV audio file."""

    # Get required parameters from config
    AZ_KEY = config['azure']['key']
    AZ_REGION = config['azure']['region']
    INPUT_FILE = config['data']['input_path']
    VERBOSE = config['verbose']

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
        if VERBOSE:
            local_time_str = time.strftime('%H:%M:%S', time.localtime())
            print(f'[{local_time_str}] Audio processing complete.')
    
    def recognised_cb(evt):
        """Callback that saves text when API has recognised solution."""
        nonlocal final_result
        final_result += evt.result.text + ' '
        if VERBOSE:
            local_time_str = time.strftime('%H:%M:%S', time.localtime())
            print(f'[{local_time_str}] Audio segment processed.')
    
    def started_cb(evt):
        """On starting audio processing, output time and message."""
        if VERBOSE:
            local_time_str = time.strftime('%H:%M:%S', time.localtime())
            print(f'[{local_time_str}] Starting audio processing.')

    # Connect callbacks to the events fired by the speech recognizer
    # Unused events are recognizing, session_started
    speech_recognizer.recognized.connect(recognised_cb)
    speech_recognizer.session_started.connect(started_cb)
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
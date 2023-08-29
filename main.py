import time
import os
import sys

import yaml
import azure.cognitiveservices.speech as speechsdk


def load_config_file(file='config.yml'):
    """Reads a YAML-formatted config file."""
    with open(file, 'r') as f:
        config = yaml.safe_load(f)
    return config


def speech_recognize_continuous_from_file(AZ_KEY, AZ_REGION, INPUT_FILE, VERBOSE):
    """Performs continuous speech recognition with input from a WAV audio file."""

    # Configure Azure speech to text based on stream and API key
    speech_config = speechsdk.SpeechConfig(subscription=AZ_KEY, region=AZ_REGION)
    audio_config = speechsdk.audio.AudioConfig(filename=INPUT_FILE)

    # Set up speech to text connection
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    # Variables to indicate when processing complete and final result
    done = False
    final_result = ''

    # Add file name to final_result
    final_result += str(INPUT_FILE.split('/')[-1]) + '\n'

    # Stopping callback
    def stop_cb(evt):
        """callback that stops continuous recognition upon receiving an event `evt`"""
        speech_recognizer.stop_continuous_recognition()
        nonlocal done
        done = True
        if VERBOSE:
            local_time_str = time.strftime('%H:%M:%S', time.localtime())
            print(f'[{local_time_str}] File processing complete for {INPUT_FILE}.')
    
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
            print(f'[{local_time_str}] Starting audio processing for file {INPUT_FILE}.')

    # Connect callbacks to the events fired by the speech recognizer
    # Unused events are recognizing
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


def save_text(text, output_path):
    """Saves given text to a new text file. Overwrites an existing file."""
    with open(output_path, 'w') as f:
        f.write(text)


def input_output_checks(input, output):
    """Perform OS checks on input and output path, ending run if errors."""
    print(input)
    print(output)
    # Make sure input is a directory
    if not os.path.isdir(input):
        print('Processing failed. Input is not a directory.')
        sys.exit()
    
    # Make sure output is not a directory
    if os.path.isdir(output):
        print('Processing failed. Output already exists as a directory.')
        sys.exit()
    
    # Warn if output already exists
    if os.path.isfile(output):
        print('Warning. Output file already exists. File will be overwritten after speech to text conversion.')
        print('Stop this process if you do not want the file to be overwritten.')


if __name__ == "__main__":
    config = load_config_file()

    # Get required parameters from config
    AZ_KEY = config['azure']['key']
    AZ_REGION = config['azure']['region']
    INPUT_PATH = config['data']['input_path']
    OUTPUT_PATH = config['data']['output_path']
    VERBOSE = config['verbose']

    # Make sure input is a directory
    input_output_checks(INPUT_PATH, OUTPUT_PATH)

    # Get list of WAV files in input directory
    files = os.listdir(INPUT_PATH)
    files = [os.path.join(INPUT_PATH, f) for f in files if f.lower().endswith('.wav')]
    
    # Convert all WAV files into text using Azure API
    all_text = ''
    for file in files:
        text = speech_recognize_continuous_from_file(AZ_KEY, AZ_REGION, file, VERBOSE)
        all_text += text + '\n\n'
    
    # Save text to file
    save_text(all_text, OUTPUT_PATH)
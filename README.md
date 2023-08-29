# Azure Speech To Text

A repository for turning a folder of WAV speech files into text.

During testing, this code was able to convert a 12 minute audio file into approximately 1350 words in 6 minutes.

## Set-Up

To run this repository, the following Python packages are required:
 - time
 - os
 - sys
 - yaml
 - azure-cognitiveservices-speech

`time`, `os`, and `sys` are part of the Python standard utility module, however `yaml` and `azure-cognitiveservices-speech` must be installed using a package manager such as pip or conda.

You will also need an Azure Speech resource and the key to call the API. Set-up for this can be found on the [Microsoft Azure website under Speech Services](https://azure.microsoft.com/en-au/products/cognitive-services/speech-services).

## Config File

Before running the code, a config file of the following structure must be created in `./config.yml`:

```
azure:
  key: [azure-key]
  endpoint: [azure-endpoint]
  region: [azure-region]

data:
  input_path: [local-path]
  output_path: [local-path]

verbose: [True or False]
```

Note that the input path should be a directory, and the output path should be a text file. The output file will be created if it does not exist, otherwise it will be overwritten.

If you change the path to the config file in the code please make sure not to share your Azure keys online. The `./config.yml` file has been included in `./.gitignore`, and you are encouraged to do the same with any other file containing keys.

## WAV Files vs MP3 Files

Microsoft Speech Service is capable on converting both WAV and MP3 files into text. The three main reasons we chose to write this code for WAV files are:
 - WAV files are directly compatible with the Azure API. MP3 files must first be converted into a data stream which requires additional error-catching to ensure it works correctly.
 - Supporting MP3 files requires the local installation of gstreamer, whereas everything required for WAV files can be contained in this repository.
 - WAV is a loseless file format while MP3 is lossy. The higher audio quality should result it a better text transcription.

Details on how to use MP3 files instead of WAV files is provided in the [Microsoft Azure AI Services documentation](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/how-to-use-codec-compressed-audio-input-streams).
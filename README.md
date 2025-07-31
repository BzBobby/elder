# Elder Voice Assistant

This project provides a simple voice interaction tool. It records speech from the microphone, transcribes the audio, sends the text to a language model API and, when enabled, reads the reply aloud with text-to-speech.

## Requirements

- Python 3
- `sounddevice` and `soundfile` for recording and saving audio
- `requests` for communicating with the API

Install dependencies with:

```bash
pip install sounddevice soundfile requests
```

## Configuration

Edit `config.py` to set your API settings. The `ENABLE_TTS` option controls whether the assistant speaks responses:

```python
ENABLE_TTS = True  # set False to disable speech playback
```

## Usage

Run the program from the command line:

```bash
python main.py
```

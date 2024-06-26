"""
File: audioProcessing.py

Description:
    This Python script provides functions for audio processing in the context of a Speech to Text Chat Bot for VrChat.
    It includes active listening to capture audio from the microphone, conversion of audio data to text using Google Speech
    Recognition, and playback of audio files triggering facial expressions for the avatar. The script utilizes the
    'speech_recognition', 'sounddevice', and 'soundfile' libraries for audio processing and the 'pythonosc' library for
    communication with the VrChat avatar.

Dependencies:
    - asyncio
    - os
    - sounddevice
    - soundfile
    - speech_recognition
    - pythonosc.udp_client.SimpleUDPClient
    - controlVariables

Global Variables:
    - HOST: The host for the VrChat avatar communication.
    - PORT: The port for the VrChat avatar communication.
    - CLIENT: The UDP client for communication with the VrChat avatar.
    - recognizer: The speech recognition object.
    - timeout_duration: The duration for active listening timeout.

Functions:
    - awoo_face() -> None: Trigger an "awoo" facial expression for the avatar.
    - active_listening(message: str) -> AudioData or None: Perform active listening to capture audio from the microphone.
    - convert_audio_to_text(audio: AudioData) -> str or None: Convert audio data to text using Google Speech Recognition.
    - play_and_delete_sound_files(segments: list of str) -> None: Play audio files and trigger "awoo" facial expressions during playback.
    - delete_sound_files(number_of_files: int) -> None: Delete audio files.

Author:
    Augustus Sroka

Last Updated:
    04/20/2024
"""

import os
import asyncio
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr

recognizer = sr.Recognizer()
recognizer.energy_threshold = 600
recognizer.dynamic_energy_threshold = True
recognizer.dynamic_energy_adjustment_damping = 0.10
recognizer.dynamic_energy_adjustment_ratio = 2.0
recognizer.pause_threshold = 1
timeout_duration = 10


def get_audio_duration_soundfile(file_path):
    try:
        with sf.SoundFile(file_path) as audio:
            num_frames = len(audio)
            sample_rate = audio.samplerate
            return num_frames / sample_rate
    except Exception as e:
        print(f"Error using soundfile: {e}")
        return None
    

async def active_listening():
    """
    Perform active listening to capture audio from the microphone.

    Parameters:
    - message (str): The message to be sent to the chatbox.

    Returns:
    - AudioData or None: The captured audio data or None if an error occurs.
    """
    global CLIENT, recognizer, timeout_duration
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            recognizer.energy_threshold += 80
            print("Calibrated energy threshold:", recognizer.energy_threshold)
            
            print("Listening...")
            audio = recognizer.listen(source, timeout_duration)
        print("Listening finished.")
        return audio
    except sr.RequestError:
        print("Error: Unable to access the microphone.")
    except sr.WaitTimeoutError:
        print("Error: No speech detected within the specified duration.")
    return None


async def convert_audio_to_text(audio):
    """
    Convert audio data to text using Google Speech Recognition.

    Parameters:
    - audio (AudioData): The audio data to be recognized.

    Returns:
    - str or None: The recognized text or None if an error occurs.
    """
    global recognizer
    try:
        print("Recognizing...")
        text = await asyncio.to_thread(recognizer.recognize_google, audio)
        print("Recognition finished.")
        return text
    except sr.UnknownValueError:
        print("Error: Unable to recognize speech.")
    except sr.RequestError:
        print("Error: Unable to connect to Google Speech Recognition service.")
    return None


async def play_and_delete_sound_files():
    """
    Play audio files and trigger "awoo" facial expressions during playback.

    Parameters:
    - segments (list of str): List of segments to be sent to the chatbox.

    Returns:
    - None
    """
    # Read all audio files and store their data and samplerate
    audio_data = []
    file_index = 0

    while True:
        file_path = f"output{file_index}.mp3"

        if not os.path.exists(file_path):
            break

        # Read audio file and store data and samplerate
        data, samplerate = sf.read(file_path)
        audio_data.append((data, samplerate))

        file_index += 1

    # Play all audio files
    for file_index, (data, samplerate) in enumerate(audio_data):
        sd.play(data, samplerate)

        # Delay for audio to play, len(data) / samplerate - wait_duration == audio duration
        await asyncio.sleep((len(data) / samplerate) - 0.6)

    # Delete all audio files after audio is done being played
    await delete_sound_files(file_index + 1)


async def delete_sound_files(number_of_files):
    """
    Delete audio files.

    Parameters:
    - number_of_files (int): The number of audio files to be deleted.

    Returns:
    - None
    """
    try:
        for i in range(number_of_files):
            file_to_delete = f"output{i}.mp3"
            if os.path.exists(file_to_delete):
                os.remove(file_to_delete)
    except FileNotFoundError:
        pass

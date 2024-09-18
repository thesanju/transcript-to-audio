import os
import requests
from pydub import AudioSegment
import io

# Set up ElevenLabs API key
api_key = "xxxxxxx"

# Define voice options
voices = {
    "Financial Planner": "flq6f7yk4E4fJM5XTYuZ",  # Replace with desired voice ID for Financial Planner
    "Client A": "EXAVITQu4vr4xnSDxMaL"  # Replace with desired voice ID for Client A
}

# Read transcript from a text file
with open("transcript.txt", "r") as file:
    transcript = file.read()

# Split the transcript into lines
lines = transcript.split("\n")

# Initialize an empty list to store audio segments
audio_segments = []

# Iterate through lines and generate audio segments
for line in lines:
    if line.strip():
        speaker, text = line.split(": ", 1)
        if speaker in voices:
            voice_id = voices[speaker]
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            headers = {
                "Content-Type": "application/json",
                "xi-api-key": api_key
            }
            payload = {
                "text": text,
                "model_id": "eleven_monolingual_v1"
            }
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                audio_data = response.content
                audio_segment = AudioSegment.from_file(io.BytesIO(audio_data), format="mp3")
                audio_segments.append((speaker, audio_segment))
            else:
                print(f"Error generating audio for speaker {speaker}: {response.text}")

# Concatenate audio segments and export as an MP3 file
combined_audio = AudioSegment.empty()
for speaker, segment in audio_segments:
    combined_audio += segment

output_file = "output.mp3"
combined_audio.export(output_file, format="mp3")
print(f"Audio file exported to {output_file}")

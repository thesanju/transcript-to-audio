import os
import requests
from pydub import AudioSegment
import io
import streamlit as st
import yaml
import streamlit_authenticator as stauth
from yaml.loader import SafeLoader

st.set_page_config(
    page_title="Wall-e",
    page_icon="🎤",
    layout="centered",
    initial_sidebar_state="auto",
)

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

authenticator.login()

if st.session_state["authentication_status"]:
    st.sidebar.write(f'Welcome *{st.session_state["name"]}* 👋')
    authenticator.logout(location='sidebar',)

    api_key = st.secrets["LABS_API_KEY"]

    # Define available voices
    available_voices = {
        "flq6f7yk4E4fJM5XTYuZ": "Michael",
        "EXAVITQu4vr4xnSDxMaL": "Sarah",
        # Add more voice IDs and names as needed
    }

    # Streamlit app
    st.title("Transcript to Audio Converter")

    # Upload transcript file
    transcript_file = st.file_uploader("Upload transcript file", type=["txt"], help="Must be .txt files")

    if transcript_file is not None:
        transcript_content = transcript_file.read().decode("utf-8")
        speaker_names = sorted(set([line.split(": ")[0] for line in transcript_content.split("\n") if ": " in line]))

        # Speaker voice selection
        speaker_voices = {}
        for speaker in speaker_names:
            voice_selection = st.selectbox(f"Select voice for **{speaker}**", options=list(available_voices.values()), key=f"voice_{speaker}")
            speaker_voices[speaker] = [k for k, v in available_voices.items() if v == voice_selection][0]

        if st.button("Convert to Audio"):
            lines = transcript_content.split("\n")
            audio_segments = []

            if lines:
                # Show a spinner or message to indicate processing
                with st.spinner('Processing audio...'):
                    for line in lines:
                        if line.strip():
                            try:
                                speaker, text = line.split(": ", 1)
                                if speaker in speaker_voices:
                                    voice_id = speaker_voices[speaker]
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
                                        st.error(f"Error generating audio for speaker {speaker}: {response.text}")
                            except ValueError:
                                st.warning(f"Skipping line: {line} (invalid format)")
            else:
                st.warning("The transcript file is empty or does not contain valid lines.")

            combined_audio = AudioSegment.empty()
            for speaker, segment in audio_segments:
                combined_audio += segment

            output_file = "output.mp3"
            combined_audio.export(output_file, format="mp3")
            st.success(f"Audio Processing Done")

            # Display audio player
            audio_file = open(output_file, 'rb')
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format='audio/mp3')

            # Create download button
            with open(output_file, "rb") as file:
                st.download_button(
                    label="Download Audio File",
                    data=file,
                    file_name="output.mp3",
                    mime="audio/mp3",
                )

elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')
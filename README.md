## Overview

This Streamlit application converts a text transcript of two or more people's conversations into 
an audio file with each person's voice in a different voice using text-to-speech. Users can upload 
a transcript file, select voices for different speakers, and download the generated audio file.

## Prerequisites
Before running the application, ensure you have the following installed:
* Python 3.7 or higher
* pip (Python package installer)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/transcript-to-audio-converter.git
```
```bash
cd transcript-to-audio-converter
```

### 2. Install Dependencies
Navigate to the project directory and install the required Python packages:
```bash
pip install -r requirements.txt
```

### 3. Configure Authentication
Create a `config.yaml` file in the project directory with the following structure:
```yml
credentials:
  usernames:
    user1:
      name: User One
      password: hashed_password1
    user2:
      name: User Two
      password: hashed_password2
cookie:
  name: your_cookie_name
  key: your_secret_key
  expiry_days: 30
preauthorized:
  emails: []
```
Replace `hashed_password1`, `hashed_password2`, `your_cookie_name`, `your_secret_key`, and other 
placeholders with your actual values. For password hashing, you can use a library like bcrypt to 
hash your passwords.

### 4. Add API Key
Add your Eleven Labs API key to the Streamlit secrets management. Create a file named 
`.streamlit/secrets.toml` in the project directory with the following content:
```toml
[LAPS]
LABS_API_KEY = "your_eleven_labs_api_key"
```
Replace `"your_eleven_labs_api_key"` with your actual Eleven Labs API key.

### 5. Run the Application
Run the Streamlit application using the following command:
```bash
streamlit run app.py
```
This will start the Streamlight server, and you should see output indicating the local address where 
the app is running (typically `http://localhost:8501`).

### 6. Access the Application
Open your web browser and go to `http://localhost:8501`
If you want to deploy, do it on Streamlit community cloud.

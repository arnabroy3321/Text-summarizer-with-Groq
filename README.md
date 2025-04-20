# 🎙️ Audio Transcription and Summarization Tool

This Python-based tool allows you to **record audio** using your microphone, **transcribe** the recording using the [Groq API's Whisper model](https://groq.com/), and then **summarize** the transcription using a powerful LLM like `llama3-70b-8192`.

---

## ✨ Features

- 🎧 Record audio with real-time duration display
- ⌨️ Press `SPACE` to stop recording
- 📄 Transcribes the audio using Groq's Whisper model
- 🧠 Summarizes the transcription using Groq’s LLMs
- 📋 Choose from short, medium, or long summaries

---

## 🛠️ Requirements

Make sure you have **Python 3.8+** installed.

### 🔌 Python Packages

Install all required packages with pip:

```bash
pip install pyaudio keyboard requests groq

```

## 🔑 Groq API Key Setup

You need an API key from [Groq](https://groq.com/):

1. Sign up and go to your Groq dashboard.
2. Generate an API key.
3. Replace `"YOUR_GROK_API"` in the script with your key:
   - In the `transcribe_audio()` function
   - In the `summarize_text()` function

---

## 🚀 How to Use

1. Clone this repository or download the script.
2. Run the script:

   ```bash
   python your_script.py
   ```

## 💦 Sample Output

Audio Transcription and Summarization Tool
==========================================
This tool will record audio from your microphone, transcribe it, and generate a summary.

Press ENTER to start recording (then press SPACE to stop when you're done)...

=== Recording started ===
Press SPACE to stop recording
Recording time: 6 seconds

=== Recording finished ===
Recorded 6.2 seconds of audio
Audio saved to recorded_audio.wav

Transcribing your audio...

TRANSCRIPTION:
--------------
This is your transcription........

Generating summary...

SUMMARY:
--------
This is your summary.........

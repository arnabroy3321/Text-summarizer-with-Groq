import os
import base64
import requests
import pyaudio
import wave
from groq import Groq
import threading
import time
import keyboard

def record_audio(output_file="recorded_audio.wav", rate=44100, channels=1, chunk=1024):
    """Record audio from microphone with manual start/stop control."""
    # Initialize PyAudio
    p = pyaudio.PyAudio()
    
    # Open stream
    stream = p.open(format=pyaudio.paInt16,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)
    
    frames = []
    recording = True
    start_time = time.time()
    
    print("=== Recording started ===")
    print("Press SPACE to stop recording")
    
    # Create a flag for the keyboard listener
    stop_recording = threading.Event()
    
    # Define the callback for the keyboard event
    def on_space_press(e):
        if e.name == 'space':
            stop_recording.set()
            return False  # Stop listener
    
    # Start the keyboard listener in a separate thread
    keyboard.on_press_key('space', on_space_press)
    
    # Record until space is pressed
    try:
        while not stop_recording.is_set():
            data = stream.read(chunk)
            frames.append(data)
            
            # Print recording duration every second
            current_time = time.time()
            elapsed = current_time - start_time
            if int(elapsed) % 1 == 0:
                print(f"\rRecording time: {int(elapsed)} seconds", end="")
    except KeyboardInterrupt:
        pass  # Handle Ctrl+C gracefully
    
    # Print newline after duration counter
    print("\n")
    print("=== Recording finished ===")
    elapsed_time = time.time() - start_time
    print(f"Recorded {elapsed_time:.1f} seconds of audio")
    
    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    # Save the recorded data as a WAV file
    wf = wave.open(output_file, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    print(f"Audio saved to {output_file}")
    return output_file

def encode_audio_to_base64(audio_file_path):
    """Encode audio file to base64 string."""
    with open(audio_file_path, "rb") as audio_file:
        return base64.b64encode(audio_file.read()).decode("utf-8")

def transcribe_audio(audio_file_path):
    """Transcribe audio file using Groq API."""
    key = "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"
    
    # Initialize Groq client
    client = Groq(api_key=key)
    
    print(f"Transcribing file: {audio_file_path}")
    
    # Send request to Groq API for transcription
    # Groq uses OpenAI-compatible endpoints for Whisper
    url = "https://api.groq.com/openai/v1/audio/transcriptions"
    
    # Prepare the file for upload
    files = {
        'file': (os.path.basename(audio_file_path), open(audio_file_path, 'rb')),
        'model': (None, 'whisper-large-v3')
    }
    
    # Send request
    response = requests.post(
        url,
        headers={"Authorization": f"Bearer {key}"},
        files=files
    )
    
    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code}, {response.text}")
    
    result = response.json()
    return result.get("text", "")

def summarize_text(text, model="llama3-70b-8192", summary_length="medium"):
    """Summarize the given text using Groq's LLM API."""
    key = "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"
    client = Groq(api_key=key)
    
    # Configure summary length
    length_descriptions = {
        "short": "a brief 2-3 sentence summary",
        "medium": "a concise paragraph summary covering the main points",
        "long": "a detailed summary with all key points and supporting details"
    }
    
    length_desc = length_descriptions.get(summary_length, length_descriptions["medium"])
    
    # Create prompt for summarization
    prompt = f"""
    Please summarize the following text. Provide {length_desc}.
    
    TEXT TO SUMMARIZE:
    {text}
    
    SUMMARY:
    """
    
    print(f"Generating {summary_length} summary using {model}...")
    
    # Generate summary
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model=model,
        temperature=0.3,
        max_tokens=1024
    )
    
    return chat_completion.choices[0].message.content

def main():
    print("Audio Transcription and Summarization Tool")
    print("==========================================")
    print("This tool will record audio from your microphone, transcribe it, and generate a summary.")
    
    # Ask user to press Enter to start recording
    input("\nPress ENTER to start recording (then press SPACE to stop when you're done)...")
    
    # Record audio from microphone
    audio_file = record_audio()
    
    # Ask user for summary length preference
    summary_length = input("\nSummary length (short/medium/long)? ").lower()
    if summary_length not in ["short", "medium", "long"]:
        print("Invalid input. Using 'medium' length.")
        summary_length = "medium"
    
    # Transcribe the recorded audio
    print("\nTranscribing your audio...")
    transcription = transcribe_audio(audio_file)
    
    if transcription:
        print("\nTRANSCRIPTION:")
        print("--------------")
        print(transcription)
        
        # Generate summary
        print("\nGenerating summary...")
        summary = summarize_text(transcription, summary_length=summary_length)
        print("\nSUMMARY:")
        print("--------")
        print(summary)
    else:
        print("No transcription was generated. Please try recording again.")

if __name__ == "__main__":
    main()
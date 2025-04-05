import os
import base64
import requests
from groq import Groq

def encode_audio_to_base64(audio_file_path):
    """Encode audio file to base64 string."""
    with open(audio_file_path, "rb") as audio_file:
        return base64.b64encode(audio_file.read()).decode("utf-8")

def transcribe_audio(audio_file_path):
    
    # Transcribe with Groq API

    key = "Your_Groq_API"
    
    # Initialize Groq client
    client = Groq(api_key=key)
    
    # Encode audio file to base64
    audio_data = encode_audio_to_base64(audio_file_path)
    
    print(f"Transcribing file: {audio_file_path}")
    
    # Send request to Groq API for transcription
    # Groq uses OpenAI-compatible endpoints for Whisper
    url = "https://api.groq.com/openai/v1/audio/transcriptions"
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "multipart/form-data"
    }
    
    # Prepare the file for upload
    files = {
        'file': (os.path.basename(audio_file_path), open(audio_file_path, 'rb')),
        'model': (None, 'whisper-large-v3')
    }
    
    # Send request without the headers in the files request
    response = requests.post(
        url,
        headers={"Authorization": f"Bearer {key}"},
        files=files
    )
    
    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code}, {response.text}")
    
    result = response.json()
    return result.get("text", "")

def summarize_text(text = transcribe_audio("test.mp3"), model="llama3-70b-8192", summary_length="medium"):
    
    # Summarize the given text using Groq's LLM API.
    

    key = "Your_Groq_API"
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
    
    print (chat_completion.choices[0].message.content)


# transcribe_audio("test.mp3")
summarize_text()
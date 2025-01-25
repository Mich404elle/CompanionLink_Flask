import os
from openai import OpenAI

# Initialize client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def test_voice(voice_name: str):
    """Test a voice by generating sample audio"""
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice_name,
        input="Hello there! I'm Frank. Let me tell you about my favorite classic car - the 1967 Shelby GT500. What a beauty she was!"
    )
    
    # Save the audio file
    filename = f"frank_{voice_name}_test.mp3"
    with open(filename, "wb") as f:
        f.write(response.content)
    print(f"Saved {filename}")

# Test different male voices
test_voice("onyx")   # Deep male voice
test_voice("echo")   # Clear male voice
test_voice("alloy")  # Smooth male voice
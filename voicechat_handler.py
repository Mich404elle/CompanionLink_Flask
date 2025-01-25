from openai import OpenAI
import os
from dotenv import load_dotenv
import base64
import io
import tempfile

load_dotenv()

class VoiceChatHandler:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.voice_mappings = {
            'narrator': 'echo',    # Male
            'melissa': 'nova',     # Female 
            'martha': 'shimmer',   # Female
            'frank': 'onyx',       # Male
            'default': 'alloy'     # Neutral fallback
        }

    def text_to_speech(self, text, voice_type='default'):
        """
        Convert text to speech using OpenAI's TTS API
        
        Args:
            text (str): The text to convert to speech
            voice_type (str): Type of voice to use ('narrator', 'melissa', 'martha', 'character', or 'default')
        
        Returns:
            str: Base64 encoded audio data
        """
        try:
            # Get the appropriate OpenAI voice ID from our mappings
            voice = self.voice_mappings.get(voice_type, self.voice_mappings['default'])
            print(f"Using voice '{voice}' for type '{voice_type}'")
            
            # Generate speech using OpenAI's TTS
            response = self.client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=text
            )
            
            # Convert to base64 for frontend use
            audio_base64 = base64.b64encode(response.content).decode('utf-8')
            return audio_base64
            
        except Exception as e:
            print(f"Text-to-speech error: {e}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            return None

    def transcribe_audio(self, audio_file_path):
        """
        Transcribe audio file using OpenAI's Whisper API
        
        Args:
            audio_file_path (str): Path to the audio file to transcribe
        
        Returns:
            str: Transcribed text
        """
        try:
            with open(audio_file_path, 'rb') as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
            
            return transcript.text
            
        except Exception as e:
            print(f"Transcription error: {e}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            return None

# Test function
def test_voice_handler():
    handler = VoiceChatHandler()
    
    # Test different voices
    test_cases = {
        'narrator': "Welcome to the scenario. Today we'll practice communication skills.",
        'melissa': "Hello dear, how are you doing today?",
        'martha': "I've been looking at these old photos all day...",
        'frank': "That Shelby GT500 had a 428 cubic inch V8 engine. What a machine!"
    }
    
    for voice_type, text in test_cases.items():
        print(f"\nTesting {voice_type} voice...")
        audio_data = handler.text_to_speech(text, voice_type)
        if audio_data:
            print(f"✓ Text-to-speech conversion successful for {voice_type}")
        else:
            print(f"⨯ Text-to-speech conversion failed for {voice_type}")

if __name__ == "__main__":
    test_voice_handler()
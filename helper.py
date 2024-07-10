from dotenv import load_dotenv
import os
import time
import anthropic
from openai import OpenAI

# Load environment variables
load_dotenv()

client = OpenAI()
# Set up Anthropic API key
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def generate_story(topic, characters):
    characters_str = ", ".join(characters)
    prompt = f"""Write a short, kid-friendly story about {topic} featuring the following characters: {characters_str}. 
    The story should be maximum 500 words long. Make sure the story is engaging, fun, and appropriate for young children, 
    incorporating all the selected characters in a meaningful way."""

    response = anthropic.Anthropic().messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.content[0].text


def get_audio_file(text, voice_id):
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice_id,
        input=text,
    )

    # Generate a unique filename using a timestamp
    filename = f"output_{int(time.time())}.mp3"
    
    response.write_to_file(filename)
    return filename
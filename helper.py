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


def generate_story(topic, characters, duration):
    characters_str = ", ".join(characters)
    prompt = f"""Write a short, kid-friendly story about {topic} featuring the following characters: {characters_str}. Start the story with a fun title. The story should be {duration} minutes long. Make sure the story is engaging, fun, and appropriate for pre-schoolers, incorporating all the selected characters in a meaningful way.
    Think before you write the story. First, consider the age group of pre-schoolers and what themes, language, and story structures would be most appropriate and engaging for them. Then, reflect on how each of the selected characters can be meaningfully integrated into the story about the given topic, ensuring each character has a purpose and contributes to the narrative. Consider how the topic can be explored in a way that is both educational and entertaining for young children. Finally, plan the story arc to include a clear beginning, middle, and end, with a simple but valuable lesson or takeaway appropriate for pre-schoolers. After this careful consideration, write the short, kid-friendly story, keeping it within {duration} minutes and maintaining an engaging, fun, and age-appropriate tone throughout.
    DO NOT OUTPUT INFORMATION LIKE WORD COUNT, THE ENDING, OR ANYTHING ELSE. JUST WRITE THE STORY.
    """

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
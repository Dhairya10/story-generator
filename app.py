import streamlit as st
import os
from config import CHARACTERS, VOICE_DICT
from helper import generate_story, get_audio_file

# Set page config first
st.set_page_config(page_title="Story Creator", page_icon="📚", layout="wide")

# Load and apply CSS
with open('styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>Story Creator</h1>", unsafe_allow_html=True)

# Create a three-column layout
left_column, center_column, right_column = st.columns([1, 2, 1])

# Use the center column for the main content
with center_column:
    topic = st.text_input("What would you like the story to be about?")
    characters = st.multiselect("Choose characters (you can select multiple)", CHARACTERS)
    
    # Add duration input
    duration = st.slider("Choose story duration (in minutes)", min_value=1, max_value=10, value=5, step=1)

    # Create a list of voice options for the selectbox
    voice_options = [f"{voice['nickname']}" for voice in VOICE_DICT.values()]
    selected_voice = st.selectbox("Choose a voice for the story", voice_options)

    # Get the voice ID for the selected voice
    selected_voice_id = None
    for voice in VOICE_DICT.values():
        if voice['nickname'] == selected_voice:
            selected_voice_id = voice['id']
            break

    if selected_voice_id is None:
        st.error("Selected voice not found. Please try again.")
    else:
        if st.button("Create Story"):
            if topic and characters:
                story = None
                audio_file = None
                
                with st.spinner("Generating your story..."):
                    story = generate_story(topic, characters, duration)
                
                if story:
                    with st.expander("Read Your Story", expanded=True):
                        st.write(story)
                    
                    st.markdown("---")
                    
                    st.subheader("Listen to Your Story")
                    with st.spinner("Turning the story into speech..."):
                        audio_filename = get_audio_file(story, selected_voice_id)
                    
                    if audio_filename:
                        # Read the audio file
                        with open(audio_filename, "rb") as audio_file:
                            audio_bytes = audio_file.read()
                        
                        # Play the audio file
                        st.audio(audio_bytes, format="audio/mp3")
                        
                        # Optionally, provide a download link
                        st.download_button(
                            label="Download Audio",
                            data=audio_bytes,
                            file_name=audio_filename,
                            mime="audio/mp3"
                        )
                        
                        # Clean up the file after use
                        os.remove(audio_filename)
            else:
                st.warning("Please enter a topic and select at least one character.")

with st.sidebar:
    st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background-color: #F0F8FA;
    }
    </style>
    """, unsafe_allow_html=True)
    st.title("About Story Creator")
    st.info(
        "This app creates custom stories based on topics you choose, featuring popular cartoon characters. "
        "Simply enter a topic, select a character, and we'll generate a unique "
        "story starring your chosen character!"
    )
    
    st.markdown("<h3 style='color: #4E9CA8;'>How It Works</h3>", unsafe_allow_html=True)
    st.write(
        "1. Enter a topic for your story\n"
        "2. Choose character(s)\n"
        "3. Click 'Create Story'\n"
        "4. Read your story and listen to the audio version"
    )

    st.markdown("---")

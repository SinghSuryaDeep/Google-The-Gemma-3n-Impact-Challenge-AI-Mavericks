"""
Author: SURYA DEEP SINGH
LinkedIn: https://www.linkedin.com/in/surya-deep-singh-b9b94813a/
Medium: https://medium.com/@SuryaDeepSingh
GitHub: https://github.com/SinghSuryaDeep
"""
import streamlit as st
import ollama
import cv2
import numpy as np
from PIL import Image
import io
import base64
import json
import time
from datetime import datetime, timedelta
import speech_recognition as sr
import pyttsx3
import threading
import queue
import os

engine = pyttsx3.init('nsss') 

class EmpowerEdAssistant:
    def __init__(self):
        self.fast_model = "gemma3n:e2b"
        self.accurate_model = "empowered-gemma-3n-2b-q8:latest"
        self.vision_model = "gemma3n:e4b"
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        self.student_profile = self.load_saved_profile()
    
    def load_saved_profile(self):
        """Load saved profile or return defaults"""
        try:
            with open("student_profile.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "reading_speed": "slow",
                "visual_preference": "normal",
                "audio_preference": True,
                "attention_span": 10,
                "learning_style": "visual",
                "disabilities": []
            }
    
    def adaptive_text_processing(self, text, disability_type):
        
        prompt = ""
        
        if disability_type == "dyslexia":
            prompt = f"""
            Reformat this text for a student with dyslexia:
            1. Use simple, clear sentences (max 10 words each)
            2. Break into small paragraphs (2-3 sentences max)
            3. Put **key words** in bold
            4. Add bullet points where helpful
            5. Use active voice only
            
            Text: {text}
            
            Output the reformatted text with clear structure.
            """
        
        elif disability_type == "adhd":
            prompt = f"""
            Reformat this content for a student with ADHD:
            1. Break into bite-sized chunks (50 words max per section)
            2. Add 🎯 emoji markers for important points
            3. Include "Brain Break!" reminders every 3 sections
            4. Use exciting, engaging language
            5. Add interactive prompts like "Think about this!"
            
            Content: {text}
            
            Make it super engaging and easy to focus on.
            """
        
        elif disability_type == "autism":
            prompt = f"""
            Adapt this content for a student with autism:
            1. Use clear, literal language (no metaphors or idioms)
            2. Number each step or point clearly
            3. Include predictable structure with headers
            4. Be very specific and concrete
            5. Add "What comes next:" transitions
            
            Content: {text}
            
            Make it structured and predictable.
            """
        else:
            prompt = f"""
            Simplify this text for easier understanding:
            1. Use simple words (grade 3-4 level)
            2. Short sentences (10 words or less)
            3. Explain any hard words
            4. Add helpful examples
            
            Text: {text}
            
            Make it very easy to understand.
            """
        
        response = ollama.generate(
            model=self.fast_model,
            prompt=prompt,
            options={
                "temperature": 0.7,
                "top_k": 64,
                "top_p": 0.95
            }
        )
        
        return response['response']
    
    def visual_learning_aid(self, image, learning_objective):
        """
        🤖 AI HELPS HERE: Generates educational content based on learning objectives
        - Creates structured learning materials
        - Adapts explanation complexity
        - Generates comprehension questions
        """
     
        temp_image_path = "temp_learning_image.png"
        try:
            image.save(temp_image_path)
            
            if self.vision_model:
                try:
                    vision_prompt = f"""
                    Describe this image for a special needs student learning about: {learning_objective}
                    Be simple, clear, and encouraging.
                    """
                    
                    response = ollama.chat(
                        model=self.vision_model,
                        messages=[{
                            'role': 'user',
                            'content': vision_prompt,
                            'images': [temp_image_path]
                        }]
                    )
                    
                    image_description = response['message']['content']
                    
                    return self.create_visual_learning_content(image_description, learning_objective)
                    
                except Exception as e:
                    print(f"Vision model not available: {e}")
            
            return self.generate_educational_content(learning_objective)
            
        finally:
            if os.path.exists(temp_image_path):
                os.remove(temp_image_path)
    
    def create_visual_learning_content(self, image_description, learning_objective):
        """
        🤖 AI HELPS HERE: Creates comprehensive learning materials from image
        """
        prompt = f"""
        Create a special needs learning guide based on this image: {image_description}
        Learning objective: {learning_objective}
        
        Include:
        1. 📸 What We See (simple description)
        2. 📚 Learning Points (3-5 bullet points)
        3. 🌍 Real World Examples (2-3 examples)
        4. ❓ Check Understanding (2 simple questions)
        5. 🎨 Fun Activity (1 hands-on activity)
        
        Use very simple language and be encouraging!
        """
        
        response = ollama.generate(
            model=self.fast_model,
            prompt=prompt,
            options={"temperature": 0.8}
        )
        
        return response['response']
    
    def generate_educational_content(self, learning_objective):
        """
        🤖 AI HELPS HERE: Creates engaging educational content from scratch
        """
        prompt = f"""
        Create an engaging educational guide for special needs students about: {learning_objective}
        
        Structure:
        1. 🎯 What is {learning_objective}? (super simple explanation)
        2. 📚 Key Things to Know (3-5 points with emojis)
        3. 🌍 Where We See It (real-life examples)
        4. ❓ Quick Check (2 yes/no questions)
        5. 🎮 Fun Activity (something hands-on)
        
        Remember: Very simple language, lots of encouragement, use emojis!
        """
        
        response = ollama.generate(
            model=self.fast_model,
            prompt=prompt,
            options={"temperature": 0.8}
        )
        
        return response['response']
    def attention_monitor(self, interaction_time):
        """Monitor attention and suggest breaks"""
        
        if interaction_time > self.student_profile["attention_span"] * 60:
            return {
                "need_break": True,
                "suggestion": "Time for a 5-minute movement break! Stand up and stretch.",
                "activity": self.generate_break_activity()
            }
        return {"need_break": False}
        
    def multi_sensory_lesson(self, topic, disability_types):
        """
        🤖 AI HELPS HERE: Creates personalized, multi-sensory lesson plans
        - Adapts content for specific disabilities
        - Includes multiple learning modalities
        - Structures content for optimal engagement
        """
        disabilities_text = ', '.join(disability_types) if disability_types else "general learning needs"
        
        prompt = f"""
        Create a multi-sensory lesson plan for: {topic}
        Student has: {disabilities_text}
        
        Structure the lesson with these sections:
        
        🎯 LESSON GOAL
        - One clear, simple learning objective
        
        👀 VISUAL ACTIVITIES
        - 2-3 things to look at or draw
        - Simple, clear instructions
        
        👂 AUDIO ELEMENTS
        - Sounds or songs related to {topic}
        - Rhythm or rhyme to remember key facts
        
        🤸 MOVEMENT ACTIVITIES
        - 2-3 physical activities
        - Include "Simon Says" style games
        
        📝 SIMPLE EXPLANATIONS
        - Key facts in 5 words or less
        - Use comparisons to familiar things
        
        🎮 INTERACTIVE CHECKPOINTS
        - "Show me" activities
        - Yes/no understanding checks
        
        😴 SENSORY BREAKS
        - When: every 5-7 minutes
        - What: stretching, deep breathing, or quiet time
        
        Make everything super engaging and appropriate for {disabilities_text}!
        """
        
        response = ollama.generate(
            model=self.accurate_model,
            prompt=prompt,
            options={"temperature": 0.8}
        )
        
        return response['response']
    
    def generate_comprehension_questions(self, text):
        """
        🤖 AI HELPS HERE: Creates appropriate comprehension questions
        """
        prompt = f"""
        Create 3 simple comprehension questions about this text:
        {text}
        
        Requirements:
        - Use yes/no or multiple choice format
        - Very simple language
        - Test basic understanding only
        - Include encouraging feedback options
        
        Format as:
        Q1: [Question]
        Options: a) ... b) ... c) ... d) ...
        Correct: [letter]
        
        Make them appropriate for special needs students.
        """
        
        response = ollama.generate(
            model=self.fast_model,
            prompt=prompt
        )
        
        return response['response']
    
    def generate_break_activity(self):
        """Generate appropriate break activities"""
        activities = [
            "🤸 Do 10 jumping jacks",
            "🎨 Draw your favorite animal",
            "🎵 Listen to calming music for 3 minutes",
            "🧘 Deep breathing: in for 4, hold for 4, out for 4",
            "🚶 Walk around the room 3 times",
            "🤹 Juggle with imaginary balls",
            "🌟 Do 5 star jumps",
            "🦆 Walk like a duck for 30 seconds"
        ]
        
        return np.random.choice(activities)

def save_profile_to_file(profile_data):
    """Save profile to JSON file for persistence"""
    with open("student_profile.json", "w") as f:
        json.dump(profile_data, f, indent=2)

def load_profile_from_file():

    try:
        with open("student_profile.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def save_progress(topic, time_spent, quiz_score=None, activity_type="lesson"):
    """Save learning progress"""
    progress_entry = {
        "timestamp": datetime.now().isoformat(),
        "topic": topic,
        "time_spent": round(time_spent, 2),
        "quiz_score": quiz_score,
        "activity_type": activity_type,
        "disabilities": st.session_state.assistant.student_profile.get("disabilities", [])
    }
    
    with open("progress_student.json", "a") as f:
        json.dump(progress_entry, f)
        f.write("\n")

def load_progress_history():
    """Load progress history from file"""
    try:
        history = []
        with open("progress_student.json", "r") as f:
            for line in f:
                if line.strip():
                    history.append(json.loads(line.strip()))
        return history
    except FileNotFoundError:
        return []

def apply_visual_preferences(visual_mode):
    """Apply visual preferences dynamically"""
    if visual_mode == "Dyslexia-Friendly":
        st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Comic+Neue:wght@400;700&display=swap');
        
        .stApp {
            background-color: #FFFBF0 !important;
        }
        
        /* Target main content area only, not entire app */
        .main .block-container {
            font-family: 'Comic Neue', Arial, sans-serif !important;
        }
        
        /* Specific targeting for readability */
        .stMarkdown p, 
        .stMarkdown li,
        .stText,
        div[data-testid="stMarkdownContainer"] p {
            font-family: 'Comic Neue', Arial, sans-serif !important;
            letter-spacing: 0.05em !important;
            word-spacing: 0.1em !important;
            line-height: 1.6 !important;
            font-size: 1.05rem !important;
            font-weight: 400 !important;
        }
        
        /* Keep headers reasonable */
        h1, h2, h3, h4, h5, h6 {
            letter-spacing: 0.03em !important;
            line-height: 1.4 !important;
        }
        
        /* Don't affect buttons and metrics */
        .stButton > button {
            font-size: 1rem !important;
            letter-spacing: normal !important;
        }
        
        .metric-container {
            letter-spacing: normal !important;
        }
        
        /* Text areas and inputs */
        .stTextArea textarea,
        .stTextInput input {
            font-family: 'Comic Neue', Arial, sans-serif !important;
            font-size: 1rem !important;
            line-height: 1.5 !important;
        }
        
        /* Info/success/warning boxes */
        .stAlert {
            font-size: 1rem !important;
        }
        </style>
        """, unsafe_allow_html=True)
    
    elif visual_mode == "High Contrast":
        st.markdown("""
        <style>
        .stApp {
            background-color: #000000 !important;
        }
        p, div, span, li, h1, h2, h3 {
            color: #FFFF00 !important;
            font-weight: bold !important;
        }
        .stButton > button {
            background-color: #FFFF00 !important;
            color: #000000 !important;
            font-weight: bold !important;
        }
        .stTextArea textarea,
        .stTextInput input {
            background-color: #1a1a1a !important;
            color: #FFFF00 !important;
            border: 2px solid #FFFF00 !important;
        }
        </style>
        """, unsafe_allow_html=True)
    
    elif visual_mode == "Dark Mode":
        st.markdown("""
        <style>
        .stApp {
            background-color: #1a1a1a !important;
        }
        p, div, span, li {
            color: #e0e0e0 !important;
        }
        .stTextArea textarea,
        .stTextInput input {
            background-color: #2a2a2a !important;
            color: #e0e0e0 !important;
            border: 1px solid #4a4a4a !important;
        }
        </style>
        """, unsafe_allow_html=True)

def show_active_accommodations():
    """Display active accommodations based on profile"""
    if st.session_state.assistant.student_profile.get("disabilities"):
        with st.expander("🛡️ Your Active Learning Supports"):
            disabilities = st.session_state.assistant.student_profile.get("disabilities", [])
            
            cols = st.columns(2)
            
            with cols[0]:
                if "Dyslexia" in disabilities:
                    st.success("📖 **Dyslexia Support Active**")
                    st.write("• Larger text spacing")
                    st.write("• Simplified sentences")
                    st.write("• Key words highlighted")
                
                if "ADHD" in disabilities:
                    st.info("🎯 **ADHD Support Active**")
                    st.write("• Content in small chunks")
                    st.write("• Frequent break reminders")
                    st.write("• Interactive elements")
                
                if "Autism" in disabilities:
                    st.success("🧩 **Autism Support Active**")
                    st.write("• Clear structure")
                    st.write("• Literal language")
                    st.write("• Predictable patterns")
            
            with cols[1]:
                if "Visual Impairment" in disabilities:
                    st.info("👁️ **Visual Support Active**")
                    st.write("• Audio descriptions")
                    st.write("• High contrast options")
                    st.write("• Screen reader friendly")
                
                if "Hearing Impairment" in disabilities:
                    st.success("👂 **Hearing Support Active**")
                    st.write("• Visual cues")
                    st.write("• Text alternatives")
                    st.write("• Clear written instructions")
                
                if "Motor Difficulties" in disabilities:
                    st.info("🖱️ **Motor Support Active**")
                    st.write("• Larger buttons")
                    st.write("• Simplified interactions")
                    st.write("• Voice control options")

def create_ui():
    """Main Streamlit UI"""
    
    st.set_page_config(
        page_title="EmpowerEd - Special Needs Learning Assistant",
        page_icon="🌟",
        layout="wide"
    )
    
    if 'assistant' not in st.session_state:
        st.session_state.assistant = EmpowerEdAssistant()
    
    if 'start_time' not in st.session_state:
        st.session_state.start_time = time.time()
    
    if 'session_start' not in st.session_state:
        st.session_state.session_start = time.time()
    
    visual_pref = st.session_state.assistant.student_profile.get("visual_preference", "normal")
    apply_visual_preferences(visual_pref.replace("_", " ").title())
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.title("🌟 EmpowerEd - Your Learning Friend")
        show_active_accommodations()
    
    with col2:
        elapsed = int(time.time() - st.session_state.start_time)
        st.metric("⏱️ Learning Time", f"{elapsed//60}:{elapsed%60:02d}")
    
    with col3:
        attention_check = st.session_state.assistant.attention_monitor(elapsed)
        if attention_check["need_break"]:
            st.warning("🎯 Break Time!")
            st.info(attention_check["activity"])
            if st.button("✅ I took a break!"):
                st.session_state.start_time = time.time()
                st.balloons()
    
    # Sidebar for student profile
    with st.sidebar:
        st.header("👤 My Learning Profile")
        
        # Load saved profile on startup
        if 'profile_loaded' not in st.session_state:
            saved_profile = load_profile_from_file()
            if saved_profile:
                st.session_state.assistant.student_profile = saved_profile
                st.session_state.profile_loaded = True
        
        st.subheader("My Learning Needs")
        disabilities = st.multiselect(
            "Select all that apply:",
            ["Dyslexia", "ADHD", "Autism", "Visual Impairment", 
             "Hearing Impairment", "Motor Difficulties"],
            default=st.session_state.assistant.student_profile.get("disabilities", [])
        )
        
        st.subheader("My Preferences")
        
        reading_speed = st.select_slider(
            "Reading Speed",
            options=["Very Slow", "Slow", "Medium", "Fast"],
            value=st.session_state.assistant.student_profile.get("reading_speed", "slow").title()
        )
        
        use_audio = st.checkbox(
            "🔊 Read text aloud to me", 
            value=st.session_state.assistant.student_profile.get("audio_preference", True)
        )
        
       
        current_pref = st.session_state.assistant.student_profile.get("visual_preference", "normal")

        pref_mapping = {
            "normal": 0,
            "high_contrast": 1,
            "dark_mode": 2,
            "dyslexia_friendly": 3,
            "dyslexia-friendly": 3
        }

        pref_index = pref_mapping.get(current_pref, 0)

        visual_mode = st.selectbox(
            "Visual Preference",
            ["Normal", "High Contrast", "Dark Mode", "Dyslexia-Friendly"],
            index=pref_index
        )
        
        if st.button("💾 Save My Profile", key="save_profile", type="primary"):
            profile_data = {
                "disabilities": disabilities,
                "reading_speed": reading_speed.lower(),
                "audio_preference": use_audio,
                "visual_preference": visual_mode.lower().replace(" ", "_"),
                "attention_span": 10,
                "learning_style": "visual"
            }
            
            st.session_state.assistant.student_profile = profile_data
            
            save_profile_to_file(profile_data)
            
            st.success("✅ Profile saved!")
            
            apply_visual_preferences(visual_mode)
            
            st.experimental_rerun()
        with st.expander("📋 Profile Summary"):
            profile = st.session_state.assistant.student_profile
            st.json(profile)
    tab1, tab2, tab3, tab4 = st.tabs([
        "📚 Reading Helper", 
        "🎨 Visual Learning", 
        "🎯 Interactive Lessons",
        "📊 My Progress"
    ])
    
    with tab1:
        reading_helper_tab()
    
    with tab2:
        visual_learning_tab()
    
    with tab3:
        interactive_lessons_tab()
    
    with tab4:
        progress_tracker_tab()
def reading_helper_tab():
    """
    🤖 AI HELPS HERE: 
    - Adapts text for different disabilities
    - Simplifies complex content
    - Generates comprehension questions
    """
    st.header("📚 Reading Helper")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        text_input = st.text_area(
            "Paste or type text to read:",
            height=200,
            placeholder="Enter your reading material here...",
            key="reading_input"
        )
        
        if text_input:
            
            disabilities = st.session_state.assistant.student_profile.get("disabilities", [])
            
            if disabilities:
               
                primary_disability = disabilities[0].lower()
                with st.spinner(f"Adapting text for {disabilities[0]}..."):
                    processed_text = st.session_state.assistant.adaptive_text_processing(
                        text_input, primary_disability
                    )
                
                st.subheader("📖 Adapted Text:")
                
                if "Dyslexia" in disabilities:
                  
                    st.markdown(
                        f'''
                        <div style="
                            background-color: #FFFBF0;
                            padding: 20px;
                            border-radius: 10px;
                            border-left: 4px solid #4CAF50;
                            font-family: 'Comic Neue', Arial, sans-serif;
                            font-size: 1.1rem;
                            line-height: 1.8;
                            letter-spacing: 0.05em;
                            word-spacing: 0.1em;
                            color: #2c3e50;
                        ">
                        {processed_text}
                        </div>
                        ''',
                        unsafe_allow_html=True
                    )
                else:
                    st.info(processed_text)
            else:
                st.write(text_input)
    
    with col2:
        st.subheader("🛠️ Reading Tools")
        
        if text_input:
            if st.button("🔊 Read Aloud", key="read_aloud", use_container_width=True):
                with st.spinner("Reading..."):
                    engine.say(text_input)
                    engine.runAndWait()
                st.success("✅ Done reading!")
            
            if st.button("📝 Simplify Text", key="simplify", use_container_width=True):
                start_time = time.time()
                with st.spinner("Simplifying..."):
                    simplified = st.session_state.assistant.adaptive_text_processing(
                        text_input, "general"
                    )
                
                st.text_area("Simplified version:", simplified, height=200)
                
                time_spent = (time.time() - start_time) / 60
                save_progress("Reading Practice", time_spent, activity_type="reading")
            
            if st.button("❓ Check Understanding", key="check_understanding", use_container_width=True):
                with st.spinner("Creating questions..."):
                    questions = st.session_state.assistant.generate_comprehension_questions(text_input)
                
                st.write("### 🧠 Quick Check:")
                st.info(questions)
                
                if st.session_state.assistant.student_profile.get("audio_preference"):
                    if st.button("🔊 Read Questions", key="read_questions"):
                        engine.say(questions)
                        engine.runAndWait()

def visual_learning_tab():
    """
    🤖 AI HELPS HERE:
    - Analyzes images (if vision model available)
    - Creates educational content based on images
    - Generates visual learning activities
    """
    st.header("🎨 Visual Learning")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📸 Upload or Take Picture")
        
        uploaded_file = st.file_uploader(
            "Choose an image",
            type=['png', 'jpg', 'jpeg'],
            key="visual_upload"
        )
        
        camera_image = st.camera_input("Or take a photo", key="camera")
        
        learning_objective = st.text_input(
            "What are we learning?",
            placeholder="e.g., 'counting objects', 'identifying shapes', 'colors'",
            key="learning_objective"
        )
    
    with col2:
        if uploaded_file or camera_image:
            image = Image.open(uploaded_file or camera_image)
            st.image(image, caption="Learning Image", use_column_width=True)
            
            if st.button("🧠 Create Learning Guide", key="explain_image", type="primary"):
                start_time = time.time()
                
                with st.spinner("Creating your learning guide..."):
                    explanation = st.session_state.assistant.visual_learning_aid(
                        image,
                        learning_objective or "general learning"
                    )
                    
                    st.session_state['current_explanation'] = explanation
                
                st.write("### 📚 Your Learning Guide:")
                st.success(explanation)
                
                # Track progress
                time_spent = (time.time() - start_time) / 60
                save_progress(f"Visual Learning: {learning_objective or 'General'}", 
                            time_spent, activity_type="visual")
            
            # Audio option
            if ('current_explanation' in st.session_state and 
                st.session_state.assistant.student_profile.get("audio_preference")):
                
                if st.button("🔊 Listen to Guide", key="listen_explanation"):
                    with st.spinner("Reading aloud..."):
                        engine.say(st.session_state['current_explanation'])
                        engine.runAndWait()
                    st.success("✅ Done!")

def interactive_lessons_tab():
    """
    🤖 AI HELPS HERE:
    - Creates personalized lesson plans
    - Generates practice questions
    - Adapts content for disabilities
    """
    st.header("🎯 Interactive Lessons")
    
    # Lesson creation
    col1, col2 = st.columns([3, 1])
    
    with col1:
        topic = st.text_input(
            "What would you like to learn today?",
            placeholder="e.g., 'numbers 1-10', 'colors', 'emotions', 'animals'",
            key="lesson_topic"
        )
    
    with col2:
        difficulty = st.selectbox(
            "Level",
            ["Beginner", "Easy", "Medium", "Challenging"],
            key="difficulty_level"
        )
    
    if topic and st.button("🚀 Create My Lesson", key="create_lesson", type="primary"):
        lesson_start = time.time()
        
        with st.spinner("Creating your personalized lesson..."):
            
            st.session_state['current_topic'] = topic
            st.session_state['current_difficulty'] = difficulty
            
            disabilities = st.session_state.assistant.student_profile.get("disabilities", ["general"])
            lesson = st.session_state.assistant.multi_sensory_lesson(topic, disabilities)
            
            st.session_state['current_lesson'] = lesson
        
        st.markdown("---")
        st.subheader(f"📖 Today's Lesson: {topic}")
        
        sections = lesson.split("\n\n")
        for i, section in enumerate(sections):
            if section.strip():
                
                with st.expander(
                    section.split("\n")[0] if "\n" in section else f"Section {i+1}",
                    expanded=(i < 2)  
                ):
                    st.write(section)
                    
                    if any(word in section.lower() for word in ["activity", "exercise", "try", "do"]):
                        if st.button(f"✅ I did this!", key=f"activity_{i}"):
                            st.balloons()
                            st.success("🌟 Fantastic work!")
        
        time_spent = (time.time() - lesson_start) / 60
        save_progress(topic, time_spent, activity_type="lesson")
    
    st.markdown("---")
    st.subheader("🎮 Practice Time!")
    
    if 'current_topic' not in st.session_state:
        st.info("👆 Create a lesson first, then practice here!")
    else:
        if st.button("🎲 Generate Practice Questions", key="generate_practice"):
            with st.spinner("Creating fun practice questions..."):
                questions = generate_practice_questions(
                    st.session_state['current_topic'],
                    st.session_state.get('current_difficulty', 'Easy'),
                    st.session_state.assistant.student_profile.get("disabilities", [])
                )
                
                st.session_state['practice_questions'] = questions
                st.session_state['current_question_index'] = 0
                st.session_state['score'] = 0
        
        if 'practice_questions' in st.session_state:
            display_practice_interface()

def generate_practice_questions(topic, difficulty, disabilities):
    """
    🤖 AI HELPS HERE: Generates adaptive practice questions
    """
    
    adaptations = []
    if "Visual Impairment" in disabilities:
        adaptations.append("audio-friendly, no visual dependencies")
    if "Dyslexia" in disabilities:
        adaptations.append("simple language, short sentences")
    if "ADHD" in disabilities:
        adaptations.append("engaging, quick to answer")
    
    prompt = f"""
    Create 3 practice questions about: {topic}
    Difficulty: {difficulty}
    Adaptations needed: {', '.join(adaptations) if adaptations else 'general special needs'}
    
    Return a JSON array with exactly 3 questions:
    [{{
        "question": "Simple question text",
        "type": "multiple_choice",
        "options": ["Option A", "Option B", "Option C", "Option D"],
        "correct_answer": "Option A",
        "feedback": "Try again! Hint: ...",
        "success_message": "Great job! You got it!"
    }}]
    
    Make questions fun, encouraging, and appropriate for special needs students.
    """
    
    try:
        response = ollama.generate(
            model=st.session_state.assistant.fast_model,
            prompt=prompt,
            options={"temperature": 0.7}
        )
        
        # Extract JSON from response
        response_text = response['response']
        json_start = response_text.find('[')
        json_end = response_text.rfind(']') + 1
        
        if json_start != -1 and json_end != 0:
            json_str = response_text[json_start:json_end]
            return json.loads(json_str)
        else:
            raise ValueError("No valid JSON found")
            
    except Exception as e:
       print(f"Error generating questions: {e}")
       # Fallback questions
       return [
           {
               "question": f"Is {topic} something you enjoy learning about?",
               "type": "yes_no",
               "options": ["Yes! 😊", "No 😕"],
               "correct_answer": "Yes! 😊",
               "feedback": "That's okay! Let's make it more fun!",
               "success_message": "Wonderful! Learning is always better when we enjoy it!"
           },
           {
               "question": f"Can you name one thing about {topic}?",
               "type": "multiple_choice",
               "options": ["Yes, I can!", "I need help", "Maybe", "Not sure"],
               "correct_answer": "Yes, I can!",
               "feedback": "That's alright! Let's think together!",
               "success_message": "Excellent thinking! You're doing great!"
           },
           {
               "question": f"Would you like to learn more about {topic}?",
               "type": "yes_no",
               "options": ["Yes! 🎯", "Maybe later 😴"],
               "correct_answer": "Yes! 🎯",
               "feedback": "That's fine! We can learn when you're ready!",
               "success_message": "That's the spirit! Keep being curious!"
           }
       ]

def display_practice_interface():
   """Display interactive practice questions"""
   questions = st.session_state.get('practice_questions', [])
   current_idx = st.session_state.get('current_question_index', 0)
   
   if current_idx < len(questions):
       
       q = questions[current_idx]
       st.write(f"### Question {current_idx + 1} of {len(questions)}")
       st.info(f"**{q['question']}**")
       
       answer_key = f"practice_answer_{current_idx}"
       
       if q['type'] == 'multiple_choice':
           answer = st.radio(
               "Choose your answer:",
               q['options'],
               key=answer_key
           )
       elif q['type'] == 'yes_no':
           answer = st.radio(
               "Choose your answer:",
               q['options'],
               key=answer_key
           )
       elif q['type'] == 'true_false':
           answer = st.radio(
               "Choose your answer:",
               ["✅ True", "❌ False"],
               key=answer_key
           )
       else:
           answer = None
       
       col1, col2 = st.columns(2)
       
       with col1:
           if st.button("✅ Check Answer", key=f"check_{current_idx}"):
               if answer:
                   is_correct = answer == q['correct_answer'] or q['correct_answer'].lower() in answer.lower()
                   
                   if is_correct:
                       st.success(q['success_message'])
                       st.balloons()
                       st.session_state['score'] = st.session_state.get('score', 0) + 1
                   else:
                       st.warning(q['feedback'])
       
       with col2:
           if current_idx < len(questions) - 1:
               if st.button("➡️ Next Question", key=f"next_{current_idx}"):
                   st.session_state['current_question_index'] = current_idx + 1
                   st.experimental_rerun()
           else:
               if st.button("🏁 Finish Practice", key="finish_practice"):
                   st.session_state['current_question_index'] = len(questions)
                   st.experimental_rerun()
   
   else:
      
       score = st.session_state.get('score', 0)
       total = len(questions)
       percentage = (score / total * 100) if total > 0 else 0
       
       st.success(f"### 🎉 Practice Complete!")
       st.metric("Your Score", f"{score}/{total} ({percentage:.0f}%)")
       
       save_progress(
           f"Quiz: {st.session_state.get('current_topic', 'Unknown')}",
           5,  
           percentage,
           activity_type="quiz"
       )
       
       if percentage >= 70:
           st.balloons()
           st.success("🌟 Amazing work! You're a star learner!")
       else:
           st.info("💪 Good effort! Practice makes perfect!")
       
       if st.button("🔄 Practice Again", key="practice_again"):
           st.session_state.pop('practice_questions', None)
           st.session_state.pop('current_question_index', None)
           st.session_state.pop('score', None)
           st.experimental_rerun()

def progress_tracker_tab():
   """
   🤖 AI HELPS HERE:
   - Analyzes learning patterns
   - Generates insights from progress data
   - Creates personalized recommendations
   """
   st.header("📊 My Learning Journey")
   
   progress_history = load_progress_history()
   
   if not progress_history:
       st.info("🌱 Your learning journey starts here! Complete some activities to see your progress.")
       
       with st.expander("🔮 Preview Your Future Progress"):
           st.write("""
           Once you start learning, you'll see:
           - 📈 Daily learning charts
           - 🏆 Achievement badges  
           - 💪 Your learning strengths
           - 🎯 Progress toward goals
           - 📊 Personalized insights
           """)
       return
   
   df_data = []
   for entry in progress_history:
       date = datetime.fromisoformat(entry['timestamp'])
       df_data.append({
           'date': date.date(),
           'weekday': date.strftime('%A'),
           'topic': entry.get('topic', 'Unknown'),
           'time_spent': entry.get('time_spent', 0),
           'score': entry.get('quiz_score', None),
           'activity': entry.get('activity_type', 'lesson')
       })
   
   import pandas as pd
   df = pd.DataFrame(df_data)
   
   col1, col2, col3, col4 = st.columns(4)
   
   with col1:
       total_time = df['time_spent'].sum()
       st.metric("⏱️ Total Time", f"{total_time:.0f} min")
   
   with col2:
       total_activities = len(df)
       st.metric("📚 Activities", total_activities)
   
   with col3:
       avg_score = df[df['score'].notna()]['score'].mean() if any(df['score'].notna()) else 0
       st.metric("📊 Avg Score", f"{avg_score:.0f}%")
   
   with col4:
       unique_topics = df['topic'].nunique()
       st.metric("🌈 Topics", unique_topics)
   
   col1, col2 = st.columns(2)
   
   with col1:
       st.subheader("📈 Daily Learning Activity")
       
       daily_data = df.groupby('date').agg({
           'time_spent': 'sum',
           'topic': 'count'
       }).reset_index()
       daily_data.columns = ['Date', 'Minutes', 'Activities']
       
       import plotly.graph_objects as go
       
       fig = go.Figure()
       fig.add_trace(go.Bar(
           x=daily_data['Date'],
           y=daily_data['Minutes'],
           name='Learning Time',
           marker_color='lightblue',
           text=daily_data['Minutes'].round(1),
           textposition='outside'
       ))
       
       fig.update_layout(
           title="Daily Learning Minutes",
           xaxis_title="Date",
           yaxis_title="Minutes",
           height=300,
           showlegend=False
       )
       
       st.plotly_chart(fig, use_container_width=True)
   
   with col2:
       st.subheader("🎯 Learning by Topic")
       
       topic_data = df.groupby('topic')['time_spent'].sum().sort_values(ascending=False).head(5)
       
       fig2 = go.Figure(data=[
           go.Pie(
               labels=topic_data.index,
               values=topic_data.values,
               hole=.3,
               marker=dict(colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8'])
           )
       ])
       
       fig2.update_layout(
           title="Top 5 Topics by Time",
           height=300
       )
       
       st.plotly_chart(fig2, use_container_width=True)
   
   st.markdown("---")
   st.subheader("🧠 Your Learning Insights")
   
   insights = generate_learning_insights(df, st.session_state.assistant.student_profile)
   
   cols = st.columns(3)  
   for i, insight in enumerate(insights[:3]):  
        with cols[i]:
            st.info(f"{insight['emoji']} **{insight['title']}**\n\n{insight['description']}")
    


   for col, insight in zip(cols, insights):
       with col:
           st.info(f"{insight['emoji']} **{insight['title']}**\n\n{insight['description']}")
   
   streak = calculate_learning_streak(progress_history)
   if streak > 0:
       st.success(f"🔥 Learning Streak: {streak} days in a row! Keep it up!")
   
   st.markdown("---")
   st.subheader("💡 Personalized Recommendations")
   
   recommendations = generate_recommendations(df, st.session_state.assistant.student_profile)
   for rec in recommendations:
       st.write(f"• {rec}")
   
   st.markdown("---")
   st.subheader("🎯 My Learning Goals")
   
   col1, col2 = st.columns([3, 1])
   
   with col1:
       goal = st.text_input(
           "Set a new learning goal:",
           placeholder="e.g., 'Learn 10 new words this week', 'Practice math for 30 minutes daily'"
       )
   
   with col2:
       if goal and st.button("Set Goal", key="set_goal"):
           
           goal_data = {
               "goal": goal,
               "created": datetime.now().isoformat(),
               "status": "active"
           }
           
           with open("learning_goals.json", "a") as f:
               json.dump(goal_data, f)
               f.write("\n")
           
           st.success("🎯 Goal set!")
           st.balloons()

def generate_learning_insights(df, profile):
   """
   🤖 AI HELPS HERE: Analyzes data to generate personalized insights
   """
   insights = []
   
   total_time = df['time_spent'].sum()
   if total_time > 60:
       hours = total_time / 60
       insights.append({
           "emoji": "⏰",
           "title": "Time Champion",
           "description": f"You've learned for {hours:.1f} hours total!"
       })
   
   unique_days = df['date'].nunique()
   if unique_days > 5:
       insights.append({
           "emoji": "📅",
           "title": "Consistent Learner",
           "description": f"You've practiced on {unique_days} different days!"
       })
   
   topics = df['topic'].unique()
   if len(topics) > 3:
       insights.append({
           "emoji": "🌈",
           "title": "Explorer",
           "description": f"You've explored {len(topics)} different topics!"
       })
   
   quiz_scores = df[df['score'].notna()]['score']
   if len(quiz_scores) > 0:
       avg_score = quiz_scores.mean()
       if avg_score > 80:
           insights.append({
               "emoji": "🏆",
               "title": "Quiz Master",
               "description": f"Average score of {avg_score:.0f}%!"
           })
   
   return insights[:3]  

def generate_recommendations(df, profile):
   """
   🤖 AI HELPS HERE: Creates personalized learning recommendations
   """
   recommendations = []
   
   avg_session_time = df['time_spent'].mean()
   if avg_session_time < 10:
       recommendations.append("🕒 Try longer learning sessions (15-20 minutes) for deeper understanding")
   
   top_topics = df.groupby('topic')['time_spent'].sum().sort_values(ascending=False).head(3)
   if len(top_topics) > 0:
       recommendations.append(f"💡 You enjoy {top_topics.index[0]} - explore related topics!")
   
   if "ADHD" in profile.get("disabilities", []):
       recommendations.append("🎯 Remember to take breaks every 10 minutes")
   
   if "Dyslexia" in profile.get("disabilities", []):
       recommendations.append("📖 Use the text simplifier for all reading materials")
   
   recent_scores = df[df['score'].notna()].tail(3)['score']
   if len(recent_scores) > 0 and recent_scores.mean() < 70:
       recommendations.append("📚 Review lessons before taking practice quizzes")
   
   return recommendations[:4]

def calculate_learning_streak(history):
   """Calculate consecutive learning days"""
   if not history:
       return 0
   
   dates = sorted(set(datetime.fromisoformat(h['timestamp']).date() for h in history))
   
   streak = 1
   for i in range(len(dates) - 1, 0, -1):
       if (dates[i] - dates[i-1]).days == 1:
           streak += 1
       else:
           break
   
   return streak

def main():
   """Main application entry point"""
   create_ui()
   
   # Footer
   st.markdown("---")
   st.markdown(
       """<center>
       <h3>🌟 Remember: You're doing great! Every step counts! 🌟</h3>
       <p style='color: gray;'>Powered by Gemma AI to make learning accessible for everyone</p>
       </center>""",
       unsafe_allow_html=True
   )

if __name__ == "__main__":
   main()
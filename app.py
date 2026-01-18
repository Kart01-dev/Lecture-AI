"""
Lecture AI - Voice to Knowledge Converter
Convert lectures to flashcards, notes, and summaries
"""

import streamlit as st
import os
from pathlib import Path
import nltk

# Download NLTK data at startup
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')

# Add src to path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from stt_engine import SpeechToTextEngine
from text_processor import TextProcessor
from llm_formatter import LLMFormatter

# Page configuration
st.set_page_config(
    page_title="Lecture AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-blue: #1f77b4;
        --secondary-blue: #0d47a1;
        --accent-color: #ff6b6b;
        --success-color: #2ecc71;
        --bg-light: #f8f9fa;
        --text-dark: #2c3e50;
    }
    
    /* Main title */
    .main-title {
        text-align: center;
        color: #0d47a1;
        margin-bottom: 30px;
        font-size: 2.5em;
        font-weight: bold;
    }
    
    /* Step headers with better contrast */
    .step-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 15px 20px;
        border-radius: 8px;
        margin: 25px 0 15px 0;
        color: white;
        font-weight: bold;
        font-size: 1.1em;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* File uploader */
    .uploadedfile {
        background-color: #e8f4f8 !important;
        border: 2px solid #667eea !important;
        border-radius: 8px !important;
        padding: 10px !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 30px !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        box-shadow: 0 6px 12px rgba(102, 126, 234, 0.4) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Text areas */
    .stTextArea > textarea {
        background-color: #f8f9fa !important;
        border: 2px solid #667eea !important;
        border-radius: 8px !important;
        color: #2c3e50 !important;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background-color: #e8f4f8 !important;
        border-radius: 8px !important;
        border-left: 4px solid #667eea !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] button {
        background-color: #f0f2f6 !important;
        color: #2c3e50 !important;
        border-radius: 8px 8px 0 0 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #667eea !important;
        color: white !important;
    }
    
    /* Metrics */
    .stMetric {
        background: linear-gradient(135deg, #f0f4ff 0%, #e8ecff 100%) !important;
        padding: 20px !important;
        border-radius: 12px !important;
        border-left: 5px solid #667eea !important;
        border: 2px solid #667eea !important;
        box-shadow: 0 4px 6px rgba(102, 126, 234, 0.1) !important;
    }
    
    .stMetric label {
        color: #2c3e50 !important;
        font-weight: bold !important;
    }
    
    .stMetric > div > div > div > div {
        color: #0d47a1 !important;
        font-weight: bold !important;
        font-size: 1.8em !important;
    }
    
    /* Success messages */
    .stSuccess {
        background-color: #d4edda !important;
        color: #155724 !important;
        border: 2px solid #2ecc71 !important;
        border-radius: 8px !important;
    }
    
    /* Error messages */
    .stError {
        background-color: #f8d7da !important;
        color: #721c24 !important;
        border: 2px solid #ff6b6b !important;
        border-radius: 8px !important;
    }
    
    /* Info messages */
    .stInfo {
        background-color: #d1ecf1 !important;
        color: #0c5460 !important;
        border: 2px solid #667eea !important;
        border-radius: 8px !important;
    }
    
    /* Spinner text */
    .stSpinner {
        color: #667eea !important;
    }
    
    /* Better text contrast */
    body {
        color: #2c3e50 !important;
        background-color: white !important;
    }
    
    /* Markdown improvements */
    .markdown-text-container {
        color: #2c3e50 !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #0d47a1 !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa !important;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("""
<div style='text-align: center; margin-bottom: 30px;'>
    <h1 style='color: #0d47a1; margin: 0; font-size: 2.8em;'>Lecture AI</h1>
    <p style='color: #667eea; font-size: 1.2em; margin: 10px 0; font-weight: 500;'>Voice to Knowledge Converter</p>
    <p style='color: #666; font-size: 0.95em;'>Transform your lecture recordings into structured learning materials</p>
</div>
""", unsafe_allow_html=True)
st.markdown("---")

# Sidebar
st.sidebar.title("📚 Project Navigation")
st.sidebar.markdown("---")
section = st.sidebar.radio(
    "Select Section:",
    ["Home", "Process Audio", "View Results", "About"]
)

# Initialize session state
if 'transcript' not in st.session_state:
    st.session_state.transcript = None
if 'structured_content' not in st.session_state:
    st.session_state.structured_content = None
if 'outputs' not in st.session_state:
    st.session_state.outputs = None

# HOME SECTION
if section == "Home":
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px; border-radius: 15px; color: white; margin-bottom: 30px;'>
        <h2 style='margin-top: 0; font-size: 1.8em;'>Welcome to Lecture AI</h2>
        <p style='font-size: 1.1em; line-height: 1.6;'>Process your lecture recordings and get structured study materials instantly</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Three column layout
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background: white; border: 2px solid #667eea; border-radius: 12px; padding: 25px; height: 100%; box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);'>
            <div style='font-size: 2.5em; margin-bottom: 15px;'>01</div>
            <h3 style='color: #0d47a1; margin-top: 0;'>Upload Audio</h3>
            <p style='color: #666; line-height: 1.6;'>Upload your lecture in MP3, WAV, OGG, or M4A format. Supports up to 30 minutes.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: white; border: 2px solid #667eea; border-radius: 12px; padding: 25px; height: 100%; box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);'>
            <div style='font-size: 2.5em; margin-bottom: 15px;'>02</div>
            <h3 style='color: #0d47a1; margin-top: 0;'>AI Processing</h3>
            <p style='color: #666; line-height: 1.6;'>Automatic transcription, text analysis, and content structuring powered by AI.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background: white; border: 2px solid #667eea; border-radius: 12px; padding: 25px; height: 100%; box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);'>
            <div style='font-size: 2.5em; margin-bottom: 15px;'>03</div>
            <h3 style='color: #0d47a1; margin-top: 0;'>Get Results</h3>
            <p style='color: #666; line-height: 1.6;'>Receive flashcards, detailed notes, and summaries ready for studying.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Features section
    st.markdown("""
    <h2 style='color: #0d47a1; margin-top: 30px;'>Key Features</h2>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='background: #f8f9fa; border-left: 4px solid #667eea; padding: 20px; border-radius: 8px; margin-bottom: 15px;'>
            <h4 style='color: #0d47a1; margin-top: 0;'>Complete Transcription</h4>
            <p style='color: #666; margin: 0;'>100% accurate speech-to-text conversion with zero content loss from your lectures.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background: #f8f9fa; border-left: 4px solid #667eea; padding: 20px; border-radius: 8px; margin-bottom: 15px;'>
            <h4 style='color: #0d47a1; margin-top: 0;'>Smart Text Processing</h4>
            <p style='color: #666; margin: 0;'>Automatic cleaning, entity extraction, and intelligent paragraph structuring.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: #f8f9fa; border-left: 4px solid #667eea; padding: 20px; border-radius: 8px; margin-bottom: 15px;'>
            <h4 style='color: #0d47a1; margin-top: 0;'>Multiple Output Formats</h4>
            <p style='color: #666; margin: 0;'>Get your content as flashcards for revision, detailed notes, or concise summaries.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background: #f8f9fa; border-left: 4px solid #667eea; padding: 20px; border-radius: 8px; margin-bottom: 15px;'>
            <h4 style='color: #0d47a1; margin-top: 0;'>Fast Processing</h4>
            <p style='color: #666; margin: 0;'>Optimized for speed - process 30 minutes of audio in just 2-4 minutes.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # CTA section
    st.markdown("""
    <div style='background: linear-gradient(135deg, #f5f7fa 0%, #f0f2f6 100%); border: 2px solid #667eea; border-radius: 12px; padding: 30px; text-align: center;'>
        <h3 style='color: #0d47a1; margin-top: 0;'>Ready to Get Started?</h3>
        <p style='color: #666; font-size: 1.05em;'>Navigate to "Process Audio" to upload your first lecture</p>
    </div>
    """, unsafe_allow_html=True)

# PROCESS AUDIO SECTION
elif section == "Process Audio":
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 25px; border-radius: 12px; color: white; margin-bottom: 20px;'>
        <h2 style='margin-top: 0;'>Process Your Lecture</h2>
        <p style='margin: 0; opacity: 0.95;'>Supported formats: MP3, WAV, OGG, M4A • Duration: 1-30 minutes</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Step 1: Upload Audio
    st.markdown("""
    <div style='background: white; border: 2px solid #667eea; border-radius: 12px; padding: 20px; margin-bottom: 20px;'>
        <h3 style='color: #0d47a1; margin-top: 0;'>Step 1: Upload Audio File</h3>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Select your lecture audio", type=['mp3', 'wav', 'ogg', 'm4a'])
    
    if uploaded_file is not None:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.success(f"File uploaded: {uploaded_file.name}")
        with col2:
            file_size = len(uploaded_file.getvalue()) / (1024*1024)
            st.info(f"{file_size:.1f} MB")
        
        # Save uploaded file temporarily
        audio_path = f"temp_{uploaded_file.name}"
        with open(audio_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        
        # Step 2: Transcribe
        st.markdown("""
        <div style='background: white; border: 2px solid #667eea; border-radius: 12px; padding: 20px; margin: 25px 0 20px 0;'>
            <h3 style='color: #0d47a1; margin-top: 0;'>Step 2: Transcribe Audio</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            transcribe_btn = st.button("Start Transcription", key="transcribe_btn", use_container_width=True)
        
        if transcribe_btn:
            with st.spinner("Processing audio..."):
                try:
                    stt = SpeechToTextEngine()
                    result = stt.transcribe(audio_path)
                    
                    if result['status'] == 'success':
                        st.session_state.transcript = result['text']
                        duration = result.get('duration', 0)
                        st.success(f"Transcription complete ({duration:.1f}s audio)")
                        
                        with st.expander("View Full Transcript"):
                            st.text_area("Transcript", value=result['text'], height=200, disabled=True, key="transcript_view")
                    else:
                        st.error(f"Error: {result.get('error', 'Unknown error')}")
                except Exception as e:
                    st.error(f"Error during transcription: {str(e)}")
        
        # Step 3: Process Text
        if st.session_state.transcript:
            st.markdown("""
            <div style='background: white; border: 2px solid #667eea; border-radius: 12px; padding: 20px; margin: 25px 0 20px 0;'>
                <h3 style='color: #0d47a1; margin-top: 0;'>Step 3: Process & Structure</h3>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                process_btn = st.button("Process Text", key="process_btn", use_container_width=True)
            
            if process_btn:
                with st.spinner("Analyzing content..."):
                    try:
                        processor = TextProcessor()
                        st.session_state.structured_content = processor.structure_content(
                            st.session_state.transcript
                        )
                        st.success("Text processing complete!")
                        
                        # Display metrics with custom HTML for better visibility
                        st.markdown("""
                        <div style='display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin: 20px 0;'>
                            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 12px; color: white; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                                <div style='font-size: 2em; font-weight: bold;'>{}</div>
                                <div style='font-size: 0.9em; margin-top: 10px; opacity: 0.9;'>Sentences</div>
                            </div>
                            <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 20px; border-radius: 12px; color: white; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                                <div style='font-size: 2em; font-weight: bold;'>{}</div>
                                <div style='font-size: 0.9em; margin-top: 10px; opacity: 0.9;'>Paragraphs</div>
                            </div>
                            <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 20px; border-radius: 12px; color: white; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                                <div style='font-size: 2em; font-weight: bold;'>{}</div>
                                <div style='font-size: 0.9em; margin-top: 10px; opacity: 0.9;'>Key Terms</div>
                            </div>
                        </div>
                        """.format(
                            st.session_state.structured_content['num_sentences'],
                            st.session_state.structured_content['num_paragraphs'],
                            len(st.session_state.structured_content['entities'])
                        ), unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error during processing: {str(e)}")
        
        # Step 4: Generate Outputs
        if st.session_state.structured_content:
            st.markdown("""
            <div style='background: white; border: 2px solid #667eea; border-radius: 12px; padding: 20px; margin: 25px 0 20px 0;'>
                <h3 style='color: #0d47a1; margin-top: 0;'>Step 4: Generate Outputs</h3>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                generate_btn = st.button("Generate All Outputs", key="generate_btn", use_container_width=True)
            
            if generate_btn:
                with st.spinner("Generating materials..."):
                    try:
                        formatter = LLMFormatter()
                        st.session_state.outputs = formatter.format_all_outputs(
                            st.session_state.structured_content
                        )
                        st.success("All outputs generated successfully! Go to 'View Results' to see them.")
                    except Exception as e:
                        st.error(f"Error during generation: {str(e)}")
        
        # Cleanup
        if os.path.exists(audio_path):
            os.remove(audio_path)

# VIEW RESULTS SECTION
elif section == "View Results":
    if st.session_state.outputs is None:
        st.markdown("""
        <div style='background: #fffacd; border: 2px solid #ffd700; border-radius: 12px; padding: 25px; text-align: center;'>
            <h3 style='color: #0d47a1; margin-top: 0;'>No Results Available</h3>
            <p style='color: #666; margin: 0;'>Process an audio file in "Process Audio" section to generate learning materials</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 25px; border-radius: 12px; color: white; margin-bottom: 20px;'>
            <h2 style='margin-top: 0;'>Your Learning Materials</h2>
            <p style='margin: 0; opacity: 0.95;'>All content generated from your lecture</p>
        </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Study Flashcards", "Detailed Notes", "Summary"])
        
        with tab1:
            st.markdown(f"<h3 style='color: #0d47a1;'>Study Flashcards ({len(st.session_state.outputs['flashcards'])} cards)</h3>", unsafe_allow_html=True)
            
            for card in st.session_state.outputs['flashcards']:
                with st.expander(f"Card {card['id']}: {card['question'][:50]}..."):
                    st.markdown(f"""
                    <div style='background: white;'>
                        <div style='border-left: 4px solid #667eea; padding: 15px; margin-bottom: 15px; background: #f8f9fa; border-radius: 8px;'>
                            <p style='color: #666; margin: 0; font-size: 0.9em; text-transform: uppercase; font-weight: bold;'>Question</p>
                            <p style='color: #0d47a1; margin: 5px 0 0 0; font-size: 1.05em;'>{card['question']}</p>
                        </div>
                        <div style='border-left: 4px solid #2ecc71; padding: 15px; background: #f0fdf4; border-radius: 8px;'>
                            <p style='color: #666; margin: 0; font-size: 0.9em; text-transform: uppercase; font-weight: bold;'>Answer</p>
                            <p style='color: #1b5e20; margin: 5px 0 0 0; line-height: 1.6;'>{card['answer']}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        with tab2:
            st.markdown("<h3 style='color: #0d47a1;'>Complete Lecture Notes</h3>", unsafe_allow_html=True)
            st.markdown("""
            <div style='background: white; border: 2px solid #667eea; border-radius: 12px; padding: 25px;'>
            """, unsafe_allow_html=True)
            st.markdown(st.session_state.outputs['notes'])
            st.markdown("</div>", unsafe_allow_html=True)
        
        with tab3:
            st.markdown("<h3 style='color: #0d47a1;'>Key Points Summary</h3>", unsafe_allow_html=True)
            st.markdown("""
            <div style='background: linear-gradient(135deg, #fffacd 0%, #fffde7 100%); border: 2px solid #ffd700; border-radius: 12px; padding: 25px;'>
                <div style='color: #1b5e20; line-height: 1.8;'>
            """, unsafe_allow_html=True)
            st.markdown(st.session_state.outputs['summary'])
            st.markdown("</div></div>", unsafe_allow_html=True)

# ABOUT SECTION
elif section == "About":
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 25px; border-radius: 12px; color: white; margin-bottom: 20px;'>
        <h2 style='margin-top: 0;'>About Lecture AI</h2>
        <p style='margin: 0; opacity: 0.95;'>Intelligent learning assistant powered by AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: white; border: 2px solid #667eea; border-radius: 12px; padding: 25px; margin-bottom: 20px;'>
        <h3 style='color: #0d47a1; margin-top: 0;'>What is Lecture AI?</h3>
        <p style='color: #666; line-height: 1.8;'>
        Lecture AI is an intelligent learning assistant that transforms audio lectures into structured learning materials. 
        Using advanced AI technology, it automatically transcribes, processes, and formats your lecture content into multiple 
        output formats for efficient studying and revision.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='background: white; border: 2px solid #667eea; border-radius: 12px; padding: 20px; margin-bottom: 15px;'>
            <h4 style='color: #0d47a1; margin-top: 0;'>Technology Stack</h4>
            <ul style='color: #666; margin: 0;'>
                <li><strong>Speech Recognition:</strong> OpenAI Whisper</li>
                <li><strong>Text Processing:</strong> NLTK, Python</li>
                <li><strong>Summarization:</strong> Facebook BART</li>
                <li><strong>Web Framework:</strong> Streamlit</li>
                <li><strong>ML Framework:</strong> PyTorch</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: white; border: 2px solid #667eea; border-radius: 12px; padding: 20px; margin-bottom: 15px;'>
            <h4 style='color: #0d47a1; margin-top: 0;'>Key Capabilities</h4>
            <ul style='color: #666; margin: 0;'>
                <li>Transcription up to 30 minutes</li>
                <li>100% accurate text conversion</li>
                <li>Automatic text cleaning</li>
                <li>Entity extraction</li>
                <li>Multiple output formats</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: white; border: 2px solid #667eea; border-radius: 12px; padding: 25px;'>
        <h3 style='color: #0d47a1; margin-top: 0;'>Processing Pipeline</h3>
        <div style='background: #f8f9fa; padding: 15px; border-radius: 8px; font-family: monospace; color: #2c3e50; line-height: 2;'>
            Audio File → Speech-to-Text → Full Transcript → Text Processing → Content Structuring → Output Generation
        </div>
    </div>
    
    <div style='text-align: right; margin-top: 50px; padding-top: 30px; padding-right: 10px; border-top: 1px solid #e0e0e0;'>
        <p style='color: #bbb; font-size: 0.85em; margin: 0; letter-spacing: 1px;'>~ Kartik Yadav</p>
    </div>
    """, unsafe_allow_html=True)

# Lecture AI - Transform Your Lectures

Ever had a pile of lecture recordings and no time to organize them? Yeah, me too. That's why I built **Lecture AI**.

This tool takes your lecture audio and automatically converts it into three useful formats:

- **Flashcards** for quick revision
- **Complete Notes** with full content structured
- **Summary** with just the key points

No manual transcription. No hours of note-taking. Just upload, wait a couple minutes, and get organized study materials.

---

## ⚡ What It Does

1. **Listens to Your Lecture** - Upload MP3, WAV, OGG, or M4A (up to 30 minutes)
2. **Transcribes Automatically** - Converts speech to text using AI
3. **Organizes Everything** - Cleans up the text, extracts key points
4. **Generates 3 Formats** - Flashcards, detailed notes, and summary all at once

**Result:** Professional study materials in 2-4 minutes instead of spending hours manually.

---

## 🚀 How to Use

### Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/Lecture-AI.git
cd Lecture-AI

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

---

## 📋 Features

✅ **Automatic Speech Recognition** - Whisper AI converts audio to text  
✅ **Smart Text Processing** - Cleans up transcription, extracts key points  
✅ **Multiple Output Formats** - Get flashcards, notes, and summary  
✅ **Fast Processing** - 30 min audio processed in 2-4 minutes (CPU)  
✅ **Clean UI** - Professional interface, easy to use  
✅ **Free & Open Source** - No subscriptions, completely offline

---

## 🛠️ Built With

- **Streamlit** - Web interface
- **OpenAI Whisper** - Speech-to-text
- **NLTK** - Text processing
- **Facebook BART** - Summarization
- **PyTorch** - ML framework

---

## 📊 Tech Stack

| Component       | Technology             |
| --------------- | ---------------------- |
| Frontend        | Streamlit              |
| STT             | Whisper (Hugging Face) |
| Text Processing | NLTK                   |
| Summarization   | Facebook BART          |
| ML Framework    | PyTorch                |

---

## 💾 File Structure

```
Lecture-AI/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── src/
    ├── stt_engine.py      # Speech-to-text processing
    ├── text_processor.py  # Text cleaning & structuring
    └── llm_formatter.py   # Output generation
```

---

## 📝 How It Works

```
Your Lecture Audio
        ↓
Speech-to-Text Engine
        ↓
Complete Transcript
        ↓
Text Cleaning & Processing
        ↓
Content Analysis
        ↓
Generate 3 Formats
├── Flashcards (Q&A)
├── Detailed Notes
└── Summary
```

---

## ⏱️ Processing Times

| Audio Length | Processing Time |
| ------------ | --------------- |
| 1 min        | 5-10 seconds    |
| 5 min        | 20-30 seconds   |
| 10 min       | 40-60 seconds   |
| 15 min       | 1-2 minutes     |
| 30 min       | 2-4 minutes     |

_Times vary based on your computer. GPU will be 2-3x faster._

---

## 🎓 Use Cases

- **Students** - Convert lecture recordings into revision materials
- **Teachers** - Create study guides from your own lectures
- **Researchers** - Transcribe interviews and seminars
- **Online Learning** - Process course videos into notes

---

## 🐛 Troubleshooting

**Models taking too long to download?**

- First run downloads ~1GB of models. This is normal, be patient.

**Audio not recognized?**

- Convert to MP3 or WAV using Audacity (free)

**Out of memory?**

- Use shorter audio files (split into 30min chunks)

**Not working?**

- Make sure virtual environment is activated
- Check internet (models auto-download)
- Try a short 1-2 min test file first

---

## 💡 Why I Built This

As a student, I realized converting lecture recordings into study materials manually takes hours. I wanted a tool that could do it automatically - accurately, quickly, and for free.

The goal is simple: **Make studying more efficient.**

---

## 📄 License

Open source - Available for personal and educational use.

---

## 👤 Author

**Kartik Yadav**

Built with ❤️ for students and learners everywhere.

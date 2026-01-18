# 🎓 Lecture AI – Automated Lecture Understanding System

Lecture AI is an **AI/ML-focused project** developed as part of an **AIML internship learning track**. It transforms raw lecture audio into structured academic content using **pre-trained speech and language models**.
The primary focus is on **AI pipeline design, model integration, and knowledge representation**, not UI/UX.

---

## 🔗 Live Demo (Streamlit App)

👉 **Try the application here:**
[https://lecture-ai-kartik-y-01.streamlit.app/](https://lecture-ai-kartik-y-01.streamlit.app/)

> Note: The UI is intentionally minimal to keep the focus on AI/ML functionality.

---

## 🎯 Project Objective

To automate the conversion of lecture recordings into usable study material, reducing manual effort and improving learning efficiency using modern AI models.

---

## 🧠 Core Features

The system automatically generates:

* 📘 **Detailed Notes** for deep conceptual understanding
* 🧠 **Flashcards** for quick revision
* 📝 **Concise Summary** for rapid recall

All outputs are generated directly from raw lecture audio using pre-trained AI models.

---

## ⚙️ System Workflow

```
Lecture Audio
        ↓
Speech-to-Text (Whisper ASR)
        ↓
Raw Transcript
        ↓
Text Cleaning & Structuring
        ↓
Knowledge Representation Layer
        ↓
├── Flashcards
├── Complete Notes
└── Summary
```

---

## 🔬 AI / ML Focus

This project is designed to demonstrate **practical AI pipeline implementation**:

* Uses **pre-trained models** (no rule-based logic)
* Integrates **Speech-to-Text and NLP models**
* Emphasizes **pipeline orchestration**
* Highlights **model capabilities and limitations**
* UI kept minimal to prioritize AI learning outcomes

---

## 🛠️ Technologies Used

* **Python**
* **Streamlit** – Lightweight interface for interaction
* **Hugging Face Transformers**

  * Whisper (Speech-to-Text)
  * FLAN-T5 (Text Generation)
* **PyTorch** – Model execution backend

---

## 📊 Tech Stack

| Component       | Technology             |
| --------------- | ---------------------- |
| Frontend        | Streamlit              |
| Speech-to-Text  | Whisper (Hugging Face) |
| Text Generation | FLAN-T5                |
| ML Backend      | PyTorch                |

---

## 📁 Project Structure

```
Lecture-AI/
├── app.py                  # Streamlit application
├── stt.py                  # Speech-to-text module
├── text_processing.py      # Text cleaning & structuring
├── knowledge.py            # Notes, summary & flashcard generation
├── requirements.txt        # Dependencies
└── README.md               # Documentation
```

---

## 🚀 How to Run Locally

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

---

## 🎓 Use Cases

* Students converting lecture recordings into study material
* Demonstration of AI/ML pipeline implementation
* Academic projects and AIML internship submissions

---

## 🧩 Scope & Limitations

* UI/UX is **not the primary focus**
* Model training is **out of scope**
* Performance depends on **pre-trained models and hardware**

---

## 📌 Learning Outcomes

* Hands-on experience with AI pipelines
* Understanding real-world usage of pre-trained ML models
* Exposure to speech processing and NLP workflows

---

## 👤 Author

**Kartik Yadav**

---

## 📄 License

Open-source for **educational and academic use**.

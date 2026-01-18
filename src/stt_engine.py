# Speech-to-Text Engine
# Using Hugging Face Whisper model

import librosa
import torch
from transformers import pipeline

class SpeechToTextEngine:
    def __init__(self, model_name="openai/whisper-tiny"):
        """
        Initialize STT engine with Whisper model
        model_name options: whisper-tiny (fastest), whisper-base, whisper-small
        Using whisper-tiny for 5-30min optimal speed on CPU
        """
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipe = pipeline(
            "automatic-speech-recognition",
            model=model_name,
            device=0 if self.device == "cuda" else -1,
            chunk_length_s=30  # Process in 30-second chunks
        )
    
    def transcribe(self, audio_path):
        """
        Transcribe audio file to text (optimized for 5-30 min)
        Args:
            audio_path: Path to audio file (.mp3, .wav, etc.)
        Returns:
            dict: {
                'text': full transcript,
                'duration': audio duration in seconds
            }
        """
        try:
            # Load audio (16kHz sample rate)
            audio, sr = librosa.load(audio_path, sr=16000)
            
            # Limit to 30 minutes for optimal processing
            max_duration = 1800  # 30 minutes
            if len(audio) / sr > max_duration:
                audio = audio[:max_duration * sr]
            
            # Transcribe with chunking for speed
            result = self.pipe(audio)
            
            return {
                'text': result['text'],
                'status': 'success',
                'duration': len(audio) / sr
            }
        except Exception as e:
            return {
                'text': None,
                'error': str(e),
                'status': 'failed'
            }

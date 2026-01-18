# Text Processing and Structuring
# Cleaning, segmentation, and structure extraction

import re
from nltk.tokenize import sent_tokenize
import nltk

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')

class TextProcessor:
    def __init__(self):
        """Initialize text processor"""
        pass
    
    def clean_text(self, text):
        """
        Remove noise from transcript
        - Remove extra whitespace
        - Remove special characters
        - Fix common STT errors
        """
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text)
        
        # Remove URLs
        text = re.sub(r'http\S+|www.\S+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        return text.strip()
    
    def segment_sentences(self, text):
        """Segment text into sentences"""
        sentences = sent_tokenize(text)
        return sentences
    
    def segment_paragraphs(self, text, sentences_per_para=3):
        """Group sentences into paragraphs (optimized for speed)"""
        sentences = self.segment_sentences(text)
        paragraphs = []
        
        for i in range(0, len(sentences), sentences_per_para):
            para = ' '.join(sentences[i:i + sentences_per_para])
            paragraphs.append(para)
        
        return paragraphs
    
    def extract_key_entities(self, text):
        """Extract important phrases (simple method)"""
        # Simple entity extraction - extract all-caps words and proper nouns
        words = text.split()
        entities = []
        
        for i, word in enumerate(words):
            # Check for all-caps words
            if word.isupper() and len(word) > 2:
                entities.append((word, "TERM"))
            # Check for capitalized words (potential proper nouns)
            elif word[0].isupper() and i > 0 and not word[0].isupper() == words[i-1][-1] == '.':
                if len(word) > 3:
                    entities.append((word, "PERSON/ORG"))
        
        return entities[:20]  # Limit to top 20
    
    def structure_content(self, text):
        """
        Main structuring pipeline
        Returns structured representation
        """
        cleaned = self.clean_text(text)
        sentences = self.segment_sentences(cleaned)
        paragraphs = self.segment_paragraphs(cleaned)
        entities = self.extract_key_entities(cleaned)
        
        return {
            'original': text,
            'cleaned': cleaned,
            'sentences': sentences,
            'paragraphs': paragraphs,
            'entities': entities,
            'num_sentences': len(sentences),
            'num_paragraphs': len(paragraphs)
        }

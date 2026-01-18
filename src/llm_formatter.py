# LLM-based Content Formatter
# Generates flashcards, notes, and summaries using Hugging Face models

from transformers import pipeline

class LLMFormatter:
    def __init__(self):
        """Initialize LLM for content generation (optimized for speed)"""
        # Use krega smaller, faster summarization model
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)
    
    def generate_summary(self, text, max_length=200, min_length=100):
        """
        Generate concise summary from text (optimized)
        Args:
            text: Input text
            max_length: Maximum length of summary
            min_length: Minimum length of summary
        Returns:
            str: Summary text
        """
        try:
            # Split text if too long
            if len(text.split()) > 1024:
                text = ' '.join(text.split()[:1024])
            
            summary = self.summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
            return summary[0]['summary_text']
        except Exception as e:
            
            sentences = text.split('.')[:3]
            return '. '.join(sentences) + '.'
    
    def generate_flashcards(self, paragraphs, num_cards=15):
        """
        Generate detailed flashcards from content
        Each paragraph becomes a flashcard (question-answer)
        """
        if num_cards is None:
            num_cards = min(15, len(paragraphs))
        
        flashcards = []
        for i, para in enumerate(paragraphs[:num_cards]):
            
            sentences = para.split('.')
            
            if len(sentences) > 1:
                
                question = sentences[0].strip() + "?"
                answer = para.strip()
            else:
                question = "What is " + para[:30] + "?"
                answer = para
            
            flashcards.append({
                'id': i + 1,
                'question': question,
                'answer': answer
            })
        
        return flashcards
    
    def generate_structured_notes(self, structured_content):
        """
        Generate detailed, well-structured notes from content
        """
        notes = []
        
        # Header
        notes.append("# 📚 Lecture Notes\n")
        notes.append(f"**Total Sentences:** {structured_content['num_sentences']} | ")
        notes.append(f"**Total Paragraphs:** {structured_content['num_paragraphs']}\n\n")
        
        # Key Entities
        if structured_content['entities']:
            notes.append("## 🔑 Key Terms & Concepts\n")
            for entity, label in structured_content['entities'][:15]:
                notes.append(f"- **{entity}** ({label})\n")
            notes.append("\n")
        
        # Main Content with Better formating ke saath 
        notes.append("## 📖 Detailed Content\n")
        for i, para in enumerate(structured_content['paragraphs'][:20], 1):
            notes.append(f"\n### Section {i}\n")
            notes.append(f"{para}\n")
        
        return ''.join(notes)
    
    def format_all_outputs(self, structured_content):
        """
        Generate all 3 output formats at once (fast)
        """
        full_text = structured_content['cleaned']
        paragraphs = structured_content['paragraphs']
        
        return {
            'summary': self.generate_summary(full_text),
            'flashcards': self.generate_flashcards(paragraphs),
            'notes': self.generate_structured_notes(structured_content)
        }

import re
import functools
import time
from sentence_transformers import SentenceTransformer

class ATSOptimizer:
    _model_instance = None

    @classmethod
    def get_model(cls, model_name='all-MiniLM-L6-v2'):
        """
        Singleton pattern for memory handling. 
        Ensures the 80MB+ transformer model is loaded into RAM only once per worker,
        rather than reloading it for every single resume.
        """
        if cls._model_instance is None:
            cls._model_instance = SentenceTransformer(model_name)
        return cls._model_instance

    @staticmethod
    def clean_noisy_text(raw_text):
        """
        Improves noisy resume handling by sanitizing OCR and PDF extraction artifacts.
        Removes non-ASCII characters, broken bullet points, and erratic spacing.
        """
        if not raw_text:
            return ""
        
        # Remove non-ASCII characters (often caused by custom PDF fonts)
        text = re.sub(r'[^\x00-\x7F]+', ' ', raw_text)
        # Remove erratic spacing and excessive newlines
        text = re.sub(r'\s+', ' ', text)
        # Clean up corrupted bullet points and list artifacts
        text = re.sub(r'[\*\-\u2022\u2023\u25E6\u2043]', '', text)
        
        return text.strip()

    @staticmethod
    @functools.lru_cache(maxsize=2000)
    def get_cached_embedding(text_chunk):
        """
        Reduces model response time.
        Caches the vector embeddings for up to 2000 frequently seen phrases (e.g., "Python", "Data Analysis").
        If a phrase is seen again, it retrieves the vector from memory instantly instead of recalculating it.
        """
        model = ATSOptimizer.get_model()
        return model.encode(text_chunk)

# Test execution
if __name__ == "__main__":
    print("Initializing optimizer test...")
    
    # 1. Test Text Sanitizer
    noisy_string = "P y t h o n \u2022 Developer   \n\n  with \u25E6 Data Science experience\u2122"
    cleaned = ATSOptimizer.clean_noisy_text(noisy_string)
    print(f"\n[Text Sanitization]\nOriginal: {repr(noisy_string)}\nCleaned:  {repr(cleaned)}")
    
    # 2. Test Caching Speed
    print("\n[Caching Speed Test]")
    skill = "Machine Learning Pipeline"
    
    # First call (Calculates embedding)
    start = time.time()
    ATSOptimizer.get_cached_embedding(skill)
    first_duration = time.time() - start
    print(f"First call (Model Computation): {first_duration:.4f} seconds")
    
    # Second call (Retrieves from cache)
    start = time.time()
    ATSOptimizer.get_cached_embedding(skill)
    second_duration = time.time() - start
    print(f"Second call (Cache Retrieval):  {second_duration:.6f} seconds")
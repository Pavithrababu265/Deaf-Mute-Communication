class TextProcessor:
    def __init__(self):
        self.translator = None        
        self.languages = {
            'English': {'text': 'en', 'speech': 'en-IN'},
            'Tamil': {'text': 'ta', 'speech': 'ta-IN'},
            'Hindi': {'text': 'hi', 'speech': 'hi-IN'}
        }
        self.current_language = 'English'

    def translate_text(self, text, target_language):
        if target_language not in self.languages:
            return text
        
        dest_code = self.languages[target_language]['text']
        # Don't translate if the source text is short/empty or if target is English and we assume source is English for now.
        if not text or len(text.strip()) == 0:
            return text
            
        try:
            if self.translator is None:
                from googletrans import Translator
                self.translator = Translator()
                
            translation = self.translator.translate(text, dest=dest_code)
            return translation.text
        except Exception as e:
            print(f"Translation Error: {e}")
            return text

            
    def analyze_emotion(self, text):
        """
        Simple keyword-based sentiment analysis/emotion detection.
        Returns: str (Happy, Sad, Angry, Surprise, Fear, Neutral)
        """
        text = text.lower()
        
        # Keyword Dictionaries
        keywords = {
            'happy': ['happy', 'good', 'great', 'joy', 'awesome', 'nice', 'love', 'excited', 'wonderful', 'smile'],
            'sad': ['sad', 'bad', 'sorry', 'unhappy', 'depressed', 'grief', 'cry', 'tears', 'upset', 'pain'],
            'angry': ['angry', 'mad', 'hate', 'furious', 'rage', 'fight', 'argue', 'annoying', 'stupid'],
            'surprise': ['wow', 'omg', 'surprise', 'shock', 'amazing', 'unbelievable', 'really'],
            'fear': ['scared', 'fear', 'afraid', 'terrified', 'horror', 'help', 'danger', 'panic']
        }
        
        # Count matches
        scores = {emotion: 0 for emotion in keywords}
        
        words = text.split()
        for word in words:
            for emotion, emot_words in keywords.items():
                if word in emot_words:
                    scores[emotion] += 1
                    
        # Find max score
        best_emotion = "Neutral"
        max_score = 0
        
        for emotion, score in scores.items():
            if score > max_score:
                max_score = score
                best_emotion = emotion.capitalize()
                
        return best_emotion

if __name__ == "__main__":
    tp = TextProcessor()
    text = "Hello, how are you?"
    print(f"Original: {text}")
    print(f"Tamil: {tp.translate_text(text, 'Tamil')}")
    print(f"Hindi: {tp.translate_text(text, 'Hindi')}")

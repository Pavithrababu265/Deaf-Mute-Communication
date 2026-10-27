from src.text_processing import TextProcessor

tp = TextProcessor()

test_cases = [
    ("I am so happy today", "Happy"),
    ("Refer to the sad news", "Sad"),
    ("I hate this stupid thing", "Angry"),
    ("Wow that is amazing", "Surprise"),
    ("I am scared of ghosts", "Fear"),
    ("Hello world", "Neutral")
]

print("Running Sentiment Tests...")
for text, expected in test_cases:
    result = tp.analyze_emotion(text)
    status = "PASS" if result == expected else f"FAIL (Expected {expected}, Got {result})"
    print(f"'{text}' -> {result} : {status}")

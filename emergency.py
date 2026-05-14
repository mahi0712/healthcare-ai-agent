danger_words = [

    "chest pain",
    "heart attack",
    "difficulty breathing",
    "stroke",
    "unconscious"
]

def detect_emergency(text):

    text = text.lower()

    for word in danger_words:

        if word in text:

            return True

    return False
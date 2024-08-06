from transliterate import translit

def normalize_text(text):
    text = text.lower()
    transliterated_text = translit(text, 'ru', reversed=True)
    return transliterated_text

from fastapi import APIRouter, HTTPException, Query
import random
from google.cloud import translate_v2 as translate
import os
from data.word_bank import words

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/Users/Totev/Google Cloud Services ID JSON/Cloud Translation API Service Agent/igneous-etching-424611-p2-63cbb04885fd.json"

words_router = APIRouter(prefix="/words")

languages = ["es", "fr", "de", "it", "pt"]


translate_client = translate.Client()


@words_router.get("/random", tags=["Words"])
def random_word(lang: str = Query(None, title="language", description="The language code(es, fr, de, it, pt)")):
    """
        Get a random word from the specified language and its English translation.

        This endpoint returns a random word from the specified language, along with its translation to English taken
        from Google Cloud Services' Translation API.
        If no language is specified, a random language from the available options (es, fr, de, it, pt) will be selected.

        Parameters:
        lang (str): The language code for the word to be returned. Supported languages are:
                    - es: Spanish
                    - fr: French
                    - de: German
                    - it: Italian
                    - pt: Portuguese

        Returns:
        dict: A dictionary containing the following keys:
              - word (str): The random word in the specified language.
              - language (str): The language code of the returned word.
              - definition (str): The English translation of the word.
        """
    if lang and lang not in languages:
        raise HTTPException(status_code=400, detail="Invalid language code")

    if not lang:
        lang = random.choice(languages)

    word = random.choice(words[lang])

    try:
        response = translate_client.translate(word, source_language=lang, target_language='en')
        translated_text = response['translatedText']
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"word": word, "language": lang, "definition": translated_text}

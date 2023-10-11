import pytest
from .translator import translate_using_wrapper  # Adjust the import based on where your function is located

def test_translate_using_wrapper():
    # Test data
    word = "hello"
    dest = "ru"
    src = "en"

    # Call the function
    # definitions, synonyms, translations, examples = translate_using_wrapper(word, dest, src)
    definitions, translations = translate_using_wrapper(word, dest, src)

    assert "здороваться" in translations
    assert "greet" in translations["здороваться"]
    assert "used as a greeting or to begin a phone conversation." in definitions
    assert "hello there, Katie!" == definitions["used as a greeting or to begin a phone conversation."]

def test_translate_using_wrapper2():
    # Test data
    word = "hi"
    dest = "ru"
    src = "en"

    # Call the function
    # definitions, synonyms, translations, examples = translate_using_wrapper(word, dest, src)
    definitions, translations = translate_using_wrapper(word, dest, src)

    assert "привет" in translations 
    assert "used as a friendly greeting or to attract attention." in definitions
    assert "“Hi there. How was the flight?”" == definitions["used as a friendly greeting or to attract attention."]

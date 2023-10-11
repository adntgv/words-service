from typing import Callable
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.models import Word, Definition, Translation, Synonym
from database.database import SessionLocal
from database.cache import cache
from services.translator import translate_using_wrapper
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# FastAPI routes
@router.get("/word/{word}")
def get_word_details(word: str, dest: str | None = 'ru', src: str | None = 'en', db: Session = Depends(get_db)):
    try:
        # Check cache
        key = f'{word}-{src}-{dest}'
        cached_word = cache.get(key)
        if cached_word:
            logger.info(f"Cache hit for word: {word}")
            return cached_word

        # Check database
        db_word = db.query(Word).filter(Word.word_text == word).first()
        if db_word:
            logger.info(f"Database hit for word: {word}")
            # Cache and return
            cache.set(key, db_word)
            return db_word

        # Scrape Google Translate
        definitions_dict, translations_dict = translate_using_wrapper(word, dest, src)

        # Save to database
        new_word = Word(word_text=word)
        for definition, example in definitions_dict.items():
            new_word.definitions.append(Definition(definition_text=definition, example_text=example))
        
        for translation, synonyms in translations_dict.items():
            new_translation = Translation(translated_text=translation, language=dest)
            for synonym in synonyms:
                new_translation.synonyms.append(Synonym(synonym_text=synonym))
            new_word.translations.append(new_translation)

        db.add(new_word)
        db.commit()
        logger.info(f"Saved word: {word} to database")

        # Cache and return
        cache.set(key, new_word)
        return new_word

    except Exception as e:
        logger.error(f"Error fetching details for word: {word}. Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/words")
def get_words(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try:
        words = db.query(Word).offset(skip).limit(limit).all()
        return words
    except Exception as e:
        logger.error(f"Error fetching words. Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/word/{word}")
def delete_word(word: str, db: Session = Depends(get_db)):
    try:
        db_word = db.query(Word).filter(Word.word_text == word).first()
        if not db_word:
            raise HTTPException(status_code=404, detail="Word not found")
        db.delete(db_word)
        db.commit()
        cache.delete(word)  # Invalidate cache
        logger.info(f"Deleted word: {word} from database and cache")
        return {"message": "Word deleted successfully"}
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error deleting word: {word}. Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

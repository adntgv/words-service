from typing import Callable, List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.models import Word, Definition, Translation, Synonym
from routes.models import WordSchema, DefinitionSchema, TranslationSchema, SynonymSchema
from database.database import SessionLocal
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

@router.get("/word/{word}", response_model=WordSchema)
def get_word_details(word: str, dest: str | None = 'ru', src: str | None = 'en', db: Session = Depends(get_db)):
    try:
        # Check database
        db_word = db.query(Word).filter(Word.word_text == word).first()
        if db_word:
            logger.info(f"Database hit for word: {word}")
            word_schema = to_word_schema(db_word)
            return word_schema

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

        # Convert to Pydantic model, cache, and return
        word_schema = to_word_schema(new_word)
        return word_schema

    except Exception as e:
        logger.error(f"Error fetching details for word: {word}. Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
        
@router.get("/words", response_model=List[WordSchema])
def get_words(page: int = 1, limit: int = 10, filter: str = '', db: Session = Depends(get_db)):
    skip = (page-1)*limit
    try:
        query = db.query(Word)
        if filter != '':
            query = query.filter(Word.word_text.like(f"%{filter}%"))
        words = query.offset(skip).limit(limit).all()
        return [to_word_schema(word) for word in words]
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
        logger.info(f"Deleted word: {word} from database and cache")
        return {"message": "Word deleted successfully"}
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error deleting word: {word}. Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def to_definition_schema(definition: Definition) -> DefinitionSchema:
    return DefinitionSchema(
        definition_id=definition.definition_id,
        definition_text=definition.definition_text,
        example_text=definition.example_text
    )

def to_synonym_schema(synonym: Synonym) -> SynonymSchema:
    return SynonymSchema(
        synonym_id=synonym.synonym_id,
        synonym_text=synonym.synonym_text
    )

def to_translation_schema(translation: Translation) -> TranslationSchema:
    return TranslationSchema(
        translation_id=translation.translation_id,
        translated_text=translation.translated_text,
        language=translation.language,
        synonyms=[to_synonym_schema(synonym) for synonym in translation.synonyms]
    )

def to_word_schema(word: Word) -> WordSchema:
    return WordSchema(
        word_id=word.word_id,
        word_text=word.word_text,
        definitions=[to_definition_schema(definition) for definition in word.definitions],
        translations=[to_translation_schema(translation) for translation in word.translations]
    )

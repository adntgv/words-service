from pydantic import BaseModel
from typing import List, Optional

class DefinitionSchema(BaseModel):
    definition_id: int
    definition_text: str
    example_text:  Optional[str] 

class SynonymSchema(BaseModel):
    synonym_id: int
    synonym_text: str

class TranslationSchema(BaseModel):
    translation_id: int
    translated_text: str
    language: str
    synonyms: List[SynonymSchema]

class WordSchema(BaseModel):
    word_id: int
    word_text: str
    definitions: List[DefinitionSchema]
    translations: List[TranslationSchema]

    class Config:
        orm_mode = True
        from_attributes = True

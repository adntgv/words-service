from sqlalchemy import Column, Integer, String, ForeignKey, Text, Date
from sqlalchemy.orm import relationship
from database.database import Base, engine

# Database models
class Word(Base):
    __tablename__ = "words"

    word_id = Column(Integer, primary_key=True, index=True)
    word_text = Column(String, unique=True, index=True)
    date_added = Column(Date)

    definitions = relationship("Definition", back_populates="word")
    translations = relationship("Translation", back_populates="word")

class Definition(Base):
    __tablename__ = "definitions"

    definition_id = Column(Integer, primary_key=True)
    word_id = Column(Integer, ForeignKey("words.word_id"))
    definition_text = Column(Text)
    example_text = Column(Text)  # Added this column to store example for each definition

    word = relationship("Word", back_populates="definitions")

class Translation(Base):
    __tablename__ = "translations"

    translation_id = Column(Integer, primary_key=True)
    word_id = Column(Integer, ForeignKey("words.word_id"))
    translated_text = Column(Text)
    language = Column(String)

    synonyms = relationship("Synonym", back_populates="translation")  # Added this relationship

    word = relationship("Word", back_populates="translations")

class Synonym(Base):
    __tablename__ = "synonyms"

    synonym_id = Column(Integer, primary_key=True)
    translation_id = Column(Integer, ForeignKey("translations.translation_id"))  # Changed this FK to translations
    synonym_text = Column(Text)

    translation = relationship("Translation", back_populates="synonyms")  # Changed this relationship

# Create tables
Base.metadata.create_all(bind=engine)

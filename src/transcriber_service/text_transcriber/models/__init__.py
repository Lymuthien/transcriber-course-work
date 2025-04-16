"""
Package: models

This package provides various components for processing audio, including:
- Speech-to-text transcription with Whisper and Faster Whisper.
- Stopword removal using the Natasha NLP library.
- Speaker separation using PyAnnote's diarization pipeline.

Modules
-------
natasha_stopwords_remover:
    Handles text processing and stopword removal.
whisper_processor:
    Provides transcription using OpenAI's Whisper model.
faster_whisper_processor:
    Offers fast transcription via the Faster Whisper library.
voice_separator:
    Implements speaker separation using PyAnnote.
"""

from .faster_whisper_processor import *
from .whisper_processor import *
from .natasha_stopwords_remover import *
from .voice_separator import *

__all__ = ['FasterWhisperProcessor', 'NatashaStopwordsRemover', 'WhisperProcessor', 'VoiceSeparatorWithPyAnnote']

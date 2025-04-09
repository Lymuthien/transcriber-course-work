"""
Package: text_transcriber.builders
-----------------------------------

This package provides utility classes for directing and managing audio-related
processing tasks, such as transcription and speaker diarization.

Modules:
    - transcribe_processor_director: Provides `TranscribeProcessorDirector` for transcription tasks.
    - voice_separator_director: Provides `VoiceSeparatorDirector` for speaker diarization.
"""

from .transcribe_processor_director import *
from .voice_separator_director import *

__all__ = ["TranscribeProcessorDirector", "VoiceSeparatorDirector"]

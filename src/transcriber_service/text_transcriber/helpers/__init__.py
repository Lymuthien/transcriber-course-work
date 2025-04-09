"""
Package: helpers
----------------

This package provides utility tools and mixins for audio processing tasks.

Modules:
--------
    - audio_processing_mixin: Defines the `AudioProcessingMixin` class, which includes reusable static methods
      for audio data handling, such as resampling, mono conversion, and audio stream extraction.

Classes:
--------
    - AudioProcessingMixin: A mixin that provides shared static methods for common audio processing operations.
"""

from .audio_processing_mixin import *

__all__ = ['AudioProcessingMixin']

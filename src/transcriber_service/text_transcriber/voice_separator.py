from copy import deepcopy
from typing import Any
from pyannote.audio import Pipeline
import torch
import librosa
import numpy as np
import soundfile as sf
from io import BytesIO
from .interfaces import IVoiceSeparator


class VoiceSeparatorWithPyAnnote(IVoiceSeparator):
    def __init__(self,
                 token: str,
                 model_name: str = "pyannote/speaker-diarization-3.1"):
        """
        Initialize PyAnnote pipeline for speaker diarization.

        :param token: HuggingFace token for speaker diarization.
        :param model_name: HuggingFace model name for speaker diarization.
        """

        try:
            self._pipeline = Pipeline.from_pretrained(model_name,
                                                      use_auth_token=token)

            self._device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self._pipeline.to(self._device)

        except Exception as e:
            raise RuntimeError(f"Failed to load PyAnnote pipeline: {e}")

    def separate_speakers(self,
                          content: bytes,
                          max_speakers: int = None) -> list[dict]:
        """
        Perform speaker diarization on input audio.

        :param content: Audio bytes (e.g., wav format).
        :param max_speakers: Max number of speakers expected in the audio.
        :return: List of segments with speaker information and timestamps.
        """

        audio_stream = BytesIO(content)
        audio, sr = sf.read(audio_stream)

        if sr != 16000:
            audio = librosa.resample(audio, orig_sr=sr, target_sr=16000)

        if len(audio.shape) > 1:
            audio = np.mean(audio, axis=1)

        audio = audio.astype(np.float32)

        timeline = self._pipeline({
            "waveform": torch.tensor(audio).unsqueeze(0),
            "sample_rate": 16000,
        })

        speaker_segments = []
        for speech_segment in timeline.itertracks(yield_label=True):
            segment, _, speaker = speech_segment
            speaker_segments.append({
                "start": segment.start,
                "end": segment.end,
                "speaker": speaker,
            })

        return self._unite_segments(speaker_segments)

    @staticmethod
    def _unite_segments(segments: list[dict[str, Any]]) -> list[dict[str, Any]]:
        speaker_segments = deepcopy(segments)

        prev_segment = speaker_segments[0]
        for segment in speaker_segments[1:]:
            if prev_segment["speaker"] == segment["speaker"]:
                segment["start"] = prev_segment["start"]
                speaker_segments.remove(prev_segment)

            prev_segment = segment

        return speaker_segments

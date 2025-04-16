from io import BytesIO
import soundfile as sf
import time

from .models import VoiceSeparatorWithPyAnnote, NatashaStopwordsRemover, WhisperProcessor, FasterWhisperProcessor
from .builders import TranscribeProcessorDirector, VoiceSeparatorDirector


class Transcriber(object):
    def __init__(self,
                 token: str,
                 whisper_model: str = "medium",
                 speaker_diarization_model: str = "pyannote/speaker-diarization-3.1",
                 use_faster_whisper: bool = False):
        whisper_processor = WhisperProcessor(model_size=whisper_model) if not use_faster_whisper \
            else FasterWhisperProcessor(model_size=whisper_model)
        self._whisper_director = TranscribeProcessorDirector(whisper_processor)

        voice_processor = VoiceSeparatorWithPyAnnote(token, model_name=speaker_diarization_model)
        self._voice_sep_director = VoiceSeparatorDirector(voice_processor)

        self._natasha_processor = NatashaStopwordsRemover()

    def transcribe(self,
                   content: bytes,
                   language: str | None = None,
                   max_speakers: str | None = None) -> str:
        start_time = time.time()
        try:
            segments = self._voice_sep_director.separate_speakers(content, max_speakers=max_speakers)
        except Exception as e:
            raise RuntimeError(f"Error while separating by voices: {e}")
        end_time = time.time()
        print(f"Time for voice separation: {end_time - start_time}")

        transcription_results = []

        start_time1 = time.time()
        for segment in segments:
            start_time = segment["start"]
            end_time = segment["end"]
            speaker = segment["speaker"]

            segment_audio = self._extract_audio_segment(content, start_time, end_time)

            try:
                segment_text, detected_language = self._whisper_director.transcribe_audio(
                    content=segment_audio,
                    language=language
                )
                transcription_results.append(f"[{speaker}] {segment_text.strip()}")
            except Exception as e:
                raise RuntimeError(f"Error while transcribe segment {speaker}: {e}")

        end_time1 = time.time()
        print(f"Time for transcription: {end_time1 - start_time1}")

        full_transcription = "\n\n".join(transcription_results)

        return full_transcription

    def remove_stopwords(self,
                         text: str,
                         remove_swear_words: bool = True,
                         go_few_times: bool = False) -> str:
        return self._natasha_processor.remove_stopwords(
            text=text,
            remove_swear_words=remove_swear_words,
            go_few_times=go_few_times
        )

    def remove_words(self,
                     text: str,
                     words: list[str]) -> str:
        return self._natasha_processor.remove_words(text, words)

    @staticmethod
    def _extract_audio_segment(content: bytes,
                               start_time: float,
                               end_time: float) -> bytes:
        """
        Extracts an audio fragment from the complete audio based on the specified timestamps.

        :param content: Original audio content in bytes format.
        :param start_time: The starting time of the segment (in seconds).
        :param end_time: The ending time of the segment (in seconds).
        :return: The audio fragment in bytes format.
        """

        audio_stream = BytesIO(content)
        audio, sr = sf.read(audio_stream)

        start_sample = int(start_time * sr)
        end_sample = int(end_time * sr)

        segment = audio[start_sample:end_sample]

        segment_stream = BytesIO()
        sf.write(segment_stream, segment, samplerate=sr, format='WAV')
        return segment_stream.getvalue()

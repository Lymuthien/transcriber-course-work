from io import BytesIO
import soundfile as sf

from .voice_separator import VoiceSeparatorWithPyAnnote
from .natasha_stopwords_remover import NatashaStopwordsRemover
from .whisper_processor import WhisperProcessor


class Transcriber(object):
    def __init__(self,
                 token: str,
                 whisper_model: str = "medium",
                 speaker_diarization_model: str = "pyannote/speaker-diarization-3.1"):
        self._whisper_processor = WhisperProcessor(model_size=whisper_model)
        self._voice_processor = VoiceSeparatorWithPyAnnote(token, model_name=speaker_diarization_model)
        self._natasha_processor = NatashaStopwordsRemover()

    def transcribe(self,
                   content: bytes,
                   language: str | None = None) -> str:
        try:
            segments = self._voice_processor.separate_speakers(content)
        except Exception as e:
            raise RuntimeError(f"Error while separating by voices: {e}")

        return segments

        # transcription_results = []
        #
        # for segment in segments:
        #     start_time = segment["start"]
        #     end_time = segment["end"]
        #     speaker = segment["speaker"]
        #
        #     segment_audio = self._extract_audio_segment(content, start_time, end_time)
        #
        #     try:
        #         segment_text, detected_language = self._whisper_processor.transcribe_audio(
        #             content=segment_audio,
        #             language=language
        #         )
        #         transcription_results.append(f"[{speaker}] {segment_text.strip()}")
        #     except Exception as e:
        #         raise RuntimeError(f"Error while transcribe segment {speaker}: {e}")
        #
        # full_transcription = "\n\n".join(transcription_results)
        #
        # return full_transcription

    def remove_stopwords(self,
                         text: str,
                         remove_swear_words: bool = True,
                         go_few_times: bool = False) -> str:
        return self._natasha_processor.remove_stopwords(text)

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

from natasha import (
    Segmenter,
    MorphVocab,
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    Doc
)

# from .interfaces import IStopwordsRemover
from src.transcriber_service.services.interfaces import IStopwordsRemover


class NatashaStopwordsRemover(IStopwordsRemover):
    def __init__(self):
        self.__stopwords = {'типа', 'короче', 'ну', 'э', 'вообще', 'походу', 'вот', 'блин', }
        self.__swear_words = {'бля', 'блять', 'пиздец', 'ахуеть', }
        self._segmenter = Segmenter()
        self._morph_vocab = MorphVocab()
        self._emb = NewsEmbedding()
        self._morph_tagger = NewsMorphTagger(self._emb)
        self._syntax_parser = NewsSyntaxParser(self._emb)

    def remove_parasite_words(self, text: str, remove_swear_words: bool = True) -> str:
        paragraphs = text.split('\n')
        new_paragraphs = []

        for paragraph in paragraphs:
            doc = Doc(paragraph)
            doc.segment(self._segmenter)
            doc.tag_morph(self._morph_tagger)
            doc.parse_syntax(self._syntax_parser)

            new_text = []

            for token in doc.tokens:
                if not self._is_stopword(doc.tokens, token, remove_swear_words):
                    new_text.append(token)

            new_paragraphs.append(self._restore_text(new_text))

        return '\n'.join(new_paragraphs)

    def remove_words(self, text: str, removing_words: tuple | list) -> str:
        removing_words = set(map(lambda s: s.lower(), removing_words))
        paragraphs = text.split('\n')
        new_paragraphs = []

        for paragraph in paragraphs:
            doc = Doc(paragraph)
            doc.segment(self._segmenter)
            doc.parse_syntax(self._syntax_parser)

            new_text = []

            for token in doc.tokens:
                if token.text.lower() not in removing_words:
                    new_text.append(token)

            new_paragraphs.append(self._restore_text(new_text))

        return '\n'.join(new_paragraphs)

    def _is_stopword(self, all_tokens, target_token, remove_swear_words: bool) -> bool:
        lower_text = target_token.text.lower()
        if lower_text not in self.__stopwords and (lower_text not in self.__swear_words and remove_swear_words):
            return False

        dependents = [token for token in all_tokens if token.head_id == target_token.id]
        for token in dependents:
            if token.rel not in ['discourse', 'punct', 'ccomp']:
                return False
        return True

    @staticmethod
    def _restore_text(token_list: list) -> str:
        restored_text = ''

        for i, token in enumerate(token_list):
            if token.rel == 'punct':
                if i != 0 and token_list[i - 1].rel != 'punct':
                    restored_text += token.text
            else:
                restored_text += ' ' + token.text

        return restored_text

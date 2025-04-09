from natasha import (
    Segmenter,
    MorphVocab,
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    Doc
)

from ..interfaces import IStopwordsRemover


class NatashaStopwordsRemover(IStopwordsRemover):
    """
    Remover of stopwords with Natasha model.
    Supports only russian language.
    """

    def __init__(self):
        self.__stopwords = {'типа', 'короче', 'ну', 'э', 'вообще', 'вообще-то', 'похоже', 'походу', 'вот', 'блин',
                            'эм', 'так'}
        self.__swear_words = {'бля', 'блять', 'пиздец', 'ахуеть', }
        self._segmenter = Segmenter()
        self._morph_vocab = MorphVocab()
        self._emb = NewsEmbedding()
        self._morph_tagger = NewsMorphTagger(self._emb)
        self._syntax_parser = NewsSyntaxParser(self._emb)

    def remove_stopwords(self,
                         text: str,
                         remove_swear_words: bool = True,
                         go_few_times: bool = False) -> str:
        """
        Remove parasite words from text.

        Removing words:
        'типа', 'короче', 'ну', 'э', 'вообще', 'вообще-то', 'похоже', 'походу', 'вот', 'блин', 'эм', 'так'

        Swear words:
        'бля', 'блять', 'пиздец', 'ахуеть'

        Words removed from text by the context.
        If go_few_times and some stopwords weren't removed, try remove them one more time. If text haven't changed,
        it's a final result. This flag can delete important words. Be careful.
        Removing of swear words can work incorrect.

        :param text: Target text.
        :param remove_swear_words: True to remove swear words.
        :param go_few_times: True to remove stopwords one more time if text have changed.
        :return: Target text without swear words.
        """

        paragraphs = text.split('\n')
        new_paragraphs = []
        restart_flag = True

        while restart_flag:
            restart_flag = False

            for paragraph in paragraphs:
                doc = Doc(paragraph)
                doc.segment(self._segmenter)
                doc.tag_morph(self._morph_tagger)
                doc.parse_syntax(self._syntax_parser)

                new_text = []

                for token in doc.tokens:
                    if not self._is_stopword(doc.tokens, token, remove_swear_words):
                        new_text.append(token)
                    elif go_few_times:
                        restart_flag = True

                new_paragraphs.append(self._restore_text(new_text))

        return '\n'.join(new_paragraphs)[1:] if new_paragraphs else ''

    def remove_words(self,
                     text: str,
                     removing_words: tuple | list) -> str:
        """
        Remove given words from text.

        :param text: Target text.
        :param removing_words: List or tuple of words to remove.
        :return: Target text without words.
        """

        removing_words = set(map(lambda s: s.lower().strip(), removing_words))
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

        return '\n'.join(new_paragraphs)[1:] if new_paragraphs else ''

    def _is_stopword(self, all_tokens, target_token, remove_swear_words: bool) -> bool:
        """
        Check if given token is stopword.

        If token not in stopwords list return False.
        If token does not contain dependent tokens return True.
        If all token dependent tokens are 'discourse', 'punct', 'ccomp' return True.

        :param all_tokens: Token list of paragraph.
        :param target_token: Target token.
        :param remove_swear_words: True to remove swear words.
        :return: True if token is stopword else False.
        """

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
        """
        Restore text from token_list.

        Delete spaces before punctuators. Delete extra punctuators.

        :param token_list: Token list of paragraph.
        :return: The restored text.
        """
        restored_text = ''

        for i, token in enumerate(token_list):
            if token.rel == 'punct':
                if i != 0 and token_list[i - 1].rel != 'punct':
                    restored_text += token.text
            else:
                restored_text += ' ' + token.text

        return restored_text

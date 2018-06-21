from nltk.probability import FreqDist
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures

def unigram_word_feats(words, top_n=None, min_freq=0):
    """
    Return most common top_n word features.

    :param words: a list of words/tokens.
    :param top_n: number of best words/tokens to use, sorted by frequency.
    :rtype: list(str)
    :return: A list of `top_n` words/tokens (with no duplicates) sorted by
        frequency.
    """
    # Stopwords are not removed
    unigram_feats_freqs = FreqDist(word for word in words)
    return [w for w, f in unigram_feats_freqs.most_common(top_n)
            if unigram_feats_freqs[w] > min_freq]


def bigram_collocation_feats(documents, top_n=None, min_freq=3,
                             assoc_measure=BigramAssocMeasures.pmi):
    """
        Return `top_n` bigram features (using `assoc_measure`).
        Note that this method is based on bigram collocations measures, and not
        on simple bigram frequency.

        :param documents: a list (or iterable) of tokens.
        :param top_n: number of best words/tokens to use, sorted by association
            measure.
        :param assoc_measure: bigram association measure to use as score function.
        :param min_freq: the minimum number of occurrencies of bigrams to take
            into consideration.

        :return: `top_n` ngrams scored by the given association measure.
        """
    finder = BigramCollocationFinder.from_documents(documents)
    finder.apply_freq_filter(min_freq)
    return finder.nbest(assoc_measure, top_n)

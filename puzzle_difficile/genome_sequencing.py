# coding=utf-8

import sys
import unittest

cache = {}


def cache_first_arg(func):
    cache[func.__name__] = {}

    def wrapper(*args):
        if len(args[0]) == 1:
            return func(*args)

        key = ''.join(sorted(args[0]))
        if key not in cache:
            cache[func.__name__][key] = list(func(*args))
        return cache[func.__name__][key]
    return wrapper


def find_best_merge(words):
    words = remove_duplicated_words(words)
    best_merge = ''
    best_size = sum(map(len, words)) + 1
    for merged in merge_words(words):
        if len(merged) < best_size:
            best_merge = merged
            best_size = len(merged)
    return best_merge


def remove_duplicated_words(words):
    words = list(set(words))
    words_to_drop = []
    for i, word1 in enumerate(words):
        for word2 in words[:i] + words[i+1:]:
            if word1 in word2:
                words_to_drop.append(word1)
    return set(words) - set(words_to_drop)


@cache_first_arg
def merge_words(words: set):
    if len(words) == 1:
        yield from words
    else:
        for word in words:
            for merged in merge_words(words - {word}):
                yield merge_two_words(word, merged)
                yield merge_two_words(merged, word)


def merge_two_words(w1: str, w2: str) -> str:
    min_size = min(len(w1), len(w2))
    suffixes = {''} | {w1[-n - 1:] for n in range(min_size)}
    prefixes = {''} | {w2[:n + 1] for n in range(min_size)}
    nb_common_char = max(map(len, suffixes & prefixes))
    return w1 + w2[nb_common_char:]


class TestGenomeSequencing(unittest.TestCase):

    def test_sample_1(self):
        self.assertEqual('AACCTT', find_best_merge(['AAC', 'CCTT']))

    def test_sample_2(self):
        self.assertEqual('AGATTACAGA', find_best_merge(['AGATTA', 'GATTACA', 'TACAGA']))

    def test_sample_4(self):
        self.assertEqual('AGATTA', find_best_merge(['AGATTA', 'GAT']))

    def test_sample_7(self):
        self.assertEqual('CCCTGACATGA', find_best_merge(['CCCTG', 'TGACA', 'CATGA']))

    def test_customs(self):
        self.assertEqual('AGATTA', find_best_merge(['AGATTA', 'AGATTA']))
        self.assertEqual('', find_best_merge(set()))
        self.assertEqual('word', find_best_merge({'word'}))
        self.assertEqual('word', find_best_merge({'rd', 'wor'}))
        self.assertEqual('CCCTGACATGA', find_best_merge({'CCCTG', 'TGACA', 'CATGA'}))

    def test_merge_two_words(self):
        self.assertEqual('', merge_two_words('', ''))
        self.assertEqual('word', merge_two_words('wo', 'rd'))
        self.assertEqual('word', merge_two_words('wor', 'ord'))
        self.assertEqual('word', merge_two_words('word', 'word'))


class HeuristiqueGenomeSequencing:

    def __init__(self):
        super(HeuristiqueGenomeSequencing, self).__init__()
        self.prefixes = {}
        self.suffixes = {}

    def prefix(self, word):
        if word not in self.prefixes:
            self.prefixes[word] = {''} | {word[:i + 1] for i in range(len(word))}
        return self.prefixes[word]

    def suffix(self, word):
        if word not in self.suffixes:
            self.suffixes[word] = {''} | {word[-i - 1:] for i in range(len(word))}
        return self.suffixes[word]

    def merge_2_best_words(self, words, level=0) -> list:
        words = list(words)
        associations = []
        max_len = 0
        for i, word1 in enumerate(words):
            for word2 in words[i + 1:]:
                prefix1 = self.prefix(word1)
                suffix2 = self.suffix(word2)
                inter21 = prefix1 & suffix2
                len21 = max(map(len, inter21))

                prefix2 = self.prefix(word2)
                suffix1 = self.suffix(word1)
                inter12 = prefix2 & suffix1
                len12 = max(map(len, inter12))

                if len21 > len12:
                    if len21 == max_len:
                        associations.append([word2, word1, len21])
                    elif len21 > max_len:
                        associations = [[word2, word1, len21]]
                        max_len = len21
                else:
                    if len12 == max_len:
                        associations.append([word1, word2, len12])
                    elif len21 > max_len:
                        associations = [[word1, word2, len12]]
                        max_len = len12

            print('associations for', word1, ':', words, associations)
            yield from associations
            associations = []
            max_len = 0

    def merge_all_words(self, words):
        words = self.remove_duplicated_words(words)
        words_keep = []
        if len(words) == 1:
            words_keep = list(words)
        else:
            for w1, w2, n in self.merge_2_best_words(words):
                merged = w1 + w2[n:]
                print(words, 'merdging', w1, w2, merged)
                words = set(words) - {w1, w2} | {merged}
                words_keep = list(self.merge_all_words(words))

        max_len = max(map(len, words_keep))
        return [word for word in words_keep if len(word) == max_len]

    def merge_all_words_bak(self, words):
        words = self.remove_duplicated_words(words)
        while len(words) > 1:
            to_merge = self.merge_2_best_words(words)
            w1, w2, n = to_merge
            merged = w1 + w2[n:]
            # print('merdging', w1, w2, merged)
            words = set(words) - {w1, w2} | {merged}

        return list(words)[0]

    def remove_duplicated_words(self, words):
        words = list(set(words))
        words_to_drop = []
        for i, word1 in enumerate(words):
            for word2 in words[:i] + words[i+1:]:
                if word1 in word2:
                    words_to_drop.append(word1)
        return set(words) - set(words_to_drop)


def main():
    n = int(input())
    words = [input() for _ in range(n)]
    merged_word = find_best_merge(words)
    print(cache, file=sys.stderr)
    print(len(merged_word))


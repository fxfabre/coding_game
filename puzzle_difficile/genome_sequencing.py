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


def main():
    n = int(input())
    words = [input() for _ in range(n)]
    merged_word = find_best_merge(words)
    print(cache, file=sys.stderr)
    print(len(merged_word))

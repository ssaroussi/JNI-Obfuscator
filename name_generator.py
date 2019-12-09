#!/usr/bin/env python3

from os import environ
environ['SPACY_WARNING_IGNORE'] = 'W008'
from spacy import load
from typing import Set
from hashlib import md5

nlp = load('en_core_web_lg')

def most_similar(word: str, excluded_words: Set[str]):
    v_word = nlp.vocab[word]
    queries = [w for w in v_word.vocab if w.is_lower ==
               v_word.is_lower and w.prob >= -15]
    by_similarity = sorted(
        queries, key=lambda w: v_word.similarity(w), reverse=True)

    name: str = ''
    optimal_distance = 20
    optimal_distance = min(optimal_distance, len(by_similarity) - 1)
    s_index: int = optimal_distance
    direction: int = 1 # 1 | -1

    while(not name):
        if s_index == -1:
            return md5(word).hexdigest()

        current_name = ''.join(
            [i for i in by_similarity[s_index].lower_ if i.isalpha()])
        if current_name in excluded_words:
            s_index += direction

            if s_index >= len(by_similarity):
                s_index = optimal_distance - direction
                direction = -1

        else:
            name = current_name

    return name



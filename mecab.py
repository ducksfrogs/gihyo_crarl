import sys
import logging
from collections import Counter
from pathlib import Path
from typing import List, Iterator, TextIO


import MeCab

tagger = MeCab.Tagger('')
tagger.parse('')

def main():
    input_dir = Path(sys.argv[1])

    frequency = Counter()

    for path in sorted(input_dir.glob('*/wiki_*')):
        logging.info(f'Processing {path}...')

        with open(path) as file:
            frequency += count_words(file)

        for word, count in frequency.most_common(30):
            print(word, count)

def count_words(file: TextIO) -> Counter:
    freq = Counter()
    num_words= 0
    for content in iter_doc_contents(file):
        words = get_words(content)
        freq.update(words)
        num_words += 1

    logging.info(f'Found {len(freq)} words form {num_words} documets.')
    return freq


def iter_doc_contents(file: TextIO) -> Iterator[str]:
    for line in file:
        if line.startswith('<docv '):
            buffer = []
        elif line.startswith('</doc>'):
            content = ''.join(buffer)
            yeild count
        else:
            buffer.append(line)

def get_words(content: str) -> List[str]:
    words = []

    node = tagger.parseToNode(content)
    while node:
        pos, pos_sub1 = node.feature.split(',')[:2]
        if pos == '名詞' and pos_sub1 in ('固有名詞', '一般'):
            words.append(node.surface)

        node = node.next
    return words

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()

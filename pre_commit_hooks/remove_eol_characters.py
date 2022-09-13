#! /usr/bin/env python

import re
import sys
from typing import List, Tuple


def remove_eol() -> Tuple[str, str]:
    eol_character = r'\n'
    # \u4e00-\u9fff contains all chinese characters
    characters = r'\u4e00-\u9fff'
    # Unicode halfwidth and fullwidth forms, refer to
    # https://en.wikipedia.org/wiki/Halfwidth_and_Fullwidth_Forms_(Unicode_block)
    punctuations = r'\uff01-\uff9f'
    # Find natural Chinese paragraphs that are split by end_of_line characters.
    # The pattern is: Chinese characters/punctuations with one and only one
    # end_of_line in between.
    pattern = fr'([{characters}{punctuations}]){eol_character}([{characters}])'
    # This replacement will remove the end_of_line character in between
    repl = r'\1\2'
    return pattern, repl


def rewrite_file(filename: str, strategies: List[Tuple[str, str]]) -> bool:
    with open(filename, encoding='utf-8') as f:
        contents = f.read()
    changed = False
    for pattern, repl in strategies:
        if re.search(pattern, contents) is None:
            continue
        contents = re.sub(pattern, repl, contents)
        changed = True
    if changed:
        with open(filename, mode='w', encoding='utf-8') as f:
            f.write(contents)
    return changed


def main():
    strategies = [remove_eol()]
    changed = False
    for file in sys.argv[1:]:
        changed = changed | rewrite_file(file, strategies)
    return changed


if __name__ == '__main__':
    raise SystemExit(main())

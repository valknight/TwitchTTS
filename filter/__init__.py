import json
words = {}

with open('words.json', 'r') as f:
    words = json.loads(f.read())

print(words)


def parse_word(word: str) -> str:
    return words.get(word, word).lower()


def get_prefixes():
    with open('prefix.json', 'r') as f:
        return json.loads(f.read())


def parse_sentence(sentence: str) -> str:
    for phrase in get_prefixes():
        if sentence.startswith(phrase):
            return ""
    words_in_s = sentence.split()
    new_words = []
    for word in words_in_s:
        new_words.append(parse_word(word))
    return ' '.join(new_words)

import logging
import csv

import transaction
from db import models
from transformers import T5ForConditionalGeneration, T5Tokenizer

from views.constants.words import TranslationLanguage

prefix = 'translate to ru: '

word_examples = {}

logger = logging.getLogger('abc')


def add_word_data_to_dict(file_name):
    print("add_word_data_to_dict - start")
    with open(file_name, 'r') as file:
        csvreader = csv.reader(file, delimiter=';')
        header = next(csvreader)
        for row in csvreader:
            word = row[0].lower()
            word_examples.setdefault(word, {
                'meaning': row[1],
                'examples': [],
                'pos': '',
                'level': '',
            })
            word_examples[word]['pos'] = row[1]
            word_examples[word]['level'] = row[2]

    print("add_word_data_to_dict - done")


def add_word_examples():
    print("add_word_examples - start")
    with open("./engvocab_word_examples.csv", 'r') as file:
        csvreader = csv.reader(file, delimiter=';')
        header = next(csvreader)
        for row in csvreader:
            word = row[0].lower()

            word_examples.setdefault(word, {
                'meaning': row[1],
                'examples': [],
                'pos': '',
                'level': '',
            })
            for idx in range(2, 11):
                example = row[idx]
                if example:
                    word_examples[word]['examples'].append(row[idx])

    print("add_word_examples - done")


model_name = 'utrobinmv/t5_translate_en_ru_zh_base_200'
model = T5ForConditionalGeneration.from_pretrained(model_name)
tokenizer = T5Tokenizer.from_pretrained(model_name)

add_word_data_to_dict("./engvocab_words.csv")
add_word_examples()


i = 0
for word, data in word_examples.items():
    i += 1

    print(f"({i}/{len(word_examples)}) {word} - exm len: ({len(data['examples'])})")

    src_text = prefix + word
    input_ids = tokenizer(src_text, return_tensors="pt")
    generated_tokens = model.generate(**input_ids)
    tr = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)

    ru = tr[0] if tr else ''

    w = models.Word(
        word=word,
        level=data['level'],
        meaning=data['meaning']
    )
    w.add()
    w.flush()

    word_translation = models.WordTranslation(
        word_id=w.id,
        language=TranslationLanguage.RU,
        translation=ru
    )
    word_translation.add()

    for example in data['examples']:
        example = models.WordExamples(
            word_id=w.id,
            example_sentece=example,
        )
        example.add()

transaction.commit()

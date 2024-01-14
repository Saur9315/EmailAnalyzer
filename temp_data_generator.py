import random
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
import pandas as pd
from decouple import config
# import pymorphy2

# morph = pymorphy2.MorphAnalyzer()
#
# def get_synonyms(word):
#     parsed_word = morph.parse(word)[0]
#     print(parsed_word)
#     print(parsed_word.lexeme)
#     # return [parse.lexeme for parse in parsed_word.lexeme]
#
# # Example usage
# word = "продукте"  # Replace with your Russian word
# synonyms = get_synonyms(word)
# print(f"Synonyms for '{word}': {synonyms}")
pd.set_option('display.max_colwidth', 100)

def generate_data(labels=None, num_sentences_per_label=10):
    if labels is None:
        labels = ['inquiry', 'feedback', 'complaint', 'request']

    def get_synonyms(word):
        synonyms = set()
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonyms.add(lemma.name())
        return list(synonyms)

    def replace_with_synonyms(sentence):
        tokens = word_tokenize(sentence)
        replaced_tokens = [
            token if random.random() > 0.5 or not get_synonyms(token) else random.choice(get_synonyms(token))
            for token in tokens
        ]
        return ' '.join(replaced_tokens)

    def generate_sentences(label, n):
        sentences = []
        for _ in range(n):
            if label == 'inquiry':
                template = "Could you please provide more information about {}?"
                content_options = [["your product"], ["your service"]]
                # template = "Не могли бы вы предоставить дополнительную информацию о вашем {}?"
                # content_options = ["продукте", "сервисе"]
                content = random.choice(content_options)
            elif label == 'feedback':
                template = "I wanted to let you know that {} is {}."
                content_options = "your product; excellent", "your service; excellent"
                # template = "Я хотел сообщить вам, что {} {}."
                # content = "ваш продукт/сервис превосходен"
                content = random.choice(content_options).split(";")
            elif label == 'complaint':
                template = "I am not satisfied with {}."
                content_options = [["your product"], ["your service"]]
                # template = "я не удовлетворен вашим {}."
                # content_options = ["продуктом", "сервисом"]
                content = random.choice(content_options)
            elif label == 'request':
                template = "I would like to request {} for {}."
                content_options = ["more information; your product", "more information; your service"]
                # template = "Я хотел бы попросить {} for {}."
                # content_options = ["больше информации; о вашем продукте", "больше информации; о вашем сервисе"]
                content = random.choice(content_options).split(';')
            else:
                return "Invalid label"

            filled_template = template.format(*content)  # Fill in the template with relevant content
            varied_sentence = replace_with_synonyms(filled_template)  # Replace some words with synonyms
            sentences.append(varied_sentence)
            # print(sentences)
        return sentences

    data = []
    for label in labels:
        generated_sentences = generate_sentences(label, num_sentences_per_label)
        for sentence in generated_sentences:
            data.append({'label': label.capitalize(), 'text': sentence})
    df = pd.DataFrame(data)
    return df


data_generator = config('DATA_GENERATOR', default=False, cast=bool)
print(data_generator, type(data_generator))
if data_generator:
    print('generating data...')
    n = config('NUM_SENTENCES_PER_LABEL', default=10, cast=int)
    print(generate_data(num_sentences_per_label=n))
    # for indx, row in data.iterrows():
    #     print(row['text'])
    #     break

import nltk
import pandas as pd

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import SnowballStemmer, WordNetLemmatizer
import string

# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')

pd.set_option('display.max_columns', None)

stemmer = SnowballStemmer(language='english')
lemmatizer = WordNetLemmatizer()

# grammar = "NP: {<DT>?<JJ>*<NN>}"
grammar = "NP: {<JJ>*}"
chunk_parser = nltk.RegexpParser(grammar)


def nlp_processing(df):
    stop_words = set(stopwords.words("english"))
    cleaned_text = []
    for sentence in sent_tokenize(df):
        cleaned_text.append([lemmatizer.lemmatize(word) for word in word_tokenize(sentence)
                             if word.casefold() not in stop_words and word.casefold() not in string.punctuation])
    # print(cleaned_text)
    return cleaned_text

    # # Now use the trained model to predict labels for new data
    # new_text = "Hello, I have a question about your products."
    # cleaned_new_text = nlp_processing(new_text)
    # new_text_features = vectorizer.transform([' '.join(sentence) for sentence in cleaned_new_text])
    # predicted_label = classifier.predict(new_text_features)
    # print(f"Predicted Label: {predicted_label}")


if __name__ == '__main__':
    email_text = """
    Hello Company Team,
    I hope this email finds you well. My name is Sender, and I am reaching out to inquire about your server products. 
    We are planning to upgrade our server infrastructure, and I'm interested in learning more about the specifications, 
    pricing, and any ongoing promotions or discounts.
    Could you please provide detailed information about the server models you offer, including their features and pricing? 
    Additionally, if there are any upcoming events or webinars related to your server solutions, 
    I would appreciate the details.

    Thank you for your time, and I look forward to hearing from you soon.

    Best regards,
    Sender.
    """
    # print(email_text.split())
    print(nlp_processing(email_text))

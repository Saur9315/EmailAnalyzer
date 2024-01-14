import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd
import random
import temp_data_generator
import os
from decouple import config

from nlp_message_processing import nlp_processing

pd.set_option('display.max_columns', None)

# Generate random sentences
# def generate_sentences(label, count):
#     sentences = []
#     for _ in range(count):
#         sentence = random.choice([
#             "I'm inquiring about your {} products and pricing.",
#             "I wanted to provide feedback on your {} service.",
#             "I have a complaint regarding the quality of your {}.",
#             "I'm requesting information about your {} solutions.",
#             "Can you provide details about your {} models?",
#             "I wanted to share some feedback about your {}.",
#             "I need to file a complaint about a recent {}.",
#             "I'm making a request for a demo of your {}.",
#             "Interested in your {} offerings. Please provide details.",
#             "Just wanted to share my thoughts on your {}.",
#             "Experiencing issues with a recent {}. Need assistance.",
#             "Requesting a trial version of your {}.",
#             "Considering your {} solutions. Need more information.",
#             "Providing feedback on the user experience of your {}.",
#             "Unhappy with a recent {}. This is a formal complaint.",
#             "Seeking a demo of your latest {} release."
#         ]).format(label)
#         sentences.append(sentence)
#     return sentences
#
# # Create a dataset with approximately 25 samples for each label
# labels = ['inquiry', 'feedback', 'complaint', 'request']
# data = {'label': [], 'text': []}
#
# for label in labels:
#     data['label'].extend([label] * 50)
#     data['text'].extend(generate_sentences(label, 50))
#
# # Shuffle the dataset
# combined = list(zip(data['label'], data['text']))
# random.shuffle(combined)
# data['label'], data['text'] = zip(*combined)
# # # download the dataset
# # data = {
# #     'label': ['inquiry', 'feedback', 'complaint', 'request', 'inquiry', 'feedback', 'complaint', 'request',
# #               'inquiry', 'feedback', 'complaint', 'request', 'inquiry', 'feedback', 'complaint', 'request'],
# #     'text': [
# #         "I'm inquiring about your server products and pricing.",
# #         "I wanted to provide feedback on your recent service.",
# #         "I have a complaint regarding the quality of your product.",
# #         "I'm requesting information about your software solutions.",
# #         "Can you provide details about your server models?",
# #         "I wanted to share some feedback about your website.",
# #         "I need to file a complaint about a recent purchase.",
# #         "I'm making a request for a demo of your software.",
# #         "Interested in your server offerings. Please provide details.",
# #         "Just wanted to share my thoughts on your customer service.",
# #         "Experiencing issues with a recent purchase. Need assistance.",
# #         "Requesting a trial version of your software.",
# #         "Considering your server solutions. Need more information.",
# #         "Providing feedback on the user experience of your website.",
# #         "Unhappy with a recent purchase. This is a formal complaint.",
# #         "Seeking a demo of your latest software release."
# #     ]
# # }
#
# df = pd.DataFrame(data)
# # print(df)


model_path = config('MODEL_PATH')
vectorizer_path = config('VECTORIZER_PATH')


def svm_model(df, model_save_path, vectorizer_save_path):
    # train, test data
    train_data, test_data = train_test_split(df, test_size=0.2, random_state=42)

    # extract features using TfidfVectorizer
    vectorizer = TfidfVectorizer()
    X_train = vectorizer.fit_transform(train_data['text'])
    X_test = vectorizer.transform(test_data['text'])

    # train, test labels
    y_train = train_data['label']
    y_test = test_data['label']

    # train a Support Vector Machine classifier
    classifier = SVC()
    classifier.fit(X_train, y_train)

    # save the trained model and vectorizer
    joblib.dump(classifier, model_save_path)
    joblib.dump(vectorizer, vectorizer_save_path)

    # predictions on test data
    predictions = classifier.predict(X_test)

    # evaluate the model
    accuracy = accuracy_score(y_test, predictions)
    print(f"Accuracy: {accuracy}")

    # classification report
    print("Classification Report:\n", classification_report(y_test, predictions, zero_division=1))


def load_and_predict(new_text, model_path=model_path, vectorizer_path=vectorizer_path):
    # Load the trained model and vectorizer
    classifier = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)

    # transform the new text
    new_text_vectorized = vectorizer.transform([new_text])

    # predictions
    predicted_label = classifier.predict(new_text_vectorized)
    print(f"Predicted Label: {predicted_label[0]}")
    return predicted_label


# train and save the model
train_model = config('TRAIN_THE_MODEL', default=False, cast=bool)
if not os.path.exists(model_path) or not os.path.exists(vectorizer_path) or train_model:
    # if config('DATA_GENERATOR'):
    n = config('NUM_SENTENCES_PER_LABEL', default=10, cast=int)
    df = temp_data_generator.generate_data(num_sentences_per_label=n)
    # print(df)
    svm_model(df, model_save_path=model_path, vectorizer_save_path=vectorizer_path)

# Load the model and make predictions on new input
# new_text = "Hello, I have a question about your products."
# new_text2 = "Dear Company support, I have an issue with your products. " \
#             "Could you call me back to discuss about the problem please?"
# load_and_predict(new_text, model_path=model_path, vectorizer_path=vectorizer_path)
# load_and_predict(new_text2, model_path=model_path, vectorizer_path=vectorizer_path)

# has been moved to nlp_message_processing.py
# # Now, you can use the trained model to predict labels for new data
# new_text = "Hello, I have a question about your products."
# cleaned_new_text = nlp_processing(new_text)
# new_text_vectorized = vectorizer.transform([' '.join(sentence) for sentence in cleaned_new_text])
# predicted_label = classifier.predict(new_text_vectorized)
# print(f"Predicted Label: {predicted_label}")

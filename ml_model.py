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


pd.set_option('display.max_columns', None)


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

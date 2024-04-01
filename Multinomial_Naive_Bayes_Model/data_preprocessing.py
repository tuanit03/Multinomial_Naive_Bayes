import os
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import spacy

nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)
nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])


def remove_special_characters(text):
    text = re.sub(r'\b(\d+\w+|\w+\d+)\b', '', text)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\.', '', text)
    text = re.sub(r'\W+', ' ', text)
    text = re.sub(r'\b\w{1,3}\b', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def to_lower_case(text):
    text = text.lower()
    return text


def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text)
    tokens = [token for token in tokens if token not in stop_words]
    return ' '.join(tokens)


def lemmatize_words(text):
    doc = nlp(text)
    lemmatized_text = ' '.join([token.lemma_ for token in doc])
    return lemmatized_text


def preprocess_text(text):
    text = remove_special_characters(text)
    text = to_lower_case(text)
    text = remove_stopwords(text)
    text = lemmatize_words(text)
    return text


def preprocess_files_in_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt"):
                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        text = f.read()
                        text = preprocess_text(text)
                        with open(os.path.join(root, file), 'w', encoding='utf-8') as f:
                            f.write(text)
                    print(f"File {file} in {root} has been successfully preprocessed.")
                except Exception as e:
                    print(f"Error preprocessing file {file} in {root}: {e}")


preprocess_files_in_directory("article_search\\train_data")

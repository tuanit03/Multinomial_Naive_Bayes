from sklearn.preprocessing import LabelEncoder
import os
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from joblib import dump


def read_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt"):
                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        yield f.read(), root.split('\\')[-1]
                except Exception as e:
                    print(f"Error reading file {file}: {e}")


def load_data_and_labels(directory):
    texts = []
    labels = []
    for text, label in read_files(directory):
        texts.append(text)
        labels.append(label)
    return texts, labels


def tfidf_vectorize(texts):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)
    return X, vectorizer


def main():
    directory = "article_search\\train_data"
    texts, labels = load_data_and_labels(directory)

    X, vectorizer = tfidf_vectorize(texts)
    dump(vectorizer, 'vectorizer.joblib')

    encoder = LabelEncoder()
    y = encoder.fit_transform(labels)

    # Save the mapping of label names to encoded values
    label_mapping = {i: label.split('\\')[-1] for i, label in enumerate(encoder.classes_)}
    dump(label_mapping, 'label_mapping.joblib')

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    clf = MultinomialNB()
    parameters = {'alpha': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]}
    grid_search = GridSearchCV(estimator=clf, param_grid=parameters, scoring='accuracy', cv=5)
    grid_search.fit(X_train, y_train)
    print("Best Score: ", grid_search.best_score_)
    print("Best Params: ", grid_search.best_params_)

    dump(grid_search, 'model.joblib')


if __name__ == "__main__":
    main()

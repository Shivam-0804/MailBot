import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from nlp.basic_nlp import extract_dates_times, extract_task

df = pd.read_csv("data/tasks.csv")

X_train, X_test, y_train, y_test = train_test_split(df["task"], df["label"], test_size=0.2, random_state=42)

vectorizer = TfidfVectorizer()

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

clf = MultinomialNB()
clf.fit(X_train_tfidf, y_train)

accuracy = clf.score(X_test_tfidf, y_test)
print("Accuracy:", accuracy)

def predict_task_label(text):
    text_tfidf = vectorizer.transform([text])
    prediction = clf.predict(text_tfidf)
    return prediction[0] if prediction[0] in df['label'].values else None

def main():
    while True:
        user_input = input("Enter a task description (or type 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break
        
        label = predict_task_label(user_input)
        if label is None:
            label = "null"
        print(f"Predicted label for the task: {label}")
        
        dates, times = extract_dates_times(user_input)
        print(f"Dates found: {dates}")
        print(f"Times found: {times}")
        
        task = extract_task(user_input)
        print(f"Extracted task: {task}")

if __name__ == "__main__":
    main()

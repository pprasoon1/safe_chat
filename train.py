import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
from preprocess import clean_text

print("Loading dataset...")
df = pd.read_csv("data/train.csv")

labels = ["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]

print("Cleaning text...")
df["clean_text"] = df["comment_text"].astype(str).apply(clean_text)

X = df["clean_text"]
y = df[labels]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Vectorizing...")
vectorizer = TfidfVectorizer(
    max_features=30000,
    ngram_range=(1,2),
    min_df=5
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

models = {}

print("Training models...")
for label in labels:
    print(f"Training for label: {label}")
    clf = LogisticRegression(max_iter=1000, n_jobs=-1)
    clf.fit(X_train_vec, y_train[label])
    models[label] = clf

print("Saving models...")
joblib.dump(vectorizer, "vectorizer.pkl")
joblib.dump(models, "toxicity_models.pkl")

print("Training complete!")
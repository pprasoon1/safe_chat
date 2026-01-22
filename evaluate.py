import pandas as pd
from sklearn.metrics import classification_report, roc_auc_score
import joblib
from preprocess import clean_text

df = pd.read_csv("data/train.csv")
labels = ["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]

df["clean_text"] = df["comment_text"].astype(str).apply(clean_text)

X = df["clean_text"]
y = df[labels]

vectorizer = joblib.load("vectorizer.pkl")
models = joblib.load("toxicity_models.pkl")

X_vec = vectorizer.transform(X)

print("\nEvaluation Results:\n")

for label in labels:
    preds = models[label].predict(X_vec)
    probs = models[label].predict_proba(X_vec)[:, 1]

    print(f"\nLabel: {label}")
    print(classification_report(y[label], preds))
    print("ROC_AUC:", roc_auc_score(y[label], probs))

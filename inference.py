import joblib
from preprocess import clean_text

vectorizer = joblib.load("vectorizer.pkl")
models = joblib.load("toxicity_models.pkl")

LABELS = ["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]

def predict(text: str):
    clean = clean_text(text)
    vec = vectorizer.transform([clean])

    scores = {}
    for label in LABELS:
        prob = models[label].predict_proba(vec)[0][1]
        scores[label] = float(prob)

    toxicity = max(scores.values())

    return {
        "scores": scores,
        "toxicity": toxicity
    }
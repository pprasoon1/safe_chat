from fastapi import FastAPI
from pydantic import BaseModel
import joblib
from preprocess import clean_text

app = FastAPI(title="Toxicity Classification API")

LABELS = ["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]

# Load models once
vectorizer = joblib.load("vectorizer.pkl")
models = joblib.load("toxicity_models.pkl")

# Request schema
class TextRequest(BaseModel):
    text: str

# Health check
@app.get("/")
async def root():
    return {"status": "ok", "message": "Toxicity API running"}

# Prediction endpoint
@app.post("/predict")
async def classify(req: TextRequest):
    clean = clean_text(req.text)
    vec = vectorizer.transform([clean])

    scores = {}
    for label in LABELS:
        prob = models[label].predict_proba(vec)[0][1]
        scores[label] = float(prob)

    toxicity = max(scores.values())

    return {
        "toxicity": toxicity,
        "scores": scores
    }
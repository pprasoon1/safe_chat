# pip install torch transformers
# using unitary/unbiased-toxic-roberta


import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

LABELS = ["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]

# Load pretrained toxic moderation model
MODEL_NAME = "unitary/unbiased-toxic-roberta"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

model.eval()  # inference mode


def predict(text: str):
    # Tokenize input
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=512
    )

    # Run model
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits  # shape: (1, 6)

    # Apply sigmoid (multi-label classification)
    probs = torch.sigmoid(logits)[0].tolist()

    # Build label → probability dict
    scores = {label: float(p) for label, p in zip(LABELS, probs)}

    # Overall toxicity = max probability
    toxicity = max(scores.values())

    return {
        "scores": scores,
        "toxicity": toxicity
    }


# Quick test
if __name__ == "__main__":
    text = "you are a disgusting idiot and should die"
    result = predict(text)
    print(result)

import re
import nltk
from nltk.corpus import stopwords

nltk.download("stopwords")
STOPWORDS = set(stopwords.words("english"))

def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+", "", text)     #remove links
    text = re.sub(r"@\w+", "", text)        #remove mentuions
    text = re.sub(r"[^a-z\s]", "", text)    #keep only letters
    text = " ".join([w for w in text.split() if w not in STOPWORDS])
    return text

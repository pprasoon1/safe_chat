Step 1 - ml model creation
preprocessing --> using re library for pattern matching and removing links, mentions etc
--> using nltk for nlp tasks (here using only stopwords) to remove noise

EDA and PCA on dataset- rejected pca because of low performance


then trained ml model using tf-idf and logisctic regression-> created vectorized library(vectorizer.pkl) and toxicity model for each label -->train.py

then evaluated the model -> evaluated.py




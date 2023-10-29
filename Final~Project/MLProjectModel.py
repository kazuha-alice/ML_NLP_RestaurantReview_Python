# importing the libraries

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# import the data-set
df = pd.read_csv('Restaurant_Reviews.tsv', delimiter='\t', quoting=3)
# bag of worlds model
import re
import nltk
nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
corpus = []
for i in range(0, 1000):
    review = df['Review'][i]  # accessing the ith review
    # remove all the punctuations
    re.sub('^a-zA-Z', ' ', review)
    # now convert this to lowercase
    review.lower()
    # create a list of words for review
    review = review.split()
    # convert all the words to their basal form, using WordNetLementizer object
    wl = WordNetLemmatizer()
    # get all the words and remove all the stopwords from the data
    all_stopwords = set(stopwords.words('english')) - {'not', 'but', 'is', 'the', 'nasty', 'great', 'bad', 'good', 'wasted'}
    # collect all the stopwords from english language to compare them
    # create a list of important words now
    review = [wl.lemmatize(word) for word in review if word not in set(all_stopwords)]
    # now again convert this list to a String of required words and append it to corpus
    review = ' '.join(review)
    corpus.append(review)
# now we need to create a bag Tf-IDF model to convert this to numeric vectors
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=1500)
# finally seperate x and the ys
x = cv.fit_transform(corpus).toarray()
print(x)
y = df.iloc[:, -1].values
# split the data into train and test set

from sklearn.model_selection import train_test_split
x_tr, x_te, y_tr, y_te = train_test_split(x, y, test_size=0.1, random_state=25)
# ---------------------------------------------K-NearestNeighbors Algorithm---------------------------------------------
from sklearn.neighbors import KNeighborsClassifier
classifier = KNeighborsClassifier(n_neighbors=1, weights='distance', algorithm='brute')
# fit the model
classifier.fit(x_tr, y_tr.ravel())
y_pred = classifier.predict(x_te)
print(y_pred)
# accuracy score and confusion matrix
from sklearn.metrics import accuracy_score, confusion_matrix, plot_confusion_matrix
print(accuracy_score(y_te, y_pred))
print(confusion_matrix(y_te, y_pred))
plot_confusion_matrix(estimator=classifier, X=x_te, y_true=y_te)
plt.show()
text = "bad place"
ip = [wl.lemmatize(word) for word in text if word not in set(corpus)]
ip = cv.transform([text])
result = classifier.predict(ip)
print(result)

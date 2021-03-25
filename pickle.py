import pandas as pd
import numpy as np
import re

df = pd.read_csv('balanced_reviews.csv')

df.dropna (inplace = True)

df = df[df['overall'] != 3]

df['overall'].value_counts()

df['Positivity'] = np.where (df['overall'] > 3, 1, 0)

df.to_csv('balanced_reviews.csv',index= False)

#cleaning the reviews
def clean_reviews(review):
    return " ".join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])", " ",review.lower()).split())

df['reviewText']=df['reviewText'].apply(clean_reviews)


#reviewText - features
#Positivity - labels

from sklearn.model_selection import train_test_split


features_train, features_test, labels_train, labels_test  = train_test_split(df['reviewText'], df['Positivity'], random_state = 42)

from sklearn.feature_extraction.text import TfidfVectorizer


vect = TfidfVectorizer(min_df = 5).fit(features_train)


features_train_vectorized = vect.transform(features_train)


from sklearn.linear_model import LogisticRegression


model = LogisticRegression()

model.fit(features_train_vectorized, labels_train)

predictions = model.predict(vect.transform(features_test))


#making the pickel file
import pickle

pkl_filename = "pickle_model.pkl"

file = open(pkl_filename, 'wb')

pickle.dump(model, file)

pickle.dump(vect.vocabulary_, open('features.pkl','wb'))
 
file.close()

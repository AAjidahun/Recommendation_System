#!/usr/bin/env python
# coding: utf-8

# In[69]:


#importing important library
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import ast

#viewing full data
dt1=pd.read_csv('C:\\Users\\ajida\\Desktop\\Machine\\tmdb_5000_movies.csv')
dt2=pd.read_csv('C:\\Users\\ajida\\Desktop\\Machine\\tmdb_5000_credits.csv')

#joining the 2 data
dt=dt1.merge(dt2,on='title',how='inner')
dt

#retaining only useful columns
data=dt[['id','title','keywords','overview','genres','cast','crew']]
data

#removing keys and retaing values 
import ast
def convert(col):
    converted=[]
    for i in ast.literal_eval(col):
        value=str(i['name'])
        converted.append(value)
    
    return converted


data['genres']=data['genres'].apply(convert)

data['keywords']=data['keywords'].apply(convert)
data['cast'] = data['cast'].apply(convert)
data['crew'] = data['crew'].apply(convert)


#makin the overview column into a list
data['overview']=data['overview'].apply(lambda x:str(x).split())
data

#remove white spaces
data['keywords']=data['keywords'].apply(lambda x: [i.replace(" ","") for i in x ] )
data['genres']=data['genres'].apply(lambda x: [i.replace(" ","") for i in x ] )
data['cast']=data['cast'].apply(lambda x: [i.replace(" ","") for i in x ] )
data['crew']=data['crew'].apply(lambda x: [i.replace(" ","") for i in x ] )

#creating the tag column
data['tag']=data['overview']+data['genres']+data['keywords']+data['cast']+data['crew']


# In[70]:


#coverting the tag to string

data['tag']=data['tag'].apply(lambda x:" ".join(x).lower())

data['tag']


# In[71]:


#converting tag text to base4
import nltk
from nltk.stem import PorterStemmer
ps=PorterStemmer()
def stem(sentence):
    y=[]
    for i in sentence.split(' '):
        y.append(ps.stem(i))
    rejoin= " ".join(y)
    return rejoin
        
data['tag']=data['tag'].apply(stem)
data       


# In[73]:


# vectorizize tag column
from sklearn.feature_extraction.text import CountVectorizer
cv=CountVectorizer(max_features=5000, stop_words='english')
countvector=cv.fit_transform(data['tag']).toarray()
countvector


# In[74]:


# Generating similarity measure
from sklearn.metrics.pairwise import cosine_similarity as cos_s
import pickle
similarity=cos_s(countvector)
similarity
with open('similarity.pkl','wb') as similar:
    pickle.dump(similarity,similar)
with open('movies.pkl','wb') as movie:
    pickle.dump(data,movie)


# In[77]:


similarity.shape
countvector.shape


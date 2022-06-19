import warnings
import argparse
import nltk
import re
import json
import ast
import os
#import pickle
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB, BernoulliNB, GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.neighbors import DistanceMetric
import pandas as pd

def get():
    with open('./backend/yummy.json',encoding = 'utf-8') as json_data:

        list_rec = json.load(json_data)
        #print("-->First Recipe:",list_rec[0])
    return list_rec

def eda(list_rec):
    rec_ings = []
    u_ingd = []
    X,y = [],[]
    ids = []
    #looking at number ingredients etc.
    for i in list_rec:
        ids.append(i['id'])
        rec_ings.append(i['ingredients'])
        u_ingd.extend(i['ingredients'])
        y.append(i['cuisine'])
    tot_ings = len(u_ingd)
    u_ingd = list(set(u_ingd))
    
    return y, ids, rec_ings

def train_mod(list_rec):
    y, ids, rec_ings = eda(list_rec)
    
    #Combining all ingredients in weach reciepe for input to tf-idf
    temp_ings = []
    for ind, ings in enumerate(rec_ings):
        all_ing ='þ' + 'þþ'.join(ings) + 'þ'
        temp_ings.append(all_ing)

    #Tf-idf for better features.
    with warnings.catch_warnings(): 
        warnings.filterwarnings(action = "ignore",category = FutureWarning)
        #vectorize = TfidfVectorizer(token_pattern=r'þ(.*?)þ',min_df =0.0001)
        vectorize = CountVectorizer(token_pattern = r'þ(.*?)þ',min_df = 0.0001)
        model = vectorize.fit_transform(temp_ings)

    X = model.toarray()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05,random_state = 1312)

    clf = MultinomialNB().fit(X_train,y_train)
    #clf = BernoulliNB().fit(X_train,y_train)
    #clf = MLPClassifier(hidden_layer_sizes = (200,100,50),verbose = True,max_iter = 50).fit(X_train,y_train)
    print("Train Accuracy:",clf.score(X_train,y_train),"Test Accuracy:",clf.score(X_test,y_test))
    return clf, vectorize, ids, X


def predict_cus(list_rec,ingredients):
    filename = "data/MLP.sav"
    clf , vectorize, ids, X = train_mod(list_rec)

    if ingredients:
        input_ing = ingredients
        input_ing  = ['þ' + 'þþ'.join(input_ing) + 'þ']
        #input_ing.append('þsea saltþ')
        with warnings.catch_warnings():
            warnings.filterwarnings(action = "ignore",category = FutureWarning)
            input_arg_mod = vectorize.transform(input_ing)
        X_in = input_arg_mod.toarray()

        prediction = clf.predict(X_in)[0].upper()
        #Calculating the top-5 recipies:
        dist = DistanceMetric.get_metric('jaccard')
        dist_l  = dist.pairwise(X,X_in)
        dist_l = [item for sublist in dist_l for item in sublist]
  
        idx = np.argpartition(dist_l,10)
        index = idx[:10]
        ids_5 = [ids[i] for i in index]
        dist_5 = [dist_l[i] for i in index]
 
        return prediction, ids_5, dist_5

def main(ingredients):
    list_rec = get()
    cuis_dict={}
    recep_lst = []
    
    data_1=pd.read_csv('./backend/data.csv')
    
    prediction,ids_5,dist_5 = predict_cus(list_rec,ingredients)        
    for i in ids_5:
      recepies=data_1.iloc[i-1]['recepies']
      cuisine=data_1.iloc[i-1]['cuisine']
      receipe_df = data_1[data_1["recepies"] == recepies]
      ingred = ast.literal_eval(list(receipe_df["ingredients"])[0])
    # ing input ingr obtained
      cnt = 0
      for ing in list(set(ingredients)):
        for ingr in list(set(ingred)):
            if ing in ingr:
                cnt+=1
      if cnt == len(list(set(ingredients))):
        if cuisine in cuis_dict.keys():
            cuis_dict[cuisine].append(recepies)
        else:
            cuis_dict[cuisine] = [recepies]
        
    #   elif cnt > 0:
    #     if cuisine in cuis_dict.keys():
    #         cuis_dict[cuisine].append(recepies)
    #     else:
    #         cuis_dict[cuisine] = [recepies]
    # if len(cuis_dict.keys()) == 0:
    #   for i in ids_5:
    #     recepies=data_1.iloc[i-1]['recepies']
    #     cuisine=data_1.iloc[i-1]['cuisine']
    #     receipe_df = data_1[data_1["recepies"] == recepies]
    #     ingred = ast.literal_eval(list(receipe_df["ingredients"])[0])
    #     # ing input ingr obtained
    #     cnt = 0
    #     for ing in list(set(ingredients)):
    #         for ingr in list(set(ingred)):
    #             if ing in ingr:
    #                 cnt+=1
    #     if cnt > 0:
    #         if cuisine in cuis_dict.keys():
    #             cuis_dict[cuisine].append(recepies)
    #         else:
    #             cuis_dict[cuisine] = [recepies]
    return cuis_dict


if __name__=='__main__':
    pass
    # print(main(['wheat','oil']))

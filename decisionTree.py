import pandas as pd
from BiasedWordsNgram import extract_biased_words
from BoW_PCA import toknize_article
from BoW_PCA import vectorize_articles
from gensim import corpora, matutils
import random
import math
import json
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.metrics import accuracy_score
from subprocess import call
from sklearn.metrics import confusion_matrix
import re
import operator
from nltk.corpus import stopwords

# import graphviz
with open('data.json') as data_file:    
  data = json.load(data_file)
  """
  Adjustable variables
  """
 
  #dividing data into three categories
  lib = data['liberal']
  con = data['conservative']

def create_dataframe(ind):
  #create word corpse
  # biased_words = extract_biased_words(1)
  if ind == 0:
    words_corpse = list(set(extract_biased_words(2)))
  elif ind == 1:
    words_corpse = list(set(add_prefix_features(list(set(extract_biased_words(1))))))
  elif ind == -1:
    # tokenize the docs
    lib_tokenized_docs = []
    con_tokenized_docs = []
    
    for sentence in lib[0:1000]:
      tokens = toknize_article(sentence)
      lib_tokenized_docs.append(tokens)
    
    for sentence in con[0:1000]:
      tokens = toknize_article(sentence)
      con_tokenized_docs.append(tokens)
    
    # concat tokenized_docs lists
    all_tokenized_docs = lib_tokenized_docs + con_tokenized_docs
    
    # use all_tokenized_docs so that matrix's # of features matches
    words_corpse =  corpora.Dictionary(all_tokenized_docs).values()
    # print dict.values()
    # create matrix for each category
  
  columns = ['ideology'] + words_corpse

  data_train_lib = []
  for i in range(len(lib[0:1000])):
    tmp = []
    for j in range(len(columns)):
      if j == 0:
        tmp.append(1)
      else:
        tmp.append(lib[i].count(columns[j]))
    data_train_lib.append(tmp)
  
  data_test_lib = []
  for i in range(len(lib[1000:1700])):
    tmp = []
    for j in range(len(columns)):
      if j == 0:
        tmp.append(1)
      else:
        tmp.append(lib[i+1000].count(columns[j]))
    data_test_lib.append(tmp)

  data_train_con = []
  for i in range(len(con[0:1000])):
    tmp = []
    for j in range(len(columns)):
      if j == 0:
        tmp.append(0)
      else:
        tmp.append(con[i].count(columns[j]))
    data_train_con.append(tmp)
  
  data_test_con = []
  for i in range(len(con[1000:1700])):
    tmp = []
    for j in range(len(columns)):
      if j == 0:
        tmp.append(0)
      else:
        tmp.append(con[i+1000].count(columns[j]))
    data_test_con.append(tmp)
  #create numpy array to use dataframe
  numpy_array_train_lib = np.asarray(data_train_lib)
  numpy_array_test_lib = np.asarray(data_test_lib)
  numpy_array_train_con = np.asarray(data_train_con)
  numpy_array_test_con = np.asarray(data_test_con)
  df_train = pd.concat([pd.DataFrame(numpy_array_train_lib, columns = columns), pd.DataFrame(numpy_array_train_con, columns = columns)])
  df_test = pd.concat([pd.DataFrame(numpy_array_test_lib, columns = columns), pd.DataFrame(numpy_array_test_con, columns = columns)])
  return [df_train, df_test]

def pick_subset(anchor_words):
  s=set(stopwords.words('english'))
  features = [];
  word_freq = {}
  for sent in lib[0: 1000]:
    sentence = re.sub("[^(a-rt-zA-z\s')]", "", sent).replace("`","").replace("(","").replace(")","").replace("	"," ")
    sent_list = sentence.split()
    if anchor_words in sent_list and sent_list.index(anchor_words) > 0:
      pref = sent_list[sent_list.index(anchor_words)-1];
      if (pref in word_freq):
        word_freq[pref] += 1
      else:
        word_freq[pref] = 1
  for sent in con[0: 1000]:
    sentence = re.sub("[^(a-rt-zA-z\s')]", "", sent).replace("`","").replace("(","").replace(")","").replace("	"," ")
    sent_list = sentence.split()
    if anchor_words in sent_list and sent_list.index(anchor_words) > 0:
      pref = sent_list[sent_list.index(anchor_words)-1];
      if (pref in word_freq):
        word_freq[pref] += 1
      else:
        word_freq[pref] = 1
  word_freq_sorted = sorted(word_freq.items(), key=operator.itemgetter(1))
  count = 0
  word_freq_sorted.reverse()
  if len(word_freq_sorted) > 0:
    while word_freq_sorted[count][1] > 3:
      if word_freq_sorted[count][0] not in s:
        features.append(word_freq_sorted[count][0])
      count += 1
    if len(features) > 0:
      print "word ", anchor_words, " features "
    return features
  else:
    return []

def add_prefix_features(biased_words):
  #we take top 5 words from liberal biased and top 5 words from conservative
  features = biased_words
  count = 0
  ind = 0
  featured_words = 0
  while ind < 100:
    new_features = pick_subset(biased_words[ind])
    if (len(new_features) > 0):
      featured_words += len(new_features)
      features = features + new_features
      count += 1
    ind += 1
  # print featured_words
  return features

def run_decision_tree(ind):
  df = create_dataframe(ind)
  df_train = df[0]
  df_test = df[1]
  
  model = tree.DecisionTreeClassifier()
  model.fit(df_train.drop('ideology', axis=1), df_train['ideology'])
  # print model
  y = df_test['ideology']
  y_predict = model.predict(df_test.drop('ideology', axis=1))
  print accuracy_score(y, y_predict)
  # pd.DataFrame(
  #   confusion_matrix(y, y_predict),
  #   columns=['Predicted Not Liberal', 'Predicted Liberal'],
  #   index=['True Not Liberal', 'True Liberal']
  # )
  dot_data = tree.export_graphviz(model, out_file='tree.dot', feature_names=df_train.drop('ideology', axis=1).columns)
  # call(['dot', '-T', 'png', 'tree.dot', '-o', 'tree.png'])
  # graph = graphviz.Source(dot_data) 
  # graph
# run_decision_tree()
run_decision_tree(-1)
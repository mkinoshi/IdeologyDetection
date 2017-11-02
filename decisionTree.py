import pandas as pd
from BiasedWordsNgram import extract_biased_words
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

def create_dataframe():
  #create word corpse
  words_corpse = list(set(extract_biased_words(1)))
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
  for word in anchor_words:
    word_freq = {}
    for sent in lib[0: 1000]:
      sentence = re.sub("[^(a-rt-zA-z\s')]", "", sent).replace("`","").replace("(","").replace(")","").replace("	"," ")
      sent_list = sentence.split()
      if word in sent_list and sent_list.index(word) > 0:
        pref = sent_list[sent_list.index(word)-1];
        if (pref in word_freq):
          word_freq[pref] += 1
        else:
          word_freq[pref] = 1
    for sent in con[0: 1000]:
      sentence = re.sub("[^(a-rt-zA-z\s')]", "", sent).replace("`","").replace("(","").replace(")","").replace("	"," ")
      sent_list = sentence.split()
      if word in sent_list and sent_list.index(word) > 0:
        pref = sent_list[sent_list.index(word)-1];
        if (pref in word_freq):
          word_freq[pref] += 1
        else:
          word_freq[pref] = 1
    word_freq_sorted = sorted(word_freq.items(), key=operator.itemgetter(1)).reverse()
    count = 0
    print len(word_freq_sorted)
    while word_freq_sorted[count][1] > 3:
      if word_freq_sorted[count][0] not in s:
        features.append(word_freq_sorted[count][0])
      count += 1

    print features

def run_decision_tree():
  df = create_dataframe()
  df_train = df[0]
  df_test = df[1]
  
  model = tree.DecisionTreeClassifier()
  model.fit(df_train.drop('ideology', axis=1), df_train['ideology'])
  print model
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
pick_subset(["government"])
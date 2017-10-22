# Tatsuya Yokota
# 10/20/2017
# Implementation of BoW kmeans classification on the IBC data set

import cPickle
import re
import numpy as np

# libraries used to tokenize article
from stop_words import get_stop_words
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer

# BoW implementation
from gensim import corpora, matutils

# classification model
from sklearn.cluster import KMeans
from BiasedWordsNgram import extract_biased_words
import sys

"""
Pre-processing tools 
"""
en_stop = get_stop_words('en')
p_stemmer = PorterStemmer()

################ helper functions ################
	
# tokenizes the given string
# 	takes in string
# 	returns list of strings 
def toknize_article(doc):
	
	# tokenize, remove stop words and single/double letter words, stem
	tokens = doc.split()
	tokens = [text for text in tokens if text not in en_stop and len(text) > 2]
# 	tokens = [p_stemmer.stem(text) for text in tokens]
	
	return tokens
	

# vectorizes the given string based on the Corpora dictionary
# 	takes in a list of article strings
# 	returns a numpy matrix, with each row representing a unique word in the dictionary
#		and each col representing a single article
def vectorize_articles(tokenized_docs, dict):
	
	
	corpus = [dict.doc2bow(article) for article in tokenized_docs]
	num_terms = len(dict.values())
	num_docs = len(tokenized_docs)
	
	# convert corpus into matrix and transpose
	# matrix shape is: 
	#	row: # of docs
	#	col: # of terms
	matrix = matutils.corpus2dense(corpus, num_terms, num_docs).T
	print matrix	
	print "Shape of docs matrix is: ", matrix.shape
	print "# of documents", num_docs
	print "# of unique terms: ", num_terms

	
	return matrix


################ main function ################	

def main(lib_docs, con_docs, lib_test_docs, con_test_docs, ind):
	### MODEL CONSTRUCTION ###
	
	# tokenize the docs
	lib_tokenized_docs = []
	con_tokenized_docs = []
	
	for sentence in lib_docs:
		tokens = toknize_article(sentence)
		lib_tokenized_docs.append(tokens)
	
	for sentence in con_docs:
		tokens = toknize_article(sentence)
		con_tokenized_docs.append(tokens)
	
	# concat tokenized_docs lists
	all_tokenized_docs = lib_tokenized_docs + con_tokenized_docs
	
	# if ind = 0, use tokenzied words to crate dic, if ind = 1 use extracted 100 biased words with length = 2 for each
	# if ind = 2  use extracted 100 biased words with length = 3 for each
	if ind == 0:		
		# use all_tokenized_docs so that matrix's # of features matches
		dict =  corpora.Dictionary(all_tokenized_docs)
	elif ind == 1:
		dict = corpora.Dictionary(BiasedWordsNgram(ind))
	else:
		dict = corpora.Dictionary(BiasedWordsNgram(ind))
	
	# create matrix for each category
	lib_docs_matrix = vectorize_articles(lib_tokenized_docs, dict)
	con_docs_matrix = vectorize_articles(con_tokenized_docs, dict)
	
	# take mean of all rows and get a vector representing the average sentence for 
	# each category
	lib_mean_vector = lib_docs_matrix.mean(axis=0)
	con_mean_vector = con_docs_matrix.mean(axis=0)
	
	print lib_mean_vector
	print lib_mean_vector.shape
	print con_mean_vector
	print con_mean_vector.shape
	
	X = np.vstack((lib_mean_vector, con_mean_vector))
	
	kmeans = KMeans(n_clusters=2, random_state=0).fit(X)
	
	
	### TESTING ###
	
	# tokenize the test docs
	lib_tokenized_test_docs = []
	con_tokenized_test_docs = []
	
	for sentence in lib_docs:
		tokens = toknize_article(sentence)
		lib_tokenized_test_docs.append(tokens)
	
	for sentence in con_docs:
		tokens = toknize_article(sentence)
		con_tokenized_test_docs.append(tokens)
	
	# create matrix for each category
	lib_test_docs_matrix = vectorize_articles(lib_tokenized_test_docs, dict)
	con_test_docs_matrix = vectorize_articles(con_tokenized_test_docs, dict)
	
	
	
	lib_result = kmeans.predict(lib_test_docs_matrix)
	
	con_result = kmeans.predict(con_test_docs_matrix)
	
	lib_hit = float(np.count_nonzero(lib_result == 0))
	con_hit = float(np.count_nonzero(con_result == 1))
	
	lib_accuracy = lib_hit/len(lib_result)
	con_accuracy = con_hit/len(con_result)
	
	print "Liberal Accuracy: ", lib_accuracy
	print "Conservative Accuracy: ", con_accuracy


if __name__ == '__main__':
	if len(sys.argv) < 2:
		print "You need one more agument"
		print "0: normal bug of words k means, 1: using  extracted biased words (length = 2) Pearson's chai square to, 2: using  extracted biased words (length = 2) Pearson's chai square to"
	else:
		[lib, con, neutral] = cPickle.load(open('ibcData.pkl', 'rb'))
		
		# 	print len(lib)
		# 	print len(con)
		# 	exit()
		
		lib_docs = []
		con_docs = []
		lib_test_docs = []
		con_test_docs = []
		
		# collect the training data 
		for tree in lib[0:1000]:
			# pre-process doc. 
			sentence = re.sub("[^(a-rt-zA-z\s)]", "", tree.get_words()).replace("`","").replace("(","").replace(")","").replace("	"," ")
			lib_docs.append(sentence)
		
		for tree in con[0:1000]:
			# pre-process doc. 
			sentence = re.sub("[^(a-rt-zA-z\s)]", "", tree.get_words()).replace("`","").replace("(","").replace(")","").replace("	"," ")
			con_docs.append(sentence)
		
		
		# collect the testing data
		for tree in lib[1000:1700]:
			# pre-process doc. 
			sentence = re.sub("[^(a-rt-zA-z\s)]", "", tree.get_words()).replace("`","").replace("(","").replace(")","").replace("	"," ")
			lib_test_docs.append(sentence)
			
		for tree in con[1000:1700]:
			# pre-process doc. 
			sentence = re.sub("[^(a-rt-zA-z\s)]", "", tree.get_words()).replace("`","").replace("(","").replace(")","").replace("	"," ")
			con_test_docs.append(sentence)
		 
		main(lib_docs, con_docs, lib_test_docs, con_test_docs, sys.argv[1])	
		# loop through training data and get a list of all article strings
		# create a dicitonary based on that, and tokenize articles while doing so
		# 
		# want to get vector representation of each training article
		# so, use dict.doc2bow(tokens) to get list of tuples with id and frequency of word in tokens
		# 	e.g. [(0, 1), (4, 1), (7, 1)] 
		# 
		# change this information into a numpy matrix where id is the row number and the 
		# 	frequency is the value in the vector. Each article is a column. 
		# 
		# Now, run k-means clustering with K = 2.
		# Put in one 
		# 	



		# take mean of each category, run PCA and reduce number of features to 3, 
		# we end up with two data points in 3-D, each representing the mean of their categories
		# find the middle value??



		# take out the words that only appear once throughout all documents
		# 
		# 
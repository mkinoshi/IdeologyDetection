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

# PCA function
from PCA import pca

# plotting library
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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
	tokens = [text.lower() for text in tokens if text.lower() not in en_stop and len(text) > 2]
	tokens = [p_stemmer.stem(text) for text in tokens]
	
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

# returns the cutoff index where cumulative percent of variance is explained 
def pca_cutoff(eigen_vals, cutoff_perc):
	# take total eigenvalue and do a cumulative summing procedure
	# keep till cutoff_perc
       	total_eval = sum(eigen_vals)
	cumulative = 0.
	for row in range(eigen_vals.shape[0]):

		cumulative += eigen_vals[row]/total_eval
		if cumulative > cutoff_perc:
			return row


# returns a list of words with high variance in the given eignevector direction
def find_topn_words(eigen_vector, dict, n=10):
	ind = np.argpartition(np.absolute(eigen_vector), -n)[-n:]
	words = []
	for i in ind:
		words.append(dict.get(i))
	return words

# uses matplotlib to visualize projection of data 
#def plot_over_vecs(x_vec, y_vec, data_matrix):

def two_dim_eigenplot(lib_xy, con_xy):
	plt.plot(lib_xy[0], lib_xy[1], 'bo', con_xy[0], con_xy[1], 'ro')
	plt.xlabel('eigenvector 0')
	plt.ylabel('eigenvector 1')
	plt.show()

	
def three_dim_eigenplot(lib_xyz, con_xyz):
	fig = plt.figure()
	ax = Axes3D(fig)
	ax.scatter(lib_xyz[0], lib_xyz[1], lib_xyz[2], c='b', marker='o')
	ax.scatter(con_xyz[0], con_xyz[1], con_xyz[2], c='r', marker='o')
	ax.set_xlabel('eigenvector 0')
	ax.set_ylabel('eigenvector 1')
	ax.set_zlabel('eigenvector 2')

	plt.show()

################ main function ################	

def main(lib_docs, con_docs, lib_test_docs, con_test_docs, num_evecs, num_words, cutoff=False, cutoff_rate=1.0):
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
	
	# use all_tokenized_docs so that matrix's # of features matches
	dict =  corpora.Dictionary(all_tokenized_docs)
	
	# create matrix for each category
	lib_docs_matrix = vectorize_articles(lib_tokenized_docs, dict)
	con_docs_matrix = vectorize_articles(con_tokenized_docs, dict)
	
	# stack them and use it to do PCA on whole training data
	all_docs_matrix = np.vstack((lib_docs_matrix, con_docs_matrix))
	
	(proj_matrix, e_vecs, e_vals)=  pca(all_docs_matrix)
	
       	print lib_docs_matrix.shape
	print con_docs_matrix.shape

	# project each category matrix onto the transpose of eigenvector matrix	
	
	if cutoff:
		cutoff_index = pca_cutoff(e_vals, cutoff_rate)
		lib_proj_matrix = np.dot(lib_docs_matrix, e_vecs.T)[:,:cutoff_index]
		con_proj_matrix = np.dot(con_docs_matrix, e_vecs.T)[:,:cutoff_index]
	else:
		lib_proj_matrix = np.dot(lib_docs_matrix, e_vecs.T)
		con_proj_matrix = np.dot(con_docs_matrix, e_vecs.T)
	
	print lib_proj_matrix.shape
	print con_proj_matrix.shape
	
	
	# take mean of all rows and get a vector representing the average sentence for 
	# each category
	lib_mean_vector = lib_proj_matrix.mean(axis=0)
	con_mean_vector = con_proj_matrix.mean(axis=0)
	
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
	

	# project each matrix to eigenspace
	if cutoff:
		lib_proj_test_matrix = np.dot(lib_test_docs_matrix, e_vecs.T)[:,:cutoff_index]
		con_proj_test_matrix = np.dot(con_test_docs_matrix, e_vecs.T)[:,:cutoff_index]
	else:
		lib_proj_test_matrix = np.dot(lib_test_docs_matrix, e_vecs.T)
		con_proj_test_matrix = np.dot(con_test_docs_matrix, e_vecs.T)
	
	

	lib_result = kmeans.predict(lib_proj_test_matrix)
	con_result = kmeans.predict(con_proj_test_matrix)
	
	lib_hit = float(np.count_nonzero(lib_result == 0))
	con_hit = float(np.count_nonzero(con_result == 1))
	
	lib_accuracy = lib_hit/len(lib_result)
	con_accuracy = con_hit/len(con_result)
	
	print "Liberal Accuracy: ", lib_accuracy
	print "Conservative Accuracy: ", con_accuracy
	

	# find the top n words for the top m eigenvectors
	for row in range(num_evecs):
		print find_topn_words(e_vecs[row,:], dict, num_words)

	
	# plot along eigenvectors
	lib_x = lib_proj_test_matrix[:,0]
	lib_y = lib_proj_test_matrix[:,1]
	con_x = con_proj_test_matrix[:,0]
	con_y = con_proj_test_matrix[:,1]
	lib_z = lib_proj_test_matrix[:,2]
	con_z = con_proj_test_matrix[:,2]
	
	lib_xyz = [lib_x, lib_y, lib_z]
	con_xyz = [con_x, con_y, lib_z]
	
	two_dim_eigenplot(lib_xyz[:2], con_xyz[:2])
	three_dim_eigenplot(lib_xyz, con_xyz)


if __name__ == '__main__':
	# user input for cutoff and influtential word seach.
	cutoff = raw_input("Cut off matrix?[y/n] ")
	if cutoff.lower() == 'y':
		rate = float(raw_input("Give percentage of variance: "))
	num_evecs = int(raw_input("How many eigenvectors to search for? " ))
	if num_evecs != 0:
		num_words = int(raw_input("How many words to search for in each eigenvector? "))
	else:
		num_words = 0

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
	
	# ask whether to cut off or not 
	if cutoff.lower() == 'y':
		main(lib_docs, con_docs, lib_test_docs, con_test_docs, 
		     num_evecs, num_words, cutoff=True, cutoff_rate=rate)
	else:
		main(lib_docs, con_docs, lib_test_docs, con_test_docs, num_evecs, num_words)
	
	
	
	
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

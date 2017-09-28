import cPickle
import re
import math

# tfidf vs. countvectorizer in sklearn
# https://stackoverflow.com/questions/22489264/is-a-countvectorizer-the-same-as-tfidfvectorizer-with-use-idf-false
# stacking two features 
# https://stackoverflow.com/questions/27496014/does-it-make-sense-to-use-both-countvectorizer-and-tfidfvectorizer-as-feature-ve
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

from stop_words import get_stop_words
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer



if __name__ == '__main__':
	[lib, con, neutral] = cPickle.load(open('ibcData.pkl', 'rb'))
	
	print len(lib)
	print len(con)
	print len(neutral)
	exit()

	"""
	Adjustable variables
	"""
	training_limit = 0.6 # proportion of training data
	
	"""
	Storage vars
	"""
	sentence_list = []
	target_val_list = []
	test_sentence_list = []
	test_target_val_list = []
	
	"""
	Pre-processing tools / BoW tools
	"""
	en_stop = get_stop_words('en')
	p_stemmer = PorterStemmer()
	vectorizer = CountVectorizer()
	tfidf_transformer = TfidfTransformer()
	
	# loop through all sentences in all categories, and build up sentence_list and target_val_list
	
	# liberal
	for tree in lib[0:int(len(lib)*training_limit)]:
		# pre-process doc. 
		sentence = re.sub("[^(a-rt-zA-z\s)]", "", tree.get_words()).replace("`","").replace("(","").replace(")","").replace("	"," ")

		# tokenize, remove stop words and single/double letter words, stem
		tokens = sentence.split()
		stopped_tokens = [text for text in tokens if text not in en_stop and len(text) > 2]
		stemmed_tokens = [p_stemmer.stem(text) for text in stopped_tokens]
		
		# join words into single string separated by a space
		sentence = " ".join( stemmed_tokens )

		print sentence
		sentence_list.append(sentence)
		target_val_list.append(1)
	
	# conservative
	for tree in con[0:int(len(con)*training_limit)]:
		# pre-process doc. 
		sentence = re.sub("[^(a-rt-zA-z\s)]", "", tree.get_words()).replace("`","").replace("(","").replace(")","").replace("	"," ")

		# tokenize, remove stop words and single/double letter words, stem
		tokens = sentence.split()
		stopped_tokens = [text for text in tokens if text not in en_stop and len(text) > 2]
		stemmed_tokens = [p_stemmer.stem(text) for text in stopped_tokens]
		
		# join words into single string separated by a space
		sentence = " ".join( stemmed_tokens )

		print sentence
		sentence_list.append(sentence)
		target_val_list.append(2)
	
	# neutral 
	
	for tree in neutral[0:int(len(neutral)*training_limit)]:
		# pre-process doc. 
		sentence = re.sub("[^(a-rt-zA-z\s)]", "", tree.get_words()).replace("`","").replace("(","").replace(")","").replace("	"," ")

		# tokenize, remove stop words and single/double letter words, stem
		tokens = sentence.split()
		stopped_tokens = [text for text in tokens if text not in en_stop and len(text) > 2]
		stemmed_tokens = [p_stemmer.stem(text) for text in stopped_tokens]
		
		# join words into single string separated by a space
		sentence = " ".join( stemmed_tokens )

		print sentence
		sentence_list.append(sentence)
		target_val_list.append(3)
	
	
	# create bag_of_words
	doc_counts = vectorizer.fit_transform(sentence_list) # assigns id to each word and figures out freq. of each word

	print doc_counts
	
	# tf-idf (term-frequency inverse document frequency)
	# "term-frequency times inverse document-frequency"
	doc_tfidf = tfidf_transformer.fit_transform(doc_counts)
	
	print doc_tfidf.shape
	
	# MultinomialNB().fit(tfidf, target_values)
	clf = MultinomialNB().fit(doc_tfidf, target_val_list)
	
	
	
	
	# test accuracy of model
	for tree in lib[int(len(lib)*training_limit)+1:]:
		# pre-process doc. 
		sentence = re.sub("[^(a-rt-zA-z\s)]", "", tree.get_words()).replace("`","").replace("(","").replace(")","").replace("	"," ")

		# tokenize, remove stop words and single/double letter words, stem
		tokens = sentence.split()
		stopped_tokens = [text for text in tokens if text not in en_stop and len(text) > 2]
		stemmed_tokens = [p_stemmer.stem(text) for text in stopped_tokens]
		
		# join words into single string separated by a space
		sentence = " ".join( stemmed_tokens )

		print sentence
		test_sentence_list.append(sentence)
		test_target_val_list.append(1)
	
	for tree in con[int(len(con)*training_limit)+1:]:
		# pre-process doc. 
		sentence = re.sub("[^(a-rt-zA-z\s)]", "", tree.get_words()).replace("`","").replace("(","").replace(")","").replace("	"," ")

		# tokenize, remove stop words and single/double letter words, stem
		tokens = sentence.split()
		stopped_tokens = [text for text in tokens if text not in en_stop and len(text) > 2]
		stemmed_tokens = [p_stemmer.stem(text) for text in stopped_tokens]
		
		# join words into single string separated by a space
		sentence = " ".join( stemmed_tokens )

		print sentence
		test_sentence_list.append(sentence)
		test_target_val_list.append(2)
	
	for tree in neutral[int(len(neutral)*training_limit)+1:]:
		# pre-process doc. 
		sentence = re.sub("[^(a-rt-zA-z\s)]", "", tree.get_words()).replace("`","").replace("(","").replace(")","").replace("	"," ")

		# tokenize, remove stop words and single/double letter words, stem
		tokens = sentence.split()
		stopped_tokens = [text for text in tokens if text not in en_stop and len(text) > 2]
		stemmed_tokens = [p_stemmer.stem(text) for text in stopped_tokens]
		
		# join words into single string separated by a space
		sentence = " ".join( stemmed_tokens )

		print sentence
		test_sentence_list.append(sentence)
		test_target_val_list.append(3)
	
	
	
	test_counts = vectorizer.transform(test_sentence_list)
	test_tfidf = tfidf_transformer.transform(test_counts)
	
	# predict for each test sentence
	predicted = clf.predict(test_tfidf)
	
	
	# calculate accuracy 
	correct = 0
	for answer, guess in zip(test_target_val_list, predicted):
		if answer == guess:
			correct += 1
		print answer, guess
	
	print float(correct)/float(len(test_target_val_list))
	
	
	
	
	
	
	
	
	
	
	
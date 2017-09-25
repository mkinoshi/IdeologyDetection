import cPickle
import re
import math

# luckily, data is organized into sentences, so no real difficulty in adding the <s> and 
# </s> tags. 

if __name__ == '__main__':
	[lib, con, neutral] = cPickle.load(open('ibcData.pkl', 'rb'))

	"""
	Adjustable variables
	"""
	n = 2 # define n-gram here
	training_limit = 0.6 # proportion of training data
	
	"""
	Dicts to store info
	"""
	lib_dict_seq = {} 
	lib_dict_uni = {}
	lib_ngram_probs = {}
	con_dict_seq = {} 
	con_dict_uni = {}
	con_ngram_probs = {}
	neu_dict_seq = {} 
	neu_dict_uni = {}
	neu_ngram_probs = {}
	
	
	"""
	Liberal corpus training
	"""
	# create uni-gram count
	lib_dict_uni["<UNK>"] = 0
# 	for tree in lib[0:4]: 
	for tree in lib[0:int(len(lib)*training_limit)]:
		start_tag = "<s> "
		sentence = re.sub("[^(a-rt-zA-z\s')]", "", tree.get_words()).replace("`","").replace("(","").replace(")","").replace("	"," ")
		end_tag = "</s> "
		
		sentence_list = (start_tag*(n-1)+sentence+end_tag*(n-1)).split()
	  	
	  	print sentence_list
	  	for i in range(len(sentence_list)):
			if i < len(sentence_list)-1:
			
				# count individual word frequency
				cur_word = sentence_list[i]
				print cur_word
				if cur_word in lib_dict_uni:
					lib_dict_uni[cur_word] += 1
				else:
					# set inital count to 0 b/c need to give it to <UNK> key later
					lib_dict_uni[cur_word] = 0

	# take <UNK> in as key
	lib_dict_uni_COPY = lib_dict_uni.copy()
	lib_dict_uni["<UNK>"] = len(lib_dict_uni)
	for key in lib_dict_uni_COPY:
		
		if lib_dict_uni[key] == 0:
			lib_dict_uni.pop(key)
	
	
	
	print lib_dict_uni

	
	# create seq n-gram count 
# 	for tree in lib[0:4]:
	for tree in lib[0:int(len(lib)*training_limit)]:
		start_tag = "<s> "
		sentence = re.sub("[^(a-rt-zA-z\s')]", "", tree.get_words()).replace("`","").replace("(","").replace(")","").replace("	"," ")
		end_tag = "</s> "
		
# 		print start_tag*(n-1)+sentence+end_tag*(n-1)
	  	
	  	sentence_list = (start_tag*(n-1)+sentence+end_tag*(n-1)).split()
		
		print sentence_list
	  	for i in range(len(sentence_list)):
			if i < len(sentence_list)-1:
				# create seq
				seq_list = []
				for word in sentence_list[i : i+n]:
					if word not in lib_dict_uni:
						seq_list.append("<UNK>")
					else:
						seq_list.append(word)
				
				print seq_list
				seq = " ".join(seq_list)
				print i, i+n, seq
			
				# add to lib_dict_seq
				if seq in lib_dict_seq:
					lib_dict_seq[seq][0] += 1
				else:
					lib_dict_seq[seq] = [1, seq_list]
	
	print lib_dict_seq
	
	
	"""
	Conservative 
	"""
	# create uni-gram count
	con_dict_uni["<UNK>"] = 0
# 	for tree in lib[0:4]: 
	for tree in con[0:int(len(con)*training_limit)]:
		start_tag = "<s> "
		sentence = re.sub("[^(a-rt-zA-z\s')]", "", tree.get_words()).replace("`","").replace("(","").replace(")","").replace("	"," ")
		end_tag = "</s> "
		
		sentence_list = (start_tag*(n-1)+sentence+end_tag*(n-1)).split()
	  	
	  	print sentence_list
	  	for i in range(len(sentence_list)):
			if i < len(sentence_list)-1:
			
				# count individual word frequency
				cur_word = sentence_list[i]
				print cur_word
				if cur_word in con_dict_uni:
					con_dict_uni[cur_word] += 1
				else:
					# set inital count to 0 b/c need to give it to <UNK> key later
					con_dict_uni[cur_word] = 0

	# take <UNK> in as key
	con_dict_uni_COPY = con_dict_uni.copy()
	con_dict_uni["<UNK>"] = len(con_dict_uni)
	for key in con_dict_uni_COPY:
		
		if con_dict_uni[key] == 0:
			con_dict_uni.pop(key)
	
	
	
	print con_dict_uni

	
	# create seq n-gram count 
# 	for tree in lib[0:4]:
	for tree in con[0:int(len(con)*training_limit)]:
		start_tag = "<s> "
		sentence = re.sub("[^(a-rt-zA-z\s')]", "", tree.get_words()).replace("`","").replace("(","").replace(")","").replace("	"," ")
		end_tag = "</s> "
		
# 		print start_tag*(n-1)+sentence+end_tag*(n-1)
	  	
	  	sentence_list = (start_tag*(n-1)+sentence+end_tag*(n-1)).split()
		
		print sentence_list
	  	for i in range(len(sentence_list)):
			if i < len(sentence_list)-1:
				# create seq
				seq_list = []
				for word in sentence_list[i : i+n]:
					if word not in con_dict_uni:
						seq_list.append("<UNK>")
					else:
						seq_list.append(word)
				
				print seq_list
				seq = " ".join(seq_list)
				print i, i+n, seq
			
				# add to lib_dict_seq
				if seq in con_dict_seq:
					con_dict_seq[seq][0] += 1
				else:
					con_dict_seq[seq] = [1, seq_list]
	
	print con_dict_seq
	
	"""
	Neutral
	"""
	# create uni-gram count
	neu_dict_uni["<UNK>"] = 0
# 	for tree in lib[0:4]: 
	for tree in neutral[0:int(len(neutral)*training_limit)]:
		start_tag = "<s> "
		sentence = re.sub("[^(a-rt-zA-z\s')]", "", tree.get_words()).replace("`","").replace("(","").replace(")","").replace("	"," ")
		end_tag = "</s> "
		
		sentence_list = (start_tag*(n-1)+sentence+end_tag*(n-1)).split()
	  	
	  	print sentence_list
	  	for i in range(len(sentence_list)):
			if i < len(sentence_list)-1:
			
				# count individual word frequency
				cur_word = sentence_list[i]
				print cur_word
				if cur_word in neu_dict_uni:
					neu_dict_uni[cur_word] += 1
				else:
					# set inital count to 0 b/c need to give it to <UNK> key later
					neu_dict_uni[cur_word] = 0

	# take <UNK> in as key
	neu_dict_uni_COPY = neu_dict_uni.copy()
	neu_dict_uni["<UNK>"] = len(neu_dict_uni)
	for key in neu_dict_uni_COPY:
		
		if neu_dict_uni[key] == 0:
			neu_dict_uni.pop(key)
	
	
	
	print neu_dict_uni

	
	# create seq n-gram count 
# 	for tree in lib[0:4]:
	for tree in neutral[0:int(len(neutral)*training_limit)]:
		start_tag = "<s> "
		sentence = re.sub("[^(a-rt-zA-z\s')]", "", tree.get_words()).replace("`","").replace("(","").replace(")","").replace("	"," ")
		end_tag = "</s> "
		
# 		print start_tag*(n-1)+sentence+end_tag*(n-1)
	  	
	  	sentence_list = (start_tag*(n-1)+sentence+end_tag*(n-1)).split()
		
		print sentence_list
	  	for i in range(len(sentence_list)):
			if i < len(sentence_list)-1:
				# create seq
				seq_list = []
				for word in sentence_list[i : i+n]:
					if word not in neu_dict_uni:
						seq_list.append("<UNK>")
					else:
						seq_list.append(word)
				
				print seq_list
				seq = " ".join(seq_list)
				print i, i+n, seq
			
				# add to lib_dict_seq
				if seq in neu_dict_seq:
					neu_dict_seq[seq][0] += 1
				else:
					neu_dict_seq[seq] = [1, seq_list]
	
	print neu_dict_seq
	
	
	
	
	# Test set loop on lib
	correct1 = 0
	correct2 = 0
	correct3 = 0
	lib_cat = 0
	con_cat = 0
	neu_cat = 0
	for tree in lib[int(len(lib)*training_limit)+1:]:
		start_tag = "<s> "
		sentence = re.sub("[^(a-rt-zA-z\s')]", "", tree.get_words()).replace("`","").replace("(","").replace(")","").replace("	"," ")
		end_tag = "</s> "
	
# 		print start_tag*(n-1)+sentence+end_tag*(n-1)
	
		sentence_list = (start_tag*(n-1)+sentence+end_tag*(n-1)).split()
	
		lib_sentence_probs = []
		con_sentence_probs = []
		neu_sentence_probs = []
		for i in range(len(sentence_list)):
			if i < len(sentence_list)-1:
				"""
				Lib seq
				"""
				# create seq
				seq_list = []
				for word in sentence_list[i : i+n]:
					if word not in lib_dict_uni:
						seq_list.append("<UNK>")
					else:
						seq_list.append(word)
				
				seq = " ".join(seq_list)
# 				print i, i+n, seq
				
				
				# if seq is in lib_dict_seq, do normal plus 1
				if seq in lib_dict_seq:
					seq_count = lib_dict_seq[seq][0] + 1
					initword = seq_list[0]
					initword_count = lib_dict_uni[initword]
				else:
					seq_count = 1
					initword = seq_list[0]
					initword_count = lib_dict_uni[initword]
				# calculate n-gram prob for each nth word and store in dict.
				lib_sentence_probs.append(float(seq_count) / float(initword_count))
				
				"""
				Con seq
				"""
				
				# create seq
				seq_list = []
				for word in sentence_list[i : i+n]:
					if word not in con_dict_uni:
						seq_list.append("<UNK>")
					else:
						seq_list.append(word)
				
				seq = " ".join(seq_list)
				
				# if seq is in con_dict_seq, do normal plus 1
				if seq in con_dict_seq:
					seq_count = con_dict_seq[seq][0] + 1
					initword = seq_list[0]
					initword_count = con_dict_uni[initword]
				else:
					seq_count = 1
					initword = seq_list[0]
					initword_count = con_dict_uni[initword]
				# calculate n-gram prob for each nth word and store in dict.
				con_sentence_probs.append(float(seq_count) / float(initword_count))
				
				"""
				Neutral seq
				"""
				
				# create seq
				seq_list = []
				for word in sentence_list[i : i+n]:
					if word not in neu_dict_uni:
						seq_list.append("<UNK>")
					else:
						seq_list.append(word)
				
				seq = " ".join(seq_list)
				
				# if seq is in neu_dict_seq, do normal plus 1
				if seq in neu_dict_seq:
					seq_count = neu_dict_seq[seq][0] + 1
					initword = seq_list[0]
					initword_count = neu_dict_uni[initword]
				else:
					seq_count = 1
					initword = seq_list[0]
					initword_count = neu_dict_uni[initword]
				# calculate n-gram prob for each nth word and store in dict.
				neu_sentence_probs.append(float(seq_count) / float(initword_count))
		
		
		# convert raw probabilities to log probabilities
		lib_log_probs = list(map(math.log, lib_sentence_probs))
		con_log_probs = list(map(math.log, con_sentence_probs))
		neu_log_probs = list(map(math.log, neu_sentence_probs))
		
		# summing up log probs is equivalent to multiplying raw probs
		# convert log prob to raw prob by taking its exponent 
		lib_prob = math.exp(sum(lib_log_probs))
		con_prob = math.exp(sum(con_log_probs))
		neu_prob = math.exp(sum(neu_log_probs))

# 		print "----------"
# 		print lib_prob
# 		print con_prob
# 		print neu_prob
		
		if lib_prob > con_prob and lib_prob > neu_prob:
# 			print start_tag*(n-1)+sentence+end_tag*(n-1)
			correct1 += 1
		
		if lib_prob > con_prob:
			correct2 += 1
			
		if lib_prob > neu_prob:
# 			print start_tag*(n-1)+sentence+end_tag*(n-1)
			correct3 += 1
			
		
		if lib_prob > con_prob and lib_prob > neu_prob:
			lib_cat += 1
		elif  con_prob > lib_prob and con_prob > neu_prob:
			con_cat += 1
		elif neu_prob > lib_prob and neu_prob > con_prob:
			neu_cat += 1
	
	print "########Liberal Test Set########"
	print "Accuracy out of lib vs. con vs. neu: ", float(correct1)/float(len(lib[int(len(lib)*training_limit)+1:]))
	print "Accuracy, lib vs. con: ", float(correct2)/float(len(lib[int(len(lib)*training_limit)+1:]))
	print "Accuracy, lib vs. neu: ", float(correct3)/float(len(lib[int(len(lib)*training_limit)+1:]))
	print "Out of "+str(len(lib[int(len(lib)*training_limit)+1:]))+" liberal articles, "
	print "Labeled Liberal: ",lib_cat
	print "Labeled Conservative: ",con_cat
	print "Labeled Neutral: ", neu_cat
	
	
	
	# Test set loop on lib
	correct1 = 0
	correct2 = 0
	correct3 = 0
	lib_cat = 0
	con_cat = 0
	neu_cat = 0
	for tree in con[int(len(con)*training_limit)+1:]:
		start_tag = "<s> "
		sentence = re.sub("[^(a-rt-zA-z\s')]", "", tree.get_words()).replace("`","").replace("(","").replace(")","").replace("	"," ")
		end_tag = "</s> "
	
# 		print start_tag*(n-1)+sentence+end_tag*(n-1)
	
		sentence_list = (start_tag*(n-1)+sentence+end_tag*(n-1)).split()
	
		lib_sentence_probs = []
		con_sentence_probs = []
		neu_sentence_probs = []
		for i in range(len(sentence_list)):
			if i < len(sentence_list)-1:
				"""
				Lib seq
				"""
				# create seq
				seq_list = []
				for word in sentence_list[i : i+n]:
					if word not in lib_dict_uni:
						seq_list.append("<UNK>")
					else:
						seq_list.append(word)
				
				seq = " ".join(seq_list)
# 				print i, i+n, seq
				
				
				# if seq is in lib_dict_seq, do normal plus 1
				if seq in lib_dict_seq:
					seq_count = lib_dict_seq[seq][0] + 1
					initword = seq_list[0]
					initword_count = lib_dict_uni[initword]
				else:
					seq_count = 1
					initword = seq_list[0]
					initword_count = lib_dict_uni[initword]
				# calculate n-gram prob for each nth word and store in dict.
				lib_sentence_probs.append(float(seq_count) / float(initword_count))
				
				
				"""
				Con seq
				"""
				# create seq
				seq_list = []
				for word in sentence_list[i : i+n]:
					if word not in con_dict_uni:
						seq_list.append("<UNK>")
					else:
						seq_list.append(word)
				
				seq = " ".join(seq_list)
				
				# if seq is in con_dict_seq, do normal plus 1
				if seq in con_dict_seq:
					seq_count = con_dict_seq[seq][0] + 1
					initword = seq_list[0]
					initword_count = con_dict_uni[initword]
				else:
					seq_count = 1
					initword = seq_list[0]
					initword_count = con_dict_uni[initword]
				# calculate n-gram prob for each nth word and store in dict.
				con_sentence_probs.append(float(seq_count) / float(initword_count))
				
				
				"""
				Neutral seq
				"""
				# create seq
				seq_list = []
				for word in sentence_list[i : i+n]:
					if word not in neu_dict_uni:
						seq_list.append("<UNK>")
					else:
						seq_list.append(word)
				
				seq = " ".join(seq_list)
				
				# if seq is in neu_dict_seq, do normal plus 1
				if seq in neu_dict_seq:
					seq_count = neu_dict_seq[seq][0] + 1
					initword = seq_list[0]
					initword_count = neu_dict_uni[initword]
				else:
					seq_count = 1
					initword = seq_list[0]
					initword_count = neu_dict_uni[initword]
				# calculate n-gram prob for each nth word and store in dict.
				neu_sentence_probs.append(float(seq_count) / float(initword_count))
		
		
		# convert raw probabilities to log probabilities
		lib_log_probs = list(map(math.log, lib_sentence_probs))
		con_log_probs = list(map(math.log, con_sentence_probs))
		neu_log_probs = list(map(math.log, neu_sentence_probs))
		
		# summing up log probs is equivalent to multiplying raw probs
		# convert log prob to raw prob by taking its exponent 
		lib_prob = math.exp(sum(lib_log_probs))
		con_prob = math.exp(sum(con_log_probs))
		neu_prob = math.exp(sum(neu_log_probs))

# 		print "----------"
# 		print lib_prob
# 		print con_prob
# 		print neu_prob
		
		if con_prob > lib_prob and con_prob > neu_prob:
# 			print start_tag*(n-1)+sentence+end_tag*(n-1)
			correct1 += 1
		
		if con_prob > lib_prob:
			correct2 += 1
			
		if con_prob > neu_prob:
# 			print start_tag*(n-1)+sentence+end_tag*(n-1)
			correct3 += 1
		
		
		if lib_prob > con_prob and lib_prob > neu_prob:
			lib_cat += 1
		elif  con_prob > lib_prob and con_prob > neu_prob:
			con_cat += 1
		elif neu_prob > lib_prob and neu_prob > con_prob:
			neu_cat += 1
		
	print "########Conservative Test Set########"
	print "Accuracy out of lib vs. con vs. neu: ", float(correct1)/float(len(con[int(len(con)*training_limit)+1:]))
	print "Accuracy, con vs. lib: ", float(correct2)/float(len(con[int(len(con)*training_limit)+1:]))
	print "Accuracy, lib vs. neu: ", float(correct3)/float(len(con[int(len(con)*training_limit)+1:]))
	print "Out of "+str(len(con[int(len(con)*training_limit)+1:]))+" conservative articles, "
	print "Labeled Liberal: ",lib_cat
	print "Labeled Conservative: ",con_cat
	print "Labeled Neutral: ", neu_cat

	
	
	
	# Test set loop on lib
	correct1 = 0
	correct2 = 0
	correct3 = 0
	lib_cat = 0
	con_cat = 0
	neu_cat = 0
	for tree in neutral[int(len(neutral)*training_limit)+1:]:
		start_tag = "<s> "
		sentence = re.sub("[^(a-rt-zA-z\s')]", "", tree.get_words()).replace("`","").replace("(","").replace(")","").replace("	"," ")
		end_tag = "</s> "
	
# 		print start_tag*(n-1)+sentence+end_tag*(n-1)
	
		sentence_list = (start_tag*(n-1)+sentence+end_tag*(n-1)).split()
	
		lib_sentence_probs = []
		con_sentence_probs = []
		neu_sentence_probs = []
		for i in range(len(sentence_list)):
			if i < len(sentence_list)-1:
				"""
				Lib seq
				"""
				# create seq
				seq_list = []
				for word in sentence_list[i : i+n]:
					if word not in lib_dict_uni:
						seq_list.append("<UNK>")
					else:
						seq_list.append(word)
				
				seq = " ".join(seq_list)
# 				print i, i+n, seq
				
				
				# if seq is in lib_dict_seq, do normal plus 1
				if seq in lib_dict_seq:
					seq_count = lib_dict_seq[seq][0] + 1
					initword = seq_list[0]
					initword_count = lib_dict_uni[initword]
				else:
					seq_count = 1
					initword = seq_list[0]
					initword_count = lib_dict_uni[initword]
				# calculate n-gram prob for each nth word and store in dict.
				lib_sentence_probs.append(float(seq_count) / float(initword_count))
				
				"""
				Con seq
				"""
				
				# create seq
				seq_list = []
				for word in sentence_list[i : i+n]:
					if word not in con_dict_uni:
						seq_list.append("<UNK>")
					else:
						seq_list.append(word)
				
				seq = " ".join(seq_list)
				
				# if seq is in con_dict_seq, do normal plus 1
				if seq in con_dict_seq:
					seq_count = con_dict_seq[seq][0] + 1
					initword = seq_list[0]
					initword_count = con_dict_uni[initword]
				else:
					seq_count = 1
					initword = seq_list[0]
					initword_count = con_dict_uni[initword]
				# calculate n-gram prob for each nth word and store in dict.
				con_sentence_probs.append(float(seq_count) / float(initword_count))
				
				"""
				Neutral seq
				"""
				
				# create seq
				seq_list = []
				for word in sentence_list[i : i+n]:
					if word not in neu_dict_uni:
						seq_list.append("<UNK>")
					else:
						seq_list.append(word)
				
				seq = " ".join(seq_list)
				
				# if seq is in neu_dict_seq, do normal plus 1
				if seq in neu_dict_seq:
					seq_count = neu_dict_seq[seq][0] + 1
					initword = seq_list[0]
					initword_count = neu_dict_uni[initword]
				else:
					seq_count = 1
					initword = seq_list[0]
					initword_count = neu_dict_uni[initword]
				# calculate n-gram prob for each nth word and store in dict.
				neu_sentence_probs.append(float(seq_count) / float(initword_count))
		
		
		# convert raw probabilities to log probabilities
		lib_log_probs = list(map(math.log, lib_sentence_probs))
		con_log_probs = list(map(math.log, con_sentence_probs))
		neu_log_probs = list(map(math.log, neu_sentence_probs))
		
		# summing up log probs is equivalent to multiplying raw probs
		# convert log prob to raw prob by taking its exponent 
		lib_prob = math.exp(sum(lib_log_probs))
		con_prob = math.exp(sum(con_log_probs))
		neu_prob = math.exp(sum(neu_log_probs))

# 		print "----------"
# 		print lib_prob
# 		print con_prob
# 		print neu_prob
		
		if neu_prob > lib_prob and neu_prob > con_prob:
# 			print start_tag*(n-1)+sentence+end_tag*(n-1)
			correct1 += 1
		
		if neu_prob > lib_prob:
			correct2 += 1
			
		if neu_prob > con_prob:
# 			print start_tag*(n-1)+sentence+end_tag*(n-1)
			correct3 += 1
		
		if lib_prob > con_prob and lib_prob > neu_prob:
			lib_cat += 1
		elif  con_prob > lib_prob and con_prob > neu_prob:
			con_cat += 1
		elif neu_prob > lib_prob and neu_prob > con_prob:
			neu_cat += 1
		
	print "########Neutral Test Set########"
	print "Accuracy out of lib vs. con vs. neu: ", float(correct1)/float(len(neutral[int(len(neutral)*training_limit)+1:]))
	print "Accuracy, neu vs. lib: ", float(correct2)/float(len(neutral[int(len(neutral)*training_limit)+1:]))
	print "Accuracy, neu vs. con: ", float(correct3)/float(len(neutral[int(len(neutral)*training_limit)+1:]))
	print "Out of "+str(len(neutral[int(len(neutral)*training_limit)+1:]))+" neutral articles, "
	print "Labeled Liberal: ",lib_cat
	print "Labeled Conservative: ",con_cat
	print "Labeled Neutral: ", neu_cat
				
				
	
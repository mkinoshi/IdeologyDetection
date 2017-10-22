import cPickle
import re
import math
import json
from scipy import stats
import random
# new file!!
if __name__ == '__main__':
  with open('data.json') as data_file:    
    data = json.load(data_file)

  print data.keys()
  """
  Adjustable variables
  """
  n = 2 # define n-gram here
  training_limit = 0.6 # proportion of training data
  random.seed(100) #initialize random number

  lib_seq_total = 0
  lib_dict_seq = {}

  con_seq_total = 0
  con_dict_seq = {}

  lib_top100 = [0]*100
  con_top100 = [0]*100

  #dividing data into three categories
  lib = data['liberal']
  con = data['conservative']
  neutral = data['neutral']
  print lib[0]

  #divide into traning data and test data
  training_ind_lib = random.sample(range(0, len(lib)), len(lib)*0.6)
  training_ind_con = random.sample(range(0, len(con)), len(con)*0.6)
  training_lib = []
  training_con = []
  for i in training_ind_lib:
    training_lib.append(lib[training_ind_lib[i]])

  for i in training_ind_con:
    training_con.append(con[training_ind_con[i]])
  """
  Count bi-word frequency for liberal 
  """
  for tree in training_lib:
  # 	for tree in lib[0:int(len(lib)*training_limit)]:
    # pre-process sentence, add <s> and </s> to beginning and end of sentence, take out non-alphabets using regex
    start_tag = "<s> "
    sentence = re.sub("[^(a-rt-zA-z\s')]", "", tree).replace("`","").replace("(","").replace(")","").replace("	"," ")
    end_tag = "</s> "
    
    # print start_tag*(n-1)+sentence+end_tag*(n-1)
      
    # sentence_list = (start_tag*(n-1)+sentence+end_tag*(n-1)).split()
    sentence_list = sentence.split()
    

    # count frequency of bi-word sequence and store in lib_dict_seq
    for i in range(len(sentence_list)):
      if i < len(sentence_list)-1:
        # create seq
        seq_list = []
        for word in sentence_list[i : i+n]:
          # just keep every word									# BOOM
          seq_list.append(word)
        
        
        print seq_list
        seq = " ".join(seq_list)
        print i, i+n, seq
      
        # add to lib_dict_seq
        if seq in lib_dict_seq:
          lib_dict_seq[seq][0] += 1.0
        else:
          lib_dict_seq[seq] = [1.0, seq_list]
        
        # increment total seq occurence count
        lib_seq_total += 1.0
      
    
  # 		print lib_dict_seq
  # 		print lib_seq_total
    


  """
  Count bi-word frequency for conservative
  """
  for tree in training_con:
  # 	for tree in con[0:int(len(con)*training_limit)]:
    # pre-process sentence, add <s> and </s> to beginning and end of sentence, take out non-alphabets using regex
    start_tag = "<s> "
    sentence = re.sub("[^(a-rt-zA-z\s')]", "", tree).replace("`","").replace("(","").replace(")","").replace("	"," ")
    end_tag = "</s> "
    
    # print start_tag*(n-1)+sentence+end_tag*(n-1)
      
    # sentence_list = (start_tag*(n-1)+sentence+end_tag*(n-1)).split()
    sentence_list = sentence.split()
    
    
    # count frequency of bi-word sequence and store in con_dict_seq
    for i in range(len(sentence_list)):
      if i < len(sentence_list)-1:
        # create seq
        seq_list = []
        for word in sentence_list[i : i+n]:
          # just keep every word									# BOOM
          seq_list.append(word)
        
        
  # 				print seq_list
        seq = " ".join(seq_list)
        print i, i+n, seq
      
        # add to con_dict_seq
        if seq in con_dict_seq:
          con_dict_seq[seq][0] += 1.0
        else:
          con_dict_seq[seq] = [1.0, seq_list]
        
        # increment total seq occurence count
        con_seq_total += 1.0
          
    
    
    
  """
  Calculate chi-square test statistic for each seq in Liberal
  """
  lib_xsqr_list = []
  lib_seq_list = []
  for seq in lib_dict_seq:
    # handle cases where liberal seq is not in the conservative sentences
    if seq not in con_dict_seq: 
      fplr = 0.0
      f_plr = con_seq_total
    else:
      fplr = con_dict_seq[seq][0]
      f_plr = con_seq_total - con_dict_seq[seq][0]
    
    fpld = lib_dict_seq[seq][0]
    f_pld = lib_seq_total - lib_dict_seq[seq][0]
    
  # 		print lib_seq_total
  # 		print con_seq_total
  # 		print seq
  # 		print fplr, f_plr, fpld, f_pld
    
    # chi-square formula
    x2 = (fplr*f_pld - fpld*f_plr)**2/((fplr+fpld)*(fplr+f_plr)*(fpld+f_pld)*(f_plr+f_pld))
    
    
    # keep record of xsqr values and seq, will always be at same index 
    lib_xsqr_list.append(x2)
    lib_seq_list.append(seq)
    
    lib_dict_seq[seq].append(x2)


  """
  Calculate chi-square test statistic for each seq in conservative
  """
  con_xsqr_list = []
  con_seq_list = []
  for seq in con_dict_seq:
    # handle cases where liberal seq is not in the conservative sentences
    if seq not in lib_dict_seq:
      fpld = 0
      f_pld = lib_seq_total
    else:
      fpld = lib_dict_seq[seq][0]
      f_pld = lib_seq_total - lib_dict_seq[seq][0]
    
    fplr = con_dict_seq[seq][0]
    f_plr = con_seq_total - con_dict_seq[seq][0]
    
    x2 = (fplr*f_pld - fpld*f_plr)**2/((fplr+fpld)*(fplr+f_plr)*(fpld+f_pld)*(f_plr+f_pld))
    
    # keep record of xsqr values and seq, will always be at same index
    con_xsqr_list.append(x2)
    con_seq_list.append(seq)
    
    con_dict_seq[seq].append(x2)

  """
  Get a phrase whose p-value is smaller than 0.05
  """
  lib_p_word = []
  for i in range(len(lib_xsqr_list)):
    print stats.chi2.pdf(lib_xsqr_list[i] , 1), lib_seq_list[i]
  # """
  # Get top 100 xsqr value bi-word sequences for liberal
  # """
  # lib_ret = []
  # for i in range(100):
  #   index = lib_xsqr_list.index(max(lib_xsqr_list))
  #   lib_ret.append(lib_seq_list[index])
    
  #   del lib_seq_list[index]
  #   del lib_xsqr_list[index]

  # """
  # Get top 100 xsqr value bi-word sequences for conservative
  # """	
  # con_ret = []
  # for i in range(100):
  #   index = con_xsqr_list.index(max(con_xsqr_list))
  #   con_ret.append(con_seq_list[index])
    
  #   del con_seq_list[index]
  #   del con_xsqr_list[index]

  # print lib_dict_seq
  # print con_dict_seq

  # print lib_ret
  # print con_ret

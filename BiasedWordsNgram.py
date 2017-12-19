import cPickle
import re
import math
import json
from scipy import stats
import random
from nltk.corpus import stopwords

# new file!!
def extract_biased_words(ind):
  with open('data.json') as data_file:    
    data = json.load(data_file)
  """
  Adjustable variables
  """
  n = 2 # define n-gram here
  training_limit = 0.6 # proportion of training data
  random.seed(100) #initialize random number

  lib_seq_total_one = 0
  lib_seq_total_two = 0
  lib_seq_total_three = 0
  lib_dict_seq_one = {}
  lib_dict_seq_two = {}
  lib_dict_seq_three = {}

  con_seq_total_one = 0
  con_seq_total_two = 0
  con_seq_total_three = 0
  con_dict_seq_one = {}
  con_dict_seq_two = {}
  con_dict_seq_three = {}

  lib_top100 = [0]*100
  con_top100 = [0]*100

  #dividing data into three categories
  lib = data['liberal']
  con = data['conservative']
  neutral = data['neutral']

  #divide into traning data and test data
  training_ind_lib = random.sample(range(0, len(lib)-1), int(len(lib)*0.6))
  training_ind_con = random.sample(range(0, len(con)-1), int(len(con)*0.6))
  training_lib = []
  training_con = []
  for i in training_ind_lib:
    training_lib.append(lib[i])

  for i in training_ind_con:
    training_con.append(con[i])
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
    

    # count frequency of bi-word sequence and store in lib_dict_seq_two
    for i in range(len(sentence_list)):
      if i < len(sentence_list)-1:
        # create seq
        seq_list_one = []
        seq_list_two = []
        seq_list_three = []
        for word in sentence_list[i : i+1]:
          # just keep every word									# BOOM
          seq_list_one.append(word.lower())

        for word in sentence_list[i : i+2]:
          # just keep every word									# BOOM
          seq_list_two.append(word.lower())
        
        for word in sentence_list[i : i+3]:
          seq_list_three.append(word.lower())
        
        seq_one = seq_list_one[0]
        seq_two = " ".join(seq_list_two)
        seq_three = " ".join(seq_list_three)

        # add to lib_dict_seq_one
        if seq_one in lib_dict_seq_one:
          lib_dict_seq_one[seq_one][0] += 1.0
        else:
          lib_dict_seq_one[seq_one] = [1.0, seq_list_one]

        # add to lib_dict_seq_two
        if seq_two in lib_dict_seq_two:
          lib_dict_seq_two[seq_two][0] += 1.0
        else:
          lib_dict_seq_two[seq_two] = [1.0, seq_list_two]

        # add to lib_dict_seq_three
        if seq_three in lib_dict_seq_three:
          lib_dict_seq_three[seq_three][0] += 1.0
        else:
          lib_dict_seq_three[seq_three] = [1.0, seq_list_three]
        
        # increment total seq occurence count
        lib_seq_total_one += 1.0
        lib_seq_total_two += 1.0
        lib_seq_total_three += 1.0
      
    
  # 		print lib_dict_seq_two
  # 		print lib_seq_total_two
    


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
    
    
    # count frequency of bi-word sequence and store in con_dict_seq_two
    for i in range(len(sentence_list)):
      if i < len(sentence_list)-1:
        # create seq
        seq_list_one = []
        seq_list_two = []
        seq_list_three = []
        for word in sentence_list[i : i+1]:
          # just keep every word									# BOOM
          seq_list_one.append(word.lower())

        for word in sentence_list[i : i+2]:
          # just keep every word									# BOOM
          seq_list_two.append(word.lower())
        
        for word in sentence_list[i : i+3]:
          seq_list_three.append(word.lower())
        
        
        seq_one = seq_list_one[0]
        seq_two = " ".join(seq_list_two)
        seq_three = " ".join(seq_list_three)

        # add to con_dict_seq_two
        if seq_one in con_dict_seq_one:
          con_dict_seq_one[seq_one][0] += 1.0
        else:
          con_dict_seq_one[seq_one] = [1.0, seq_list_one]

        # add to con_dict_seq_two
        if seq_two in con_dict_seq_two:
          con_dict_seq_two[seq_two][0] += 1.0
        else:
          con_dict_seq_two[seq_two] = [1.0, seq_list_two]

        # add to con_dict_seq_three
        if seq_three in con_dict_seq_three:
          con_dict_seq_three[seq_three][0] += 1.0
        else:
          con_dict_seq_three[seq_three] = [1.0, seq_list_three]
        
        # increment total seq occurence count
        con_seq_total_one += 1.0
        con_seq_total_two += 1.0
        con_seq_total_three += 1.0

  if ind == 1:
    """
    Calculate chi-square test statistic for each bi-gram word in Liberal
    """
    lib_xsqr_list_one = []
    lib_seq_list_one = []
    for seq in lib_dict_seq_one:
      # handle cases where liberal seq is not in the conservative sentences
      if seq not in con_dict_seq_one: 
        fplr = 0.0
        f_plr = con_seq_total_one
      else:
        fplr = con_dict_seq_one[seq][0]
        f_plr = con_seq_total_one - con_dict_seq_one[seq][0]
      
      fpld = lib_dict_seq_one[seq][0]
      f_pld = lib_seq_total_one - lib_dict_seq_one[seq][0]
      
    # 		print lib_seq_total_one
    # 		print con_seq_total_one
    # 		print seq
    # 		print fplr, f_plr, fpld, f_pld
      
      # chi-square formula
      x2 = (fplr*f_pld - fpld*f_plr)**2/((fplr+fpld)*(fplr+f_plr)*(fpld+f_pld)*(f_plr+f_pld))
      
      
      # keep record of xsqr values and seq, will always be at same index 
      lib_xsqr_list_one.append(x2)
      lib_seq_list_one.append(seq)
      
      lib_dict_seq_one[seq].append(x2) 
  elif ind == 2:
    """
    Calculate chi-square test statistic for each bi-gram word in Liberal
    """
    lib_xsqr_list_two = []
    lib_seq_list_two = []
    for seq in lib_dict_seq_two:
      # handle cases where liberal seq is not in the conservative sentences
      if seq not in con_dict_seq_two: 
        fplr = 0.0
        f_plr = con_seq_total_two
      else:
        fplr = con_dict_seq_two[seq][0]
        f_plr = con_seq_total_two - con_dict_seq_two[seq][0]
      
      fpld = lib_dict_seq_two[seq][0]
      f_pld = lib_seq_total_two - lib_dict_seq_two[seq][0]
      
    # 		print lib_seq_total_two
    # 		print con_seq_total_two
    # 		print seq
    # 		print fplr, f_plr, fpld, f_pld
      
      # chi-square formula
      x2 = (fplr*f_pld - fpld*f_plr)**2/((fplr+fpld)*(fplr+f_plr)*(fpld+f_pld)*(f_plr+f_pld))
      
      
      # keep record of xsqr values and seq, will always be at same index 
      lib_xsqr_list_two.append(x2)
      lib_seq_list_two.append(seq)
      
      lib_dict_seq_two[seq].append(x2)
  else:
    """
    Calculate chi-square test statistic for each tri-gram word in Liberal
    """
    lib_xsqr_list_three = []
    lib_seq_list_three = []
    for seq in lib_dict_seq_three:
      # handle cases where liberal seq is not in the conservative sentences
      if seq not in con_dict_seq_three: 
        fplr = 0.0
        f_plr = con_seq_total_three
      else:
        fplr = con_dict_seq_three[seq][0]
        f_plr = con_seq_total_three - con_dict_seq_three[seq][0]
      
      fpld = lib_dict_seq_three[seq][0]
      f_pld = lib_seq_total_three - lib_dict_seq_three[seq][0]
      
    # 		print lib_seq_total_three
    # 		print con_seq_total_three
    # 		print seq
    # 		print fplr, f_plr, fpld, f_pld
      
      # chi-square formula
      x2 = (fplr*f_pld - fpld*f_plr)**2/((fplr+fpld)*(fplr+f_plr)*(fpld+f_pld)*(f_plr+f_pld))
      
      
      # keep record of xsqr values and seq, will always be at same index 
      lib_xsqr_list_three.append(x2)
      lib_seq_list_three.append(seq)
      
      lib_dict_seq_three[seq].append(x2)

  if ind == 1:
    """
    Calculate chi-square test statistic for each uni-gram word in conservative 
    """
    con_xsqr_list_one = []
    con_seq_list_one = []
    for seq in con_dict_seq_one:
      # handle cases where liberal seq is not in the conservative sentences
      if seq not in lib_dict_seq_one:
        fpld = 0
        f_pld = lib_seq_total_one
      else:
        fpld = lib_dict_seq_one[seq][0]
        f_pld = lib_seq_total_one - lib_dict_seq_one[seq][0]
      
      fplr = con_dict_seq_one[seq][0]
      f_plr = con_seq_total_one - con_dict_seq_one[seq][0]
      
      x2 = (fplr*f_pld - fpld*f_plr)**2/((fplr+fpld)*(fplr+f_plr)*(fpld+f_pld)*(f_plr+f_pld))
      
      # keep record of xsqr values and seq, will always be at same index
      con_xsqr_list_one.append(x2)
      con_seq_list_one.append(seq)
      
      con_dict_seq_one[seq].append(x2)
  elif ind == 2:
    """
    Calculate chi-square test statistic for each bi-gram word in conservative 
    """
    con_xsqr_list_two = []
    con_seq_list_two = []
    for seq in con_dict_seq_two:
      # handle cases where liberal seq is not in the conservative sentences
      if seq not in lib_dict_seq_two:
        fpld = 0
        f_pld = lib_seq_total_two
      else:
        fpld = lib_dict_seq_two[seq][0]
        f_pld = lib_seq_total_two - lib_dict_seq_two[seq][0]
      
      fplr = con_dict_seq_two[seq][0]
      f_plr = con_seq_total_two - con_dict_seq_two[seq][0]
      
      x2 = (fplr*f_pld - fpld*f_plr)**2/((fplr+fpld)*(fplr+f_plr)*(fpld+f_pld)*(f_plr+f_pld))
      
      # keep record of xsqr values and seq, will always be at same index
      con_xsqr_list_two.append(x2)
      con_seq_list_two.append(seq)
      
      con_dict_seq_two[seq].append(x2)
  else:
    """
    Calculate chi-square test statistic for each tri-gram word in conservative 
    """
    con_xsqr_list_three = []
    con_seq_list_three = []
    for seq in con_dict_seq_three:
      # handle cases where liberal seq is not in the conservative sentences
      if seq not in lib_dict_seq_three:
        fpld = 0
        f_pld = lib_seq_total_three
      else:
        fpld = lib_dict_seq_three[seq][0]
        f_pld = lib_seq_total_three - lib_dict_seq_three[seq][0]
      
      fplr = con_dict_seq_three[seq][0]
      f_plr = con_seq_total_three - con_dict_seq_three[seq][0]
      
      x2 = (fplr*f_pld - fpld*f_plr)**2/((fplr+fpld)*(fplr+f_plr)*(fpld+f_pld)*(f_plr+f_pld))
      
      # keep record of xsqr values and seq, will always be at same index
      con_xsqr_list_three.append(x2)
      con_seq_list_three.append(seq)
      
      con_dict_seq_three[seq].append(x2)

  # """
  # Get a phrase whose p-value is smaller than 0.05
  # """
  # lib_p_word = []
  # for i in range(len(lib_xsqr_list_two)):
  #   print stats.chi2.pdf(lib_xsqr_list_two[i] , 1), lib_seq_list_two[i]
  if ind == 1:
    """
    Get top all xsqr value uni-word sequences for liberal
    """
    lib_ret_one = []
    for i in range(len(lib_seq_list_one)):
      index = lib_xsqr_list_one.index(max(lib_xsqr_list_one))
      lib_ret_one.append(lib_seq_list_one[index])
      
      del lib_seq_list_one[index]
      del lib_xsqr_list_one[index]
  elif ind == 2:
    """
    Get top all xsqr value bi-word sequences for liberal
    """
    lib_ret_two = []
    for i in range(len(lib_seq_list_two)):
      index = lib_xsqr_list_two.index(max(lib_xsqr_list_two))
      lib_ret_two.append(lib_seq_list_two[index])
      
      del lib_seq_list_two[index]
      del lib_xsqr_list_two[index]
  else:
    """
    Get top all xsqr value tri-word sequences for liberal
    """
    lib_ret_three = []
    for i in range(len(lib_seq_list_three)):
      index = lib_xsqr_list_three.index(max(lib_xsqr_list_three))
      lib_ret_three.append(lib_seq_list_three[index])
      
      del lib_seq_list_three[index]
      del lib_xsqr_list_three[index]

  if ind == 1:
    """
    Get top all xsqr value bi-word sequences for conservative
    """	
    con_ret_one = []
    for i in range(len(con_seq_list_one)):
      index = con_xsqr_list_one.index(max(con_xsqr_list_one))
      con_ret_one.append(con_seq_list_one[index])
      
      del con_seq_list_one[index]
      del con_xsqr_list_one[index]
  elif ind == 2:
    """
    Get top all xsqr value bi-word sequences for conservative
    """	
    con_ret_two = []
    for i in range(len(con_seq_list_two)):
      index = con_xsqr_list_two.index(max(con_xsqr_list_two))
      con_ret_two.append(con_seq_list_two[index])
      
      del con_seq_list_two[index]
      del con_xsqr_list_two[index]
  else:
    """
    Get top all xsqr value tri-word sequences for conservative
    """	
    con_ret_three = []
    for i in range(len(con_seq_list_three)):
      index = con_xsqr_list_three.index(max(con_xsqr_list_three))
      con_ret_three.append(con_seq_list_three[index])
      
      del con_seq_list_three[index]
      del con_xsqr_list_three[index]

  s=set(stopwords.words('english'))
  if ind == 1:
    """
    Get top 100 biased uni-words for liberal
    """
    count_lib_one = 0
    count_lib_list_one = 0
    lib_ret_100_one = []
    # uncomment to remove words which are not included in biased words for conserv
    while count_lib_one < 100 and count_lib_list_one < len(lib_ret_one):
      #if lib_ret_one[count_lib_list_one] not in con_ret_one:
      if lib_ret_one[count_lib_list_one] not in s:
        lib_ret_100_one.append(lib_ret_one[count_lib_list_one])
        count_lib_one += 1
      count_lib_list_one += 1
  elif ind == 2:
    """
    Get top 100 biased bi-words for liberal
    """
    count_lib_two = 0
    count_lib_list_two = 0
    lib_ret_100_two = []
    # uncomment to remove words which are not included in biased words for conserv
    while count_lib_two < 100 and count_lib_list_two < len(lib_ret_two):
      #if lib_ret_two[count_lib_list_two] not in con_ret_two:
      if '' not in lib_ret_two[count_lib_two] and "" not in lib_ret_two[count_lib_two]:
        lib_ret_100_two.append(lib_ret_two[count_lib_list_two])
        count_lib_two += 1
      count_lib_list_two += 1
      lib_ret_100_two = lib_ret_two[0: 101]
  else:
    """
    Get top 100 biased tri-words for liberal
    """
    count_lib_three = 0
    count_lib_list_three = 0
    lib_ret_100_three = []
    # uncomment to remove words which are not included in biased words for conserv
    while count_lib_three < 100 and count_lib_list_three < len(lib_ret_three):
      # if lib_ret_three[count_lib_list_three] not in con_ret_three:
      if '' not in lib_ret_three[count_lib_three] and "" not in lib_ret_three[count_lib_three]:
        lib_ret_100_three.append(lib_ret_three[count_lib_list_three])
        count_lib_three += 1
      count_lib_list_three += 1
    lib_ret_100_three = lib_ret_three[0:101]
  
  if ind == 1:
    """
    Get top 100 biased uni-words for conservative
    """
    count_con_one = 0
    count_con_list_one = 0
    con_ret_100_one = []
    # uncomment to remove words which are not included in biased words for liberal
    while count_con_one < 100 and count_con_list_one < len(con_ret_one):
      # if con_ret_one[count_con_list_one] not in lib_ret_one:
      if con_ret_one[count_con_list_one] not in s:
        con_ret_100_one.append(con_ret_one[count_con_list_one])
        count_con_one += 1
      count_con_list_one += 1
  elif ind == 2:
    """
    Get top 100 biased bi-words for conservative
    """
    count_con_two = 0
    count_con_list_two = 0
    con_ret_100_two = []
    # uncomment to remove words which are not included in biased words for liberal
    while count_con_two < 100 and count_con_list_two < len(con_ret_two):
      # if con_ret_two[count_con_list_two] not in lib_ret_two:
      if '' not in con_ret_two[count_con_two] and "" not in con_ret_two[count_con_two]:
        con_ret_100_two.append(con_ret_two[count_con_list_two])
        count_con_two += 1
      count_con_list_two += 1
    con_ret_100_two = con_ret_two[0: 101]
  else:
    """
    Get top 100 biased tri-words for conservative
    """
    count_con_three = 0
    count_con_list_three = 0
    con_ret_100_three = []
    # uncomment to remove words which are not included in biased words for liberal
    while count_con_three < 100 and count_con_list_three < len(con_ret_three):
      # if con_ret_three[count_con_list_three] not in lib_ret_three:
      if '' not in con_ret_three[count_con_three] and "" not in con_ret_three[count_con_three]:
        con_ret_100_three.append(con_ret_three[count_con_list_three])
        count_con_three += 1
      count_con_list_three += 1
    con_ret_100_three = con_ret_three[0: 101]

  if ind == 1:
    print lib_ret_100_one[0:10]
    print con_ret_100_one[0:10]
    return lib_ret_100_one + con_ret_100_one
  elif ind == 2:
    print lib_ret_100_two[0:10]
    print con_ret_100_two[0:10]
    return lib_ret_100_two + con_ret_100_two
  else:
    print lib_ret_100_three[0:10]
    print con_ret_100_three[0:10]
    return lib_ret_100_three + con_ret_100_three

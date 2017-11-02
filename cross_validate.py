# Tatsuya Yokota
# Cross Validation

import cPickle
import re

from BoW_PCA import main


def cross_validate(n=5):
    print "Pickling data"
    [lib, con, neutral] = cPickle.load(open('ibcData.pkl', 'rb'))

    lib_docs = []
    con_docs = []
    # total: 1700
    # 5 sets of 340
    # divide the data set into n sets for each category
    print "pre-processing data"
    for tree in lib:
        # pre-process doc. 
	sentence = re.sub("[^(a-rt-zA-z\s)]", "", tree.get_words()).replace("`","").replace("(","").replace(")","").replace("	"," ")
	lib_docs.append(sentence)
        
    for tree in con:
        # pre-process doc. 
	sentence = re.sub("[^(a-rt-zA-z\s)]", "", tree.get_words()).replace("`","").replace("(","").replace(")","").replace("	"," ")
	con_docs.append(sentence)

    print "balance and subdividing the data"
    # balance the data set size
    size = min([len(lib_docs), len(con_docs)])
    lib_docs = lib_docs[:size]
    con_docs = con_docs[:size]

    print len(lib_docs)
    print len(con_docs)
    
    # subdivide the data set 
    lib_subsets = []
    con_subsets = []
    subset_size = size/n
    print "subset size", subset_size
    
    for i in range(n):
        lib_subsets.append(lib_docs[i*subset_size:(i+1)*subset_size])
        con_subsets.append(con_docs[i*subset_size:(i+1)*subset_size])
        print subset_size*i, subset_size*(i+1)
    
    print "cross-validating model"
    lib_accuracies = []
    con_accuracies = []
    for j in range(n):

        lib_train_temp = lib_subsets[:j] + lib_subsets[(j + 1):] # still list of lists, need to join inner lists
        con_train_temp = con_subsets[:j] + con_subsets[(j + 1):]
        lib_train = [inner for outer in lib_train_temp for inner in outer]
        con_train = [inner for outer in con_train_temp for inner in outer]

        lib_test = lib_subsets[j]
        con_test = con_subsets[j]

    
        
        lib_accuracy, con_accuracy = main(lib_train, con_train, lib_test, con_test)
        lib_accuracies.append(lib_accuracy)
        con_accuracies.append(con_accuracy)

        print "For the %dth iteration:" % (j+1)
        print "Liberal accuracy: %.2f" % lib_accuracy
        print "Conservative accuracy: %.2f\n" % con_accuracy
        
    lib_avg_accuracy = sum(lib_accuracies)/n
    con_avg_accuracy = sum(con_accuracies)/n
    total_avg_accuracy = (lib_avg_accuracy+con_avg_accuracy)/2

    
    print "Average Liberal Accuracy: %.2f" % lib_avg_accuracy
    print "Average Conservative Accuracy: %.2f" % con_avg_accuracy
    print "Average Total Accuracy: %.2f" % total_avg_accuracy
    
    return lib_avg_accuracy, con_avg_accuracy, total_avg_accuracy


if __name__ == "__main__":
    cross_validate(n=5)

import cPickle
import pickle

if __name__ == '__main__':
  [lib, con, neutral] = cPickle.load(open('ibcData.pkl', 'rb'))
  """
	Adjustable variables
	"""
  n = 2 # define n-gram here
  training_limit = 0.6 # proportion of training data

  for tree in lib[0:int(len(lib)*training_limit)]:
    sentence = re.sub("[^(a-rt-zA-z\s')]", "", tree.get_words()).replace("`","").replace("(","").replace(")","").replace("	"," ")
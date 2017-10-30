

import numpy as np
import scipy.stats
import scipy.cluster.vq as vq
import math
import random

# takes in a matrix to perform PCA on and the minimum percentage of variance 
# 	eigenvectors should account for in the data
# returns eigenvector matrix and eigenvalues
def pca(matrix):

	# assign to m the mean values of the columns of matrix
	avg = matrix.mean(axis=0)

  	# assign to D the difference matrix A - m
	D = matrix - avg


	# assign to U, S, V the result of running np.svd on D, with full_matrices=False
	U, S, V = np.linalg.svd(D, full_matrices=True)
	
# 		print U
# 		print S
# 		print V

	# the eigenvalues of cov(A) are the squares of the singular values (S matrix)
	# 	divided by the degrees of freedom (N-1). The values are sorted.
	eVals = np.square(S)/(matrix.shape[0] - 1)
# 		print eigVals
	
	# project the data onto the eigenvectors. Treat V as a transformation 
	# 	matrix and right-multiply it by D transpose. The eigenvectors of matrixA 
	# 	are the rows of V. The eigenvectors match the order of the eigenvalues.
	eVecs = V
# 	print V
# 		print D.T
# 		print eigVecs
	
	# return the projected data
#	projData = D * eVecs.T
	
	projData = np.dot(D, eVecs.T)

	print eVecs.shape
	
	
	
	# take principle components

# 	print totalEval

	
	
	
	return (projData, eVecs, eVals)


# if __name__ == '__main__':



# no need to normalize the matrix because everything is in the same units in this case 
# 
# 
# 
# 
# 



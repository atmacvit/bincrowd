import csv
import numpy as np
import json
import operator
from bayesian_blocks import bayesian_blocks

def rankify(A): 
    '''
    Given an array A returns rank array correspondint to the array A

    Tied ranks given 1/2 values.
    '''
  
    # Rank Vector 
    R = [0 for x in range(len(A))] 
  
    # Sweep through all elements 
    # in A for each element count 
    # the number of less than and  
    # equal elements separately 
    # in r and s. 
    for i in range(len(A)): 
        (r, s) = (1, 1) 
        for j in range(len(A)): 
            if j != i and A[j] < A[i]: 
                r += 1
            if j != i and A[j] == A[i]: 
                s += 1       
         
        # Use formula to obtain rank 
        R[i] = r + (s - 1) / 2
  
    # Return Rank Vector 
    return R 

def best_2(data,fitness_funct,test_ratio_arr,gammas):
    '''
    Parameters: 
    -----------
            => data = array of counts x =[0.0, 0.0, 0.0, 1.0, 2.0, 5.0, ..., 20033.0]
            => fitness_funct = "multinomial" or "poisson" .
            => test_ratio_arr = list of test ratios
            => gammas = Gammas used for training
    
    Function:
    ----------
    All the mean/standard_dev corresponding to all of the gammas are saved in json files after train.py is run at location select best.
    Their filename is in the following format xxx_mu_sim_yyy.json xxx-- either mln (multinomial) or poi( poisson),
    yyy -- (number of test samples for nwpu, 0.1,0.2,0.25 correspond to 360,721,902)
    Based on the mean/Standard_dev value we rank the gamma values for each of the test set size (0.1,0.2,0.25)
    and sum the ranks. Best one overall is the one with the least rank across the test set sizes (0.1,0.2,0.25).

    Output:
    -------
    prints the top 2 gamma value for the given fitness_funct and its corresonding bins.
    '''
    jsons={}
    for i in test_ratio_arr:
        ranks=[]
        new_dict={}
        for j in gammas:

            # if fitness_funct=="multinomial":
            #     path ="./select_best/mln_mu_sig_"+str(i)+".json"
            # if fitness_funct=="poisson":
            #     path ="./select_best/poi_mu_sig_"+str(i)+".json"
            path = i
            print("path",i)
            with open(path, 'r') as fp:
                testt = json.load(fp)

            # assigning ranks for the test array values
            ranks=rankify(list(testt.values()))

            for ii in range(len(list(testt.keys()))):
                new_dict[list(testt.keys())[ii]]=ranks[ii]
            # print(new_dict)
            # culumative of ranks over the sample test sizes
            if j in jsons:
                jsons[j]+=new_dict[str(j)]
            else:
                jsons[j]=new_dict[str(j)]

    # print(jsons)
    #mu/sigma = low == lower rank value, therfore we take the top 2 one with highest rank value to get the highest mu/sig

    sorted_ = dict(sorted(jsons.items(),reverse=True,key=lambda item: item[1]))
    print("Top Two Gamma for "+str(fitness_funct)) #least rank (top one is taken)
    # print(sorted_)
    print(list(sorted_.keys())[0:2])
    top_2 = list(sorted_.keys())[0:2]
    # bins for entire data based on the gamma values 
    print("Best Bins for the corresponding values of prior are ")
    for i in top_2:
        print(list(bayesian_blocks(data,fitness=fitness_funct,gamma=i)))



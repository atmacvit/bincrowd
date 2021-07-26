import numpy as np
from load_data import load_data,make_train_test,load_data_patch
from multinomial import multinomial_bay_block
from poisson import poisson_bay_block
from bayesian_blocks import bayesian_blocks
import argparse
import os
import glob
import random
from select_best import best_2
random.seed(999)

def main(path,fitness_funct,gammas,k,test_ratio,iter):
    '''
    Parameters:
    -----------
            => path : datapath of counts.
            => fitness function type: 'poisson' or 'multinomial'.
            => gammas : list of gamma values to iterate over.
            => k = value of factor in prior function (1-gamma)/(1-gamma**(N//2**k)) {2,4,8}
            => test_ratio : Sample size ratio kept aside for likelihood estimation
            => iter : Number of times the likelihood should be calculated (to check variance and mean likelihood).

    Function:
    ----------
    Takes the array of counts and divides into train and test arrays.
    Performs parameter estimation on train and negetive log likelihood on test.
    Repeates the experiment for a number of iterations and a number of gamma values.

    Output: 
    -------
    returns likelihoods along with gammas corresponding. (used to calculate best gamma)
    '''

    
    #uncomment below line for full image data
    t = load_data(path=path)               # t= [    0.     0.     0. ... 13843. 15426. 20033.]
    tr,tes = make_train_test(t,test_ratio=test_ratio,iter=iter)
    if fitness_funct == 'multinomial':
        likeli = multinomial_bay_block(tr,tes,k,gammas=gammas,iter=iter)
    elif fitness_funct =='poisson':
        likeli = poisson_bay_block(tr,tes,k,gammas=gammas,iter=iter)


    return likeli


# clearing the files in the folders
files = glob.glob('./test_jsons/*')
for f in files:
    os.remove(f)
files = glob.glob('./train_jsons/*')
for f in files:
    os.remove(f)
files = glob.glob('./select_best/*')
for f in files:
    os.remove(f)


# Initialize parser
parser = argparse.ArgumentParser()
# Adding optional argument
parser.add_argument("-d", "--dataset", help = "Give dataset path in txt",type=str,default="./dataset_txt/Train_nwpu.txt")
parser.add_argument("-f", "--fitness_function", help = "Select fitness function",type=str,default="multinomial")

# Read arguments from command line
args = parser.parse_args()

print("You have chosen",args.dataset)
print("Fitness function is chosen as",args.fitness_function)

test_ratio_array =[0.1,0.2,0.25]
fitness_funct=args.fitness_function
for i in test_ratio_array:
    print("ran")
    print(main(path=[args.dataset],fitness_funct=fitness_funct,
        gammas=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9],k=2,
        test_ratio=i,iter=10))
    print("end")
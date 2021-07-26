from load_data import load_data,load_data_patch
from select_best import best_2
import os
import glob
import argparse


parser = argparse.ArgumentParser()
# Adding optional argument
parser.add_argument("-d", "--dataset", help = "Give dataset path in txt",type=str,default="./dataset_txt/Train_nwpu.txt")
parser.add_argument("-f", "--fitness_function", help = "Select fitness function",type=str,default="multinomial")

# Read arguments from command line
args = parser.parse_args()

test_ratio_arr=[]
files = glob.glob('./select_best/*')
for f in files:
    test_ratio_arr.append(f)
# run this code after running train.py
# this code prins out top 2 bins for each fitness fucntion 
# and its corresponding gamma values
fitness_funct=args.fitness_function
t = load_data(path=[args.dataset]) 
# t = load_data_patch(path=['crops_bl_nwpu.txt']) 
# test_ratio_arr =[2053,4106,5133]
best_2(t,fitness_funct=fitness_funct,test_ratio_arr=test_ratio_arr,gammas=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9])


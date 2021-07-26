from load_data import load_data,load_data_patch
from select_best import best_2
import os
test_ratio_arr=[]
files = glob.glob('./select_best/*')
for f in files:
    test_ratio_arr.append(f)
# run this code after running train.py
# this code prins out top 2 bins for each fitness fucntion 
# and its corresponding gamma values
fitness_funct='multinomial'
t = load_data(path=[r'Val_new.txt']) 
# t = load_data_patch(path=['crops_bl_nwpu.txt']) 
# test_ratio_arr =[2053,4106,5133]
best_2(t,fitness_funct=fitness_funct,test_ratio_arr=test_ratio_arr,gammas=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9])


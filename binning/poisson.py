import numpy as np
import json
from load_data import make_freq_dict
from bayesian_blocks import bayesian_blocks

def find_lamhdas(x,bins):
    '''
    Parameters: 
    -----------
            => x = train array
            => bins = bins estimated by using bayesian blocks on train data
    
    Function:
    ----------
    Used to find the lambda parameters for each bin.

    Output:
    -------
    returns list of lambdas.
    '''
    bin_num =[]
    bin_wd=[]
    lambdas=[]

    for i in range(len(bins)-1):
        num=0

        for j in x:
            if j>=bins[i] and  j<bins[i+1]:
                num+=1
            if i==len(bins)-2 and j== bins[i+1]:
                num+=1
        bin_wd.append(abs(bins[i]-bins[i+1]))
        bin_num.append(num)
        lambdas.append((num/abs(bins[i]-bins[i+1])))

    return lambdas

def likeli_poisson(x_test,lambdas,bins):
    '''
    Parameters: 
    -----------
            => x_test = test array
            => lambdas = list of lambdas estimated for each bin on train data.
            => bins = bins estimated by using bayesian blocks on train data
    
    Function:
    ----------
    Used to find the Log Likelihood of the test data, using paramters estimated on train data.

    Output:
    -------
    returns likelihood value.
    '''
    likli =0

    for i in range(len(bins)-1):
        for j in x_test:
            if j>=bins[i] and  j<bins[i+1]:
                likli+= (j)*np.log(lambdas[i])-lambdas[i]#ℓ(λ)=ln (f(x|λ))=−nλ+tlnλ.,n=1, likelihood of that point
            if i==len(bins)-2 and j== bins[i+1]:
                likli+= (j)*np.log(lambdas[i])-lambdas[i] #ℓ(λ)=ln (f(x|λ))=−nλ+tlnλ.,n=1, likelihood of that point
    
    return likli

def poisson_bay_block(tr,tes,k,gammas,iter):
    '''
    Parameters: 
    -----------
            => tr = train data
            => tes = test data
            => k = value of factor in prior function (1-gamma)/(1-gamma**(N//2**k))
            => gammas = list of gammas to iterate over
            => iter = number of times the experiment has to be performed
    
    Function:
    ----------
    Used to estimate the parameters of poisson on train data.
    And calculate the log likelihood for test data for varying gamma.
    Output:
    -------
    returns likelihood list with parameters.
    '''

    total_likeli=[]
    dumper={}
    for gamma in gammas:
        likeli_poi=[]
        fold=0
        for_best =[]
        for i in range(iter):
            X_train = tr[i]
            X_test =tes[i]
            bin_edges = bayesian_blocks(X_train,fitness='poisson',lam=k,gamma=gamma)
            # print("edges",bin_edges)
            lambdas = find_lamhdas(X_train,bin_edges)
            # print("lambda",lambdas)
            likli=likeli_poisson(X_test,lambdas,bin_edges)
            tr_likeli= likeli_poisson(X_train,lambdas,bin_edges)
            likeli_poi.append([fold,-likli,len(bin_edges)-1])#negetive log likeli
            #saving the gammas, folds, likelihoods
            # with open("./poisson_likeli/"+str(len(tes[0]))+"/poi_"+str(gamma)+"_"+".csv","a+") as output:
            #     output.write(str(gamma)+","+str(fold)+","+str(-likli)+"\n")
            # output.close()
            # with open("./poisson_likeli/"+str(len(tes[0]))+"/poi_bins_"+str(gamma)+"_"+".csv","a+") as output:
            #     output.write(str(gamma)+","+str(fold)+","+str(bin_edges)+"\n")
            # output.close() 
            for_best.append(-likli)          
            # likeli_poi.append([fold,-tr_likeli,len(bin_edges)-1]) # uncomment for train likeli
            fold+=1
        total_likeli.append([gamma,likeli_poi])
        mu = np.mean(for_best)
        sig = np.std(for_best)
        dumper[gamma]=mu/sig
        # with open("./poisson_likeli/"+str(len(tes[0]))+"/poi_mu_sig_"+".csv","a+") as output:
        #     output.write(str(gamma)+","+str(fold)+","+str(mu/sig)+"\n")
        # output.close() 
    # print(total_likeli)  
    with open("./select_best/poi_mu_sig_"+str(len(tes[0]))+".json", "w") as write_file:
        json.dump(dumper, write_file)
    
    return total_likeli
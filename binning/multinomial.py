import numpy as np
import json
from load_data import make_freq_dict
from bayesian_blocks import bayesian_blocks




def find_prob(x,bins):
    '''
    Parameters: 
    -----------
            => x = train_data
            => bins = bin edges from the bayesian blocks 
    
    Function:
    ----------
    Used to find the probabilities of each of the training samples, within its bin.

    Output:
    -------
    returns probabilities bin wise as a list of dicts
    '''
    c=[]
    x_i=[]
    p=[]
    for i in range(len(bins)-1):
        lis=[]
        for j in x:
            if j>=bins[i] and  j<bins[i+1]:
                lis.append(j)
            if i==len(bins)-2 and j== bins[i+1]:
                lis.append(j)
        freq = make_freq_dict(lis)
        c.append(list(freq.values()))
        x_i.append(list(freq.keys()))  #x_i = list of lists: values of corresponding probability

    for row in c:
        temp=[]
        for i in row:
            temp.append(i/sum(row))
        p.append(temp)                 #p= list of list: prob of all train samples

    dic_lis=[]
    for i in range(len(p)):
        dic={}
        for j in range(len(p[i])):
            dic[x_i[i][j]]=p[i][j]  #dict of probabilities within a bin
        dic_lis.append(dic)         #list of dicts over all the bins.

    return dic_lis
    
    

def find_prob_test(x_test,dic_lis,bins):
    '''
    Parameters: 
    -----------
            => x_test = test list of counts
            => dic_list = probabilities bin wise as a list of dicts estimated on train data
            => bins = bin edges from the bayesian blocks estimated on train_data
    
    Function:
    ----------
    Used to find the probabilities of each of the testing samples.
    If new sample exists in test but not in train, the probabilty for that is taken as 0.

    Output:
    -------
    returns dict of x_test amd its corresponding prob
    '''
    prob={}
    for i in range(len(bins)-1):
        #lis=[]
        for j in x_test:
            if j>=bins[i] and  j<bins[i+1]:
                #id.append(i)
                if j in dic_lis[i]:
                    prob[j]=dic_lis[i][j]
                else:
                    prob[j]=0.0
            if i==len(bins)-2 and j== bins[i+1]:
                if j in dic_lis[i]:
                    prob[j]=dic_lis[i][j]
                else:
                    prob[j]=0.0
    return prob



def likeli_mln(x_test,prob):
    '''
    Parameters: 
    -----------
            => X_test = test array
            => prob = probabilities estimated on test data
    
    Function:
    ----------
    Used to find the Log Likelihood of the test data.

    Output:
    -------
    returns likelihood value.
    '''
    likeli=0
    for i in x_test:
        if i in prob:
            if prob[i]!=0:
                likeli+= i*np.log(prob[i])#x_i log p_i
    return likeli



def multinomial_bay_block(tr,tes,k,gammas,iter):
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
    Used to estimate the parameters of multinominal on train data.
    And calculate the log likelihood for test data for varying gamma.
    
    Output:
    -------
    returns likelihood list with parameters.
    '''
    dumper={}
    total_likeli=[]
    for gamma in gammas:
        likeli_mlnn=[]
        for_best=[] # array for selecting best one
        fold=0
        for i in range(iter):
            X_train = tr[i]
            X_test =tes[i]
            bin_edges = bayesian_blocks(X_train,fitness='multinomial',lam=k,gamma=gamma)
            # print("edges",bin_edges)
            dic_lis = find_prob(X_train,bin_edges)
            prob_train = find_prob_test(X_train,dic_lis,bin_edges)
            prob = find_prob_test(X_test,dic_lis,bin_edges)
            #print(prob)
            likeli= likeli_mln(X_test,prob)
            tr_likeli = likeli_mln(X_train,prob_train)
            #print("likeli",likeli)
            likeli_mlnn.append([fold,-likeli,len(bin_edges)-1])#negetive log likeli
            #saving the gammas, folds, likelihoods
            # with open("./mln_likeli/"+str(len(tes[0]))+"/mln_"+str(gamma)+"_"+".csv","a+") as output:
            #     output.write(str(gamma)+","+str(fold)+","+str(-likeli)+"\n")
            # output.close()
            # with open("./mln_likeli/"+str(len(tes[0]))+"/mln_bins_"+str(gamma)+"_"+".csv","a+") as output:
            #     output.write(str(gamma)+","+str(fold)+","+str(bin_edges)+"\n")
            # output.close()    
            for_best.append(-likeli)
            
            # likeli_mlnn.append([fold,-tr_likeli,len(bin_edges)-1])  # uncomment for train likeli
            fold+=1
        total_likeli.append([gamma,likeli_mlnn])
        mu = np.mean(for_best)
        sig = np.std(for_best)
        dumper[gamma]=mu/sig

        # with open("./mln_likeli/"+str(len(tes[0]))+"/mln_mu_sig_"+".csv","a+") as output:
        #         output.write(str(gamma)+","+str(fold)+","+str(mu/sig)+"\n")
        # output.close()
    # print(total_likeli)  
    with open("./select_best/mln_mu_sig_"+str(len(tes[0]))+".json", "w") as write_file:
        json.dump(dumper, write_file)

    return total_likeli








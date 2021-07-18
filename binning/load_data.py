import numpy as np
import json

def load_data_patch(path):
    '''
    Parameters: 
    ----------- 
    path of data

    Function:
    -----------
    Loading data from txt file in the form [count_of_people_in_patch]
    
    Output:
    -------
     returns array of patch counts x =[0.0, 0.0, 0.0, 1.0, 2.0, 5.0, ..., 20033.0] with npise
    '''
    cumul = []
    j = 0

    for i in path:
        f = open(i, "r")
        k = f.read().replace("[","").replace("]","")
        k = k.split(",")
        k = [float(i) for i in k]
        x = k
        # for i in range(len(x)):
        #     x[i] = int(x[i])
        # x = x.astype(int)
        # print(x)

        x = np.hstack((x,np.asarray(list(range(int(min(x)),int(max(x))+1)))))# noise addition step comment if you dont want to add noise
        # x = np.hstack((x,np.linspace(min(x),max(x),num=int(max(x)+1)))) #noise =2
        # x = np.hstack((x,np.linspace(min(x),max(x),num=int(max(x)+1)))) #noise =3
        # print(x)
    return x






def load_data(path):
    '''
    Parameters: 
    ----------- 
    path of data

    Function:
    -----------
    Loading data from txt file in the form [imgname,count_of_people_in_img,datasetcode]
    datasetcode=[1:sta train+val,
                  2: sta test,
                  3:sta train+val,
                  4: sta test,
                  5:sta train+val,
                  6: sta test,
                  7: nwpu]
    
    Output:
    -------
     returns array of counts x =[0.0, 0.0, 0.0, 1.0, 2.0, 5.0, ..., 20033.0]
    '''
    cumul = []
    j = 0

    for i in path:
        tr_nwpu = np.genfromtxt(i,delimiter=',')
        tr_nwpu =  tr_nwpu[tr_nwpu[:,1].argsort()]
        x = tr_nwpu[:,1]
        # for i in range(len(x)):
        #     x[i] = int(x[i])
        # x = x.astype(int)
        # print(x)

        x = np.hstack((x,np.asarray(list(range(int(min(x)),int(max(x))+1)))))# noise addition step comment if you dont want to add noise
        # x = np.hstack((x,np.linspace(min(x),max(x),num=int(max(x)+1)))) #noise =2
        # x = np.hstack((x,np.linspace(min(x),max(x),num=int(max(x)+1)))) #noise =3
        # print(x)
    return x

def make_freq_dict(t):
    '''
    Parameters: 
    -----------
    array of counts t =[0.0, 0.0, 0.0, 1.0, 2.0, 5.0, ..., 20033.0]

    Function: 
    ---------
    Makes a dict which gives the histogram of counts with the count as key and number of such images as value.
    
    Output:
    ------- 
    returns dict{count_of_people_in_img : number_of_such_images}
    '''
    dictt={}
    for i in t:
        if i in dictt:
            dictt[i]+=1
        else:
            dictt[i]=1
    return dictt


def read_dicts(test_ratio,seeds_path='seeds.txt',path='./test_jsons/test'):
    '''
    Parameters: 
    -----------
            => seeds_path = path of seeds file
            => path = test or train json files path
    
    Function:
    ----------
    From dicts, converting into list of lists (can be used for both train and test, used in make_train_test).
    Outer list in size of iter, inner list in size of train or test samples.
    
    Output:
    -------
    returns integer lists of lists, with array of counts ex. [0.0, 0.0, 0.0, 1.0, 2.0, 5.0, ..., 20033.0]
    '''

    seeds = np.loadtxt(seeds_path) 
    i=seeds[0]
    output=[]
    for i in seeds:
        lis=[]
        flattened=[]
        with open(path+str(i)+"_"+str(test_ratio)+'.json', 'r') as fp:
            testt = json.load(fp)
        lis=[[x]*testt[x] for x in testt.keys()]
        flattened = [int(float(y)) for x in lis for y in x]
        output.append(flattened)

    # print("...",output)
    return output

def make_train_test(t,test_ratio,iter,change_seed=True):
    '''
    Parameters:
    -----------
            => t : array of counts t =[0.0, 0.0, 0.0, 1.0, 2.0, 5.0, ..., 20033.0]
            => test_ratio : Sample size ratio kept aside for likelihood estimation
            => iter : Number of times the likelihood should be calculated (to check variance and mean likelihood).
            => change_seed : If set to True, new set of seeds will be generated. Changing number of iterations also changes the seed values.
    
    Function:
    ----------
    Takes the array of counts and divides into train and test arrays.
    Step 1 : Select a bin randomly, from existing non zero bins. (random numbers sampled from a discrete uniform distribution (np.random.randint))
    Step 2 : Sends one count from train array to test array and updates the length of the bins.
    Step 3 : Zero bins are removed, 
    then go to Step 1 and Repeat until number of samples in test array are equal to test_ratio that mentioned in Input.
    Step 4 : Repeat the process for iter  (Input) number of times.
    
    Output: 
    -------
    returns lists of train and test arrays , number of lists == iter
    '''

    test_size = int((len(t))*test_ratio)
    freq = make_freq_dict(t)
    # print(test_ratio,test_size)
    # loading seed from previously saved file, Updating if number of iterations changed

    seeds = np.loadtxt('seeds'+str(int(iter))+'.txt')
    # if len(seeds)!=iter:
    #     # changing seeds when iter changes
    #     change_seed=True
    # if change_seed:
    #     # code for new set of seeds.    
    #     seed_array = np.random.randint(999,9999,iter)
    #     np.savetxt("seeds"+str(int(iter))+".txt",seed_array)

    seeds = np.loadtxt('seeds'+str(int(iter))+'.txt') 
    # print(len(seeds))
    # generation train test lists (number of such lists == iter)
    for it in range(iter):
        dictt=freq.copy()
        test_dict ={}
        np.random.seed(int(seeds[it]))

        # fill test dict until the test_ratio_size is achieved 
        while sum(list(test_dict.values())) < test_size:
            index = np.random.randint(0,len(dictt))
            keyy = list(dictt.keys())[index]
            if keyy in test_dict:
                test_dict[keyy]+=1
                dictt[keyy]-=1
            else:
                test_dict[keyy]=1
                dictt[keyy]-=1
            
            if dictt[keyy] ==0:
                del dictt[keyy]
 
        #saving dicts with seed name
        # for k,v in test_dict.items():
        #     test_dict[k] = float(v)
        
        
        
        if change_seed ==True:
            # test_dict = np.asarray(test_dict)
            with open('./test_jsons/test'+str(seeds[it])+"_"+str(test_ratio)+".json", 'w') as fp:
                json.dump(test_dict, fp)
            with open('./train_jsons/train'+str(seeds[it])+"_"+str(test_ratio)+'.json', 'w') as fp:
                json.dump(dictt, fp)
        
    # reading from dicts and converting into list of lists. 
    test = read_dicts(test_ratio,seeds_path='seeds'+str(int(iter))+'.txt',path='./test_jsons/test')
    train = read_dicts(test_ratio,seeds_path='seeds'+str(int(iter))+'.txt',path='./train_jsons/train')
    # print(train)
    return train,test

# t = load_data(path=['train_list_nwpu.txt'])
# tr,tes = make_train_test(t,test_ratio=0.1,iter=10)




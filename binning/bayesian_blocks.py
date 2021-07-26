"""
Bayesian Block implementation
=============================

Dynamic programming algorithm for finding the optimal adaptive-width histogram.

Based on Scargle et al 2012 [1]_

References
----------
.. [1] http://adsabs.harvard.edu/abs/2012arXiv1207.5578S
"""
import numpy as np
from astroML.utils import deprecated
from astroML.utils.exceptions import AstroMLDeprecationWarning



class FitnessFunc(object):
    """Base class for fitness functions

    Each fitness function class has the following:
    - fitness(...) : compute fitness function.
       Arguments accepted by fitness must be among [T_k, N_k, a_k, b_k, c_k]
    - prior(N, Ntot) : compute prior on N given a total number of points Ntot
    """
    def __init__(self, p0=0.05, gamma=None):
        self.p0 = p0
        self.gamma = gamma

    def validate_input(self, t, x, sigma):
        """Check that input is valid"""
        pass

    def fitness(self,**kwargs):
        raise NotImplementedError()

    def prior(self, N, Ntot):
        if self.gamma is None:
            return self.p0_prior(N, Ntot)
        else:
            return self.gamma_prior(N, Ntot)

    def p0_prior(self, N, Ntot):
        # eq. 21 from Scargle 2012
        return 4 - np.log(73.53 * self.p0 * (N ** -0.478))

    def gamma_prior(self, N, Ntot,lam):
        """Basic prior, parametrized by gamma (eq. 3 in Scargle 2012)"""
        if self.gamma == 1:
            return 0
        else:
            return (np.log(1 - self.gamma)
                    - np.log(1 - self.gamma ** (Ntot//2**(lam)))
                    + N * np.log(self.gamma))

    # the fitness_args property will return the list of arguments accepted by
    # the method fitness().  This allows more efficient computation below.
    @property
    def args(self):
        try:
            # Python 2
            return self.fitness.func_code.co_varnames[1:]
        except AttributeError:
            return self.fitness.__code__.co_varnames[1:]



class Poisson(FitnessFunc):
    """Fitness for binned or unbinned events

    Parameters
    ----------
    p0 : float
        False alarm probability, used to compute the prior on N
        (see eq. 21 of Scargle 2012).  Default prior is for p0 = 0.
    gamma : float or None
        If specified, then use this gamma to compute the general prior form,
        p ~ gamma^N.  If gamma is specified, p0 is ignored.
    """
    def fitness(self, N_k, T_k):
        # eq. 19 from Scargle 2012
        return N_k * (np.log(N_k) - np.log(T_k))

    def prior(self, N, Ntot,lam):
        if self.gamma is not None:
            #print("Gamma Sucess")
            return self.gamma_prior(N, Ntot,lam)
        else:
            print("Provide gamma")


class Multinomial(FitnessFunc):
    """Fitness for binned or unbinned events

    Parameters
    ----------
    p0 : gamma for a prior
    gamma : float or None
        If specified, then use this gamma to compute the general prior form,
        p ~ gamma^N.  If gamma is specified, p0 is ignored.
    """
    def fitness(self, sum_log_fact_count, sum_nn_vec_log_mult,sum_cnt_vec_log_mult):
        # -1_mlog(xj!)+1_m lx_jlog(xj)-nlog(n)
        return -sum_log_fact_count+sum_nn_vec_log_mult-sum_cnt_vec_log_mult

    def prior(self, N, Ntot,lam):
        if self.gamma is not None:
            #print("Gamma Sucess")
            return self.gamma_prior(N, Ntot,lam)
        else:
            print("Provide gamma")




def bayesian_blocks(t, x=None, sigma=None,
                    fitness='poisson',lam=2, **kwargs):
    """Bayesian Blocks Implementation

    This is a flexible implementation of the Bayesian Blocks algorithm
    described in Scargle 2012 [1]_

    Parameters
    ----------
    t : array_like
        data times (one dimensional, length N)
    x : array_like (optional)
        data values
    sigma : array_like or float (optional)
        data errors
    fitness : str or object
        the fitness function to use.
        If a string, the following options are supported:

        - 'events' : binned or unbinned event data
            extra arguments are `p0`, which gives the false alarm probability
            to compute the prior, or `gamma` which gives the slope of the
            prior on the number of bins.
        - 'poisson' : fitness function is chosen as likelihood of poisson .
        - 'multinomial' : fitness function is chosen as likelihood of multinomial


        Alternatively, the fitness can be a user-specified object of
        type derived from the FitnessFunc class.

    Returns
    -------
    edges : ndarray
        array containing the (N+1) bin edges

    """
    # validate array input
    t = np.asarray(t, dtype=float)
    if x is not None:
        x = np.asarray(x)
    if sigma is not None:
        sigma = np.asarray(sigma)

    # verify the fitness function
    if fitness == 'poisson':
        if x is not None and np.any(x % 1 > 0):
            raise ValueError("x must be integer counts for fitness='poisson'")
        fitfunc = Poisson(**kwargs)
    elif fitness == 'multinomial':
        if x is not None and (np.any(x % 1 > 0) or np.any(x > 1)):
            raise ValueError("x must be integer counts for fitness='multinomial'")
        fitfunc = Multinomial(**kwargs)
    else:
        if not (hasattr(fitness, 'args') and
        hasattr(fitness, 'fitness') and
                hasattr(fitness, 'prior')):
            raise ValueError("fitness not understood")
        fitfunc = fitness

    # find unique values of t
    t = np.array(t, dtype=float)
    # t =[0,0,0,...,20033] all counts
    assert t.ndim == 1
    unq_t, unq_ind, unq_inv = np.unique(t, return_index=True,
                                        return_inverse=True)
    '''
    unq_t : unique values of t (unique counts)
    unq_ind : indicies of first occrances of unique counts
    unq_inv : The indices to reconstruct the original array from the unique array.
    '''
    # if x is not specified, x will be counts at each time
    if x is None:
        if sigma is not None:
            raise ValueError("If sigma is specified, x must be specified")

        if len(unq_t) == len(t):
            x = np.ones_like(t)
        else:
            x = np.bincount(unq_inv)   # makes x have counts of the array
        
        t = unq_t  # unique values of t                    #
        sigma = 1

    # if x is specified, then we need to sort t and x together
    else:
        x = np.asarray(x)

        if len(t) != len(x):
            raise ValueError("Size of t and x does not match")

        if len(unq_t) != len(t):
            raise ValueError("Repeated values in t not supported when "
                             "x is specified")
        t = unq_t
        x = x[unq_ind]

    # verify the given sigma value
    N = t.size
    if sigma is not None:
        sigma = np.asarray(sigma)
        if sigma.shape not in [(), (1,), (N,)]:
            raise ValueError('sigma does not match the shape of x')
    else:
        sigma = 1

    # validate the input
    fitfunc.validate_input(t, x, sigma)

    # compute values needed for computation, below
    if 'a_k' in fitfunc.args:
        ak_raw = np.ones_like(x) / sigma / sigma
    if 'b_k' in fitfunc.args:
        bk_raw = x / sigma / sigma
    if 'c_k' in fitfunc.args:
        ck_raw = x * x / sigma / sigma

    # create length-(N + 1) array of cell edges
    edges = np.concatenate([t[:1],
                            0.5 * (t[1:] + t[:-1]),
                            t[-1:]])
    block_length = t[-1] - edges
    # print("block_length",block_length )
    # arrays to store the best configuration
    best = np.zeros(N, dtype=float)
    last = np.zeros(N, dtype=int)

    #code added-------------------------
    act =t
    prev = -1
    nk_array = []
    for i in range(act.size):
    	if act[i]==prev:
    		nk_array[-1]+=1
    	else:
    		nk_array.append(1)
    	prev=act[i]
    nn_vec = np.array(nk_array)
    log_nn_vec = np.log(nn_vec)
    nn_vec_log_mult = nn_vec*log_nn_vec
    #-------------------------------------

    lll=0
    #-----------------------------------------------------------------
    # Start with first data cell; add one cell at each iteration
    #-----------------------------------------------------------------
    for R in range(N):
        # Compute fit_vec : fitness of putative last block (end at R)
        kwds = {}
        if fitness == 'poisson':
            # T_k: width/duration of each block
            if 'T_k' in fitfunc.args:
                kwds['T_k'] = block_length[:R + 1] - block_length[R + 1]

            # N_k: number of elements in each block
            if 'N_k' in fitfunc.args:
                kwds['N_k'] = np.cumsum(x[:R + 1][::-1])[::-1]

        #code added --------------------------
        elif fitness == 'multinomial':
            '''
            variables used for calulating the likelihood of multinomial
            '''
            if 'sum_log_fact_count' in fitfunc.args:
                kwds['sum_log_fact_count'] = np.cumsum(log_nn_vec[:R + 1][::-1])[::-1]
            #∑j=1_mx_jlog(xj)
            if 'sum_nn_vec_log_mult' in fitfunc.args:
                kwds['sum_nn_vec_log_mult'] = np.cumsum(nn_vec_log_mult[:R + 1][::-1])[::-1]
            #nlog(n)
            if 'sum_cnt_vec_log_mult' in fitfunc.args:
                kwds['sum_cnt_vec_log_mult'] = (np.cumsum(nn_vec[:R + 1][::-1])[::-1])*np.log(np.cumsum(nn_vec[:R + 1][::-1])[::-1])
        #---------------------------------------


        # evaluate fitness function
        fit_vec = fitfunc.fitness(**kwds)
        # print("data",t[:R])
        # print("fit_vec",fit_vec)
        # print("prior",fitfunc.prior(R + 1, N,lam))
        # print(lll)
        lll+=1
        # print("prior",fitfunc.prior(R + 1, N,lam))

        A_R = fit_vec + fitfunc.prior(R + 1, N,lam)
        A_R[1:] += best[:R]
        # print("best",best)

        i_max = np.argmax(A_R)
        last[R] = i_max
        # print("last",last)
        best[R] = A_R[i_max] 
        #  fitfunc.prior(R + 1, N,lam)
        # print("last", last)

    #-----------------------------------------------------------------
    # Now find changepoints by iteratively peeling off the last block
    #-----------------------------------------------------------------
    change_points = np.zeros(N, dtype=int)
    i_cp = N
    ind = N
    while True:
        i_cp -= 1
        change_points[i_cp] = ind
        if ind == 0:
            break
        ind = last[ind - 1]
    change_points = change_points[i_cp:]
    # print("bins",edges[change_points])
    return edges[change_points]

# X_train = [1,2,3,4,4,5,5,5,5,6,7,8,0,0,0,0,2,3,4,4,5,5,5,5,6,7,8,0,0,0,0]
# print(bayesian_blocks(X_train,fitness='multinomial',lam=2,gamma=0.1))
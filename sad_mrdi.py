'''This file has all of the code necessary for plotting SADs and MRDIs as predicted by METE.
It also has code to simulate these distributions to build a log likelihood distribution. This is so that
we can compare the empirical log likelihood to this distribution to see how good the fit is. This is known as
a parametric bootstrap. 
Additionally, I included a function to calculate AIC values to compare models, and the
lognormal model, so that we can look at how well the logseries vs. lognormal describe the data.
This file should be broadly applicable across ecosystems.'''

import numpy as np
import scipy.stats as st
from scipy.optimize import fsolve

# Define a default random seed
rng = np.random.default_rng(12)

# METE beta
def beta_constraint_approx(b,S,N):
    '''This is the beta constraint in METE with give state variables. Use this as a function call to get beta.
    This version is an approximation to the true sum.
    Inputs S and N
    Also inputs beta
    outputs beta constraint to minimize'''
    return b*np.log(1/(1-np.exp(-b)))-S/N

def get_beta_approx(S,N,b0=0.0001):
    '''This returns the METE beta for a given S and N. Uses the approximate version of the constraint.
    Good for if it's very slow.
    Optional input of an initial beta, if we know it's going to be somewhere other than small positive.
    outputs array of lambdas'''
    beta = fsolve(beta_constraint_approx,b0,args=(S,N))[0]
    return beta

def beta_constraint(b,S,N):
    '''This is the beta constraint in METE with given state variables. This version doesn't rely on any approximations.
    Use this as a function call to get beta.
    Inputs S and N
    Also inputs beta
    outputs beta constraint to minimize'''
    nrange = np.arange(N)+1
    expnb = np.exp(-nrange*b)
    return expnb.sum()/(expnb/nrange).sum()-N/S

def get_beta(S,N,b0=0.0001):
    '''This returns the METE beta for a given S and N.
    Optional input of an initial beta, if we know it's going to be somewhere other than small positive.
    outputs array of lambdas'''
    beta = fsolve(beta_constraint,b0,args=(S,N))[0]
    return beta

# Define functions for SAD
def sad_rank(r,s,be):
    ''' Return rank ordered SAD by using the isf function in logseries.
    Inputs the number of species s and beta
    Returns the phi(r), the SAD at rank r'''
    return st.logser.isf((r-0.5)/s,p=np.exp(-be))
    
def sad_rvs(s,be,rs=rng):
    '''Simulate s = number of species draws from a logseries distribution with parameter be = beta
    Return rank ordered abundances
    By default put the seed as the global one above, but make it changeable'''
    d = st.logser.rvs(np.exp(-be), loc=0, size=s, random_state=rs)
    return np.sort(d)[::-1]

def sad_logll(pts,be):
    '''Get the log likelihood for the SAD by summing over all pts for a corresponding be = beta'''
    logp = st.logser.logpmf(pts, p=np.exp(-be), loc=0)
    return np.sum(logp)

# Define distributions for MRDI
def mrdi_rank(r,l,N):
    '''
    Modified from equation 7.37 in John's book -- 
    an approximation of the rank ordered equation for psi, the metabolic rate distribution.
    This is modified in that it uses the cdf we defined below, which is MUCH more accurate than John's.
    This is approximate for several reasons, including the factor of 1/2, but it's good enough for visual comparison.
    Inputs r as ranks, l is lambda 1 and 2 as array-like, and N is number of individuals.
    Outputs psi at rank r.
    '''
    logarg = ((np.exp(l[0]+l[1])-1)*N+r-1/2)/(r-1/2)
    return (np.log(logarg) - l[0])/l[1]

def mrdi_pdf(e,l):
    '''The actual probability function for the MRDI, with a very accurate normalization.
    Returns psi at metabolic rate e given lambdas as array-like
    Note that this is slightly different from Eq. 7.24'''
    eg = np.exp(-l[0]-l[1]*e)
    return l[1]*(np.exp(l[0]+l[1])-1) * eg/(1-eg)**2

def mrdi_cdf(e,l):
    '''The CDF for psi from 1 to e given array-like lambdas.'''
    return 1-(np.exp(l[0]+l[1])-1)/(np.exp(l[0]+l[1]*e)-1)

def mrdi_inv_cdf(u,l):
    '''Inverse of the cdf for sampling. u is a random variable distributed uniformly between 0 and 1.'''
    b = l[0]+l[1]
    logarg = (u-np.exp(b))/(u-1)
    return (np.log(logarg)-l[0])/l[1]
    
def mrdi_rvs(n,l,rs=rng):
    '''Simulate n draws from the mrdi distribution with lambdas l
    Return rank ordered
    By default put the generator as a global one but make it changeable.
    '''
    # Get s random uniform variables
    u = rs.random(n)
    # Get the inverse cdf at that point
    e = mrdi_inv_cdf(u,l)
    # Return rank ordered
    return np.sort(e)[::-1]

def mrdi_logll(pts,l):
    '''Get the log likelihood by summing over all pts'''
    logp = np.log(mrdi_pdf(pts,l))
    return np.sum(logp)

# AIC functions
def aic(ll,k,n,correction=True):
    '''Calculate the AIC given the number of parameters k and the log likelihood. Also require the sample size n.
    If correction=True, use AICc. This is the default.
    '''
    corr = 0
    if correction:
        corr = 2*k*(1+k)/(n-k-1)
    return 2*k-2*ll+corr

def aic_weights(aic1,aic2):
    ''' Calculate the weights between two models given their aic values. This is calculated as Exp(-0.5*delta AIC)
    Return the weights as the largest weight first, then the smallest. Up to user to interpret which is which based 
    on which has the higher AIC.'''
    daic = np.abs(aic1-aic2)
    aicw = np.exp(-0.5*daic)
    return 1/(1+aicw),aicw/(1+aicw)

# Lognormal functions
def lognorm_fit(abd):
    '''Given abundance data, fit for lognorm parameters s and scale. The easiest way to do this is to log transform,
    then take the standard deviation and mean.
    Returns s, scale'''
    s = np.log(abd).std()
    scale = np.exp(np.log(abd).mean())
    return s,scale

def lognorm_ll(abd):
    '''Given abundances, calculate best fit parameters and return the corresponding log likelihood.'''
    s,scale = lognorm_fit(abd)
    return np.sum(st.lognorm.logpdf(abd,s=s,scale=scale))

def lognorm_sad(abd):
    '''Given abundances, return the predicted rank ordered SAD.'''
    # Get number of species
    s0 = len(abd)
    ranks = np.arange(s0)+1
    # Get params
    s,scale = lognorm_fit(abd)
    # Return isf at half ranks
    return st.lognorm.isf((ranks-0.5)/s0,s=s,scale=scale)
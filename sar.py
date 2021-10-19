# This function has the macroeco code curv as a dependency. Alternatively could have figured out imported models.
import _curves as curv

import numpy as np
import pandas as pd

def mete_sar(data,scales):
    '''
    Given a set of spatial data at some fine scale and the scales at which we want to make the comparison, 
    return the empirical number of species at each requested scale along with the slope of the empirical SAR
    at that slope, along with two METE predictions:
    1.  The number of species predicted at each scale, iterating down from the next highest scale 
        (ie. there is no one anchor scale, the information at one scale is used to get S at the next smallest scale)
    2.  The prediction for the slope z at that scale, obtained by taking the empirical S at that scale and dividing
        by the predicted S for the next smallest scale.
    
    Input
    data:   DataFrame with indices corresponding to sample sites (here it is S01-S30) 
            and columns corresponding to invidual species abundances at those sites.
    scales: An array of the list of scales at which to calculate the output metrics
    
    Returns
    sn:     A DataFrame containing the empirical S, N, their errors, and the slope z at each requested scale. 
            The indices are the scales, and z is obtained by 
            log(S(scale)/S(next smallest scale))/log(scale/next smallest scale)
    mete:   A DataFrame containing the predictions for S at each requested scale, obtained by downscaling iteratively 
            from the top scale. Note that because of this the largest S will be identical to the empirical value.
            This DataFrame additionally contains the predicted z at each scale, obtained by 
            log(S_empirical(scale)/S_theoretical(next smallest scale))/log(scale/next smallest scale)
    '''
    # Ensure scales is a sorted array
    scales = np.sort(scales)
    # Get number of scales
    nscales = len(scales)
    # Setup return arrays
    sn = pd.DataFrame(index=scales,columns=['s','serr','n','nerr','z'],dtype=float)
    mete = pd.DataFrame(index=scales,columns=['s','z'],dtype=float)

    # Now loop over each scale to get s and n at that scale
    for i in scales:
        # For each scale, get the number of iterations by dividing largest scale by current scale
        niter = int(np.floor(scales[-1]/i))
        # Make a temporary zeros array that is to sum/mean over
        sntemp = pd.DataFrame(columns=['s','n'],index=np.arange(niter))
        # Now get all combinations for s and n at this scale 
        # (ie. if there are 30 cells and scale is 15, this will iterate twice)
        for j in np.arange(niter):
            # Right now this always starts at 1 and goes until it no longer fits evenly.
            # (ie. if there are 30 cells, at scale 4 it stops at 28, 8 it stops at 24.)
            # It turns out the average seems decently robust against this.
            # Get first and last index for the data array
            fi = 'S{:02.0f}'.format((j+1)+j*(i-1))
            li = 'S{:02.0f}'.format((j+i)+j*(i-1))
            # Get number of species and individuals by summing over this range of cells
            sntemp.loc[j,'s'] = np.count_nonzero(data.loc[fi:li].sum())
            sntemp.loc[j,'n'] = data.loc[fi:li].sum().sum()
        # Input data into array. Take mean over all iters.
        sn.loc[i,'s'] = sntemp['s'].mean()
        sn.loc[i,'serr'] = sntemp['s'].std()
        sn.loc[i,'n'] = sntemp['n'].mean()
        sn.loc[i,'nerr'] = sntemp['n'].std()
        
    # Now get the mete prediction for each of these scales
    for i in np.arange(nscales-1): 
        # Use the code from macroeco. This inputs the scale we have and then the scale we want to predict at 
        # as the first argument, and then the data for the scale we have as the second argument.
        # The way I have this set up here is essentially doing curv.mete_sar_iterate.vals, but without being forced
        # to 1/2 for each iteration, and instead using the empirical data at each scale.
        # To reiterate, this uses the empirical data at the next highest scale to calculate a predicted S at the 
        # next lowest scale.
        mete['s'].iloc[i] = curv.mete_sar.vals([sn.index[i+1],sn.index[i]],
                                             sn['s'].iloc[i+1],sn['n'].iloc[i+1],approx=True)[1]
    # Append the largest scale to the end
    mete['s'].iloc[-1] = sn['s'].iloc[-1]

    # Now get empirical and theoretical z by looping over each scale and comparing that scale to the next scale down
    # Note that at the smallest scale, this isn't defined because it depends on the next smallest scale.
    for i in np.arange(nscales-1):
        # For empirical
        sn['z'].iloc[i+1] = np.log(sn['s'].iloc[i+1]/sn['s'].iloc[i])/np.log(sn.index[i+1]/sn.index[i])
        # Theoretical. Note that the larger scale here is the empirical one, since that was used to calculate the
        # smaller scale. We want to know z given the empirical S at the current scale.
        mete['z'].iloc[i+1] = np.log(sn['s'].iloc[i+1]/mete['s'].iloc[i])/np.log(sn.index[i+1]/sn.index[i])
        
    return sn,mete
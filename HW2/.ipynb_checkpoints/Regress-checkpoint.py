import numpy as np
import pandas as pd

def Regress(DF_X,Y):
    # Drop the na rows and reset the index of the rows
    
    if not isinstance(DF_X,pd.DataFrame):
        print("X Must be a Data Frame")
        return (-1,-1,-1,-1)
    
    if not isinstance(Y,np.ndarray):
        print("Y must be a numpy array")
        return (-1,-1,-1,-1)
    
    DF_X = DF_X.dropna()
    DF_X = DF_X.reset_index(drop = True)
    
    if DF_X.empty:
        print("X is empty")
        return (-1,-1,-1,-1)
    
    # turn dataframe to numpy array
    X = DF_X.values
    
    # store the number of data points and independent variables
    N = X.shape[0] 
    K = X.shape[1]   
    
    if N != Y.shape[0]:
        print("Y must be of same number of rows of X")
        return (-1,-1,-1,-1)
    
    # stack a column of ones to the beginning of the numpy array
    X = np.column_stack([np.ones(N), X])
    
    # calculate the estimates
    Beta = np.matmul(X.transpose(),X)
    Beta = np.linalg.inv(Beta)
    Beta = np.matmul(Beta,X.transpose())
    Beta = np.matmul(Beta,Y.transpose())
    
    # calculate error or residual vector
    Error = Y - np.matmul(X,Beta.transpose())
    
    # calculate standard error
    STD_ERR = np.matmul(Error.transpose(),Error)
    STD_ERR = STD_ERR / (N - K - 1) 
    
    # calculate standard error of coefficients
    VarBeta = STD_ERR * np.linalg.inv(np.matmul(X.transpose(),X))
    Beta_STD_Err = np.sqrt(VarBeta.diagonal())
        
    # caclculate confidence interval
    CI_L = Beta - 2 * Beta_STD_Err
    CI_R = Beta + 2 * Beta_STD_Err
    
    # return a tuple of (estimates,standard error,left bounds of CI,right bounds od CI)
    return (Beta,Beta_STD_Err,CI_L,CI_R)
    

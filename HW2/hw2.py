import pandas as pd
import numpy as np
import seaborn as sns
import plotly
import chart_studio.plotly as py
import matplotlib.pyplot as plt
import Regress
from matplotlib import style
from pandas.api.types import is_numeric_dtype
import os
%matplotlib inline

# get data from kaggle api
from kaggle.api.kaggle_api_extended import KaggleApi
from zipfile import ZipFile
import os
api = KaggleApi()
api.authenticate()

# data will be downloaded as a zip file to we shall unzip it
api.dataset_download_file('smid80/weatherww2','Summary of Weather.csv')
with ZipFile('Summary%20of%20Weather.csv.zip','r') as zipObj:
    zipObj.extractall()
    
# remove zip file once contents are extracted
os.remove("Summary%20of%20Weather.csv.zip")

# read data as csv
DF = pd.read_csv('Summary of Weather.csv')

# this function is used to explore the data
def plot_feature_against(df,col_list,target):
    
    plt.figure(figsize = (10,14))
    i = 0
    for col in col_list:
        if col == target:
            continue
        i += 1
        plt.subplot(8,3,i)
        plt.plot(df[col],df[target],marker = '.', linestyle = 'none')
        plt.title("%s vs %s"%(target,col))
        plt.tight_layout()


# extract numerical columns to test against one another
cols = DF.columns
col_list = []
for c in cols:
    if is_numeric_dtype(DF[c]):
        col_list.append(c)
plot_feature_against(DF,col_list,'MaxTemp')


# extract a sample of 200 points and run regression
Sample = DF.sample(n = 200, replace = False)

X = Sample[['MaxTemp']]
Y = Sample['MinTemp']

Beta, Sigma, CI_L,CI_R = Regress.Regress(X,Y.values)
print(Beta)
print(Sigma)
print(CI_L)
print(CI_R)

plt.figure()
# plot the points and regression lines
plt.scatter(X,Y)
plt.plot(X,Beta[0] + Beta[1] * X)


plt.figure()
# plot confidence intervals
Error1 = [Beta[0] - CI_L[0]]
Error2 = [Beta[1] - CI_L[1]]
plt.errorbar([Beta[0]] ,[Beta[0]] ,yerr = Error1, fmt = '.k')
plt.errorbar([Beta[1]] ,[Beta[1]] ,yerr = Error2, fmt = '.k')

plt.plot([-10,10],[0,0],'--')
plt.scatter([Beta[0],Beta[1]],[(CI_L[0] + CI_R[0])/2,(CI_L[1] + CI_R[1])/2])



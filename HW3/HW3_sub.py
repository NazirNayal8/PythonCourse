#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pystan
import numpy as np
import pandas as pd


Data = pd.read_csv('trend2.csv')


# In[2]:


Data = Data.dropna()
Data = Data.reset_index(drop = True)
Data.tail(10)


# In[3]:


# enumerate countries
countries = Data.country.str.strip()
unique_countries = countries.unique()
num_countries = len(unique_countries)
countries_dict = dict(zip(unique_countries, range(num_countries)))
countries = countries.replace(countries_dict).values
N = len(countries);
J = num_countries


# In[7]:


Model = """
data {
    int<lower=0> J;
    int<lower=0> N;
    int<lower=0> K;
    int<lower=1,upper=J> country[N];
    matrix[N,K] X;
    vector[N] y;
}

parameters {
    vector[J] a;
    vector[K] B;
    real mu_a;
    real<lower=0,upper=200> sigma_a;
    real<lower=0,upper=200> sigma_y;
}

transformed parameters {
    vector[N] y_hat;
    for(i in 1:N)
        y_hat[i] = a[country[i]] + X[i] * B;
}

model {
    sigma_a ~ normal(0,10);
    sigma_y ~ normal(0,10);
    B ~ normal(0,10);
    a ~ normal(mu_a,sigma_a);
    y ~ normal(y_hat,sigma_y);
}
"""

model_data = {'N':N,
              'J':J,
              'K':2,
              'country':countries + 1,
              'X': Data[['gini_net','rgdpl']],
              'y': Data['church2']}

model_fit = pystan.stan(model_code = Model, data = model_data, iter = 1000, chains = 2, n_jobs = 2)

print(model_fit)


# In[21]:


import matplotlib.pyplot as plt
a_sample = pd.DataFrame(model_fit['a'])

import seaborn as sns
sns.set(style="ticks", palette="muted", color_codes=True)

# Plot the orbital period with horizontal boxes
plt.figure(figsize=(16, 6))
sns.boxplot(data=a_sample, whis=np.inf, color="c")

model_fit.plot(pars=['sigma_a', 'B']);


# In[22]:


xvals = np.arange(2)
bp = model_fit['a'].mean(axis=0)
mp = model_fit['B'].mean()
for bi in bp:
    plt.plot(xvals, mp*xvals + bi, 'bo-', alpha=0.4)
plt.xlim(-0.1,1.1);


# In[26]:


Model2 = """
data {
    int<lower=0> J;
    int<lower=0> N;
    int<lower=0> K;
    int<lower=1,upper=J> country[N];
    matrix[N,K] X;
    vector[N] y;
}

parameters {
    vector[J] a;
    vector[K] B;
    real mu_a;
    real<lower=0,upper=200> sigma_a;
    real<lower=0,upper=200> sigma_y;
}

transformed parameters {
    vector[N] y_hat;
    for(i in 1:N)
        y_hat[i] = a[country[i]] + X[i] * B;
}

model {
    sigma_a ~ normal(0,10);
    sigma_y ~ normal(0,10);
    B[1] ~ normal(15,15);
    B[2] ~ normal(0,10);
    a ~ normal(mu_a,sigma_a);
    y ~ normal(y_hat,sigma_y);
}
"""

model_data2 = {'N':N,
              'J':J,
              'K':2,
              'country':countries + 1,
              'X': Data[['gini_net','rgdpl']],
              'y': Data['church2']}

model_fit2 = pystan.stan(model_code = Model, data = model_data2, iter = 1000, chains = 4, n_jobs = 2)

print(model_fit2)


# In[51]:


# After changing the prior on the explanatory variable estimate there was not a substantial effect on the posterior


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





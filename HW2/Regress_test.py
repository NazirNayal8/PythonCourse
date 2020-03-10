import unittest
import Regress
import pandas as pd
import numpy as np
import math

class RegressTest(unittest.TestCase):
    
    # This test is adapted from https://datatofish.com/multiple-linear-regression-python/
    def test_correct(self):
        Stock_Market = {'Year': [2017,2017,2017,2017,2017,2017,2017,2017,2017,2017,2017,2017,2016,2016,2016,2016,2016,2016,2016,2016,2016,2016,2016,2016],
                'Month': [12, 11,10,9,8,7,6,5,4,3,2,1,12,11,10,9,8,7,6,5,4,3,2,1],
                'Interest_Rate': [2.75,2.5,2.5,2.5,2.5,2.5,2.5,2.25,2.25,2.25,2,2,2,1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75],
                'Unemployment_Rate': [5.3,5.3,5.3,5.3,5.4,5.6,5.5,5.5,5.5,5.6,5.7,5.9,6,5.9,5.8,6.1,6.2,6.1,6.1,6.1,5.9,6.2,6.2,6.1],
                'Stock_Index_Price': [1464,1394,1357,1293,1256,1254,1234,1195,1159,1167,1130,1075,1047,965,943,958,971,949,884,866,876,822,704,719]        
                }
        df = pd.DataFrame(Stock_Market,columns=['Year','Month','Interest_Rate','Unemployment_Rate','Stock_Index_Price']) 
        Y = df['Stock_Index_Price']
        X = df[['Interest_Rate','Unemployment_Rate']]
        
        Beta, Sigma, CI_L, CI_R = Regress.Regress(X,Y.values)
        self.assertTrue((Beta[0] - 1798.40397763) < 1e-9)
        self.assertTrue((Beta[1] - 345.54008701) < 1e-9)
        self.assertTrue((Beta[2] - 250.14657137) < 1e-9)
        
        self.assertTrue((Sigma[0] - 899.248075) < 1e-9)
        self.assertTrue((Sigma[1] - 111.36692223) < 1e-9)
        self.assertTrue((Sigma[2] - 117.94986892) < 1e-9)
    
    def test_nan(self):
        Map = {
            'c1': [math.nan,math.nan],
            'c2': [math.nan,math.nan],
            'c3': [math.nan,math.nan]
            }
        DF = pd.DataFrame(Map,columns = ['c1','c2','c3'])
        Y = np.array([1,1])
        a,b,c,d = Regress.Regress(DF,Y)
        self.assertEqual(a,-1)

    def test_different_size(self):
        Map = {
            'c1': [1,1],
            'c2': [2,2],
            'c3': [3,3]
            }
        Df = pd.DataFrame(Map,columns = ['c1','c2','c3'])
        Y = np.array([1])
        a,b,c,d = Regress.Regress(Df,Y)
        self.assertEqual(a,-1)
        
    def test_Y_not_np(self):
        Map = {
            'c1': [1,1],
            'c2': [2,2],
            'c3': [3,3]
            }
        Df = pd.DataFrame(Map,columns = ['c1','c2','c3'])
        Y = np.array([1,1])
        Y = pd.DataFrame(Y)
        a,b,c,d = Regress.Regress(Df,Y)
        self.assertEqual(a,-1)
        
    def test_X_not_pd(self):
        Map = {
            'c1': [1,1],
            'c2': [2,2],
            'c3': [3,3]
            }
        Df = pd.DataFrame(Map,columns = ['c1','c2','c3'])
        Y = np.array([1,1])
        Y = pd.DataFrame(Y)
        a,b,c,d = Regress.Regress(Df.values,Y)
        self.assertEqual(a,-1)
        
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
    

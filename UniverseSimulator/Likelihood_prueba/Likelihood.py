#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 21:59:59 2022

@author: jesus
"""

from scipy import stats
import statsmodels.api as sm
import numpy as np
from statsmodels.base.model import GenericLikelihoodModel
from prueba_likelihood import simulator


class MyLikelihood(GenericLikelihoodModel):
    
    def __init__(self, endog, exog, **kwds):
        super(MyLikelihood, self).__init__(endog, exog, **kwds)

    def loglike(self, params):
        X = self.exog
        Y = self.endog
        temp = simulator(np.array(X), np.array(params))
        res = np.sum(np.abs(temp.evaluation() - np.array(Y)))
        return -res


if __name__ == "__main__":
    X = np.array([(1,1, 2), (2,2, 3), (3,3, 4), (4,4, 5), (5,5, 6)])
    Y = np.array([17, 31, 45, 59, 63])
    mod = MyLikelihood(endog = Y, exog = X)
    res = mod.fit()
    print('Parameters: alpha = %f; beta = %f; gamma = %f ' 
          % (res.params[0], res.params[1], res.params[2]))
    print('Standard errors: ', res.bse)
    print('P-values: ', res.pvalues)
    print('AIC: %f ' % res.aic)
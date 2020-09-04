import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.tsa.stattools as statsmodels
from statsmodels.tsa.api import VAR
from statsmodels.tsa.vector_ar.var_model import VARResults
from statsmodels.tsa.vector_ar.vecm import coint_johansen
from statsmodels.stats.stattools import durbin_watson
import numpy as np

class DataCleaning:

    @staticmethod
    def remove_empty_rows(df):
        return df.dropna()


#https://www.machinelearningplus.com/time-series/vector-autoregression-examples-python/
class VAR_Builder:

    def __init__(self, df, max_lags):
        self.df = df
        self.model_fitted = VARResults
        self.max_lags = max_lags

    def checkForRandomData(self):
        fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(10, 6))
        self.df.plot(ax=ax1)
        pd.plotting.lag_plot(self.df)
        plt.show()

    # stationarity check
    def augmented_dickey_fuller_statistics(self):

        for c in self.df.columns:
            result = statsmodels.adfuller(self.df[c])

            print('ADF Statistic: %f' % result[0])
            print('p-value: %f' % result[1])
            print('Critical Values:')
            for key, value in result[4].items():
                print('\t%s: %.3f' % (key, value))


    def cointegration_test(self, alpha=0.05):
        """Perform Johanson's Cointegration Test and Report Summary"""
        out = coint_johansen(self.df, -1, 5)
        d = {'0.90': 0, '0.95': 1, '0.99': 2}
        traces = out.lr1
        cvts = out.cvt[:, d[str(1 - alpha)]]

        def adjust(val, length=6): return str(val).ljust(length)

        # Summary
        print('Name   ::  Test Stat > C(95%)    =>   Signif  \n', '--' * 20)
        for col, trace, cvt in zip(self.df.columns, traces, cvts):
            print(adjust(col), ':: ', adjust(round(trace, 2), 9), ">", adjust(cvt, 8), ' =>  ', trace > cvt)


    def visualize_dataset(self):
        # Plot
        fig, axes = plt.subplots(nrows=len(self.df.columns), ncols=1, dpi=120, figsize=(10, 6))
        for i, ax in enumerate(axes.flatten()):
            data = self.df[self.df.columns[i]]
            ax.plot(data, color='red', linewidth=1)
            # Decorations
            ax.set_title(self.df.columns[i])
            ax.xaxis.set_ticks_position('none')
            ax.yaxis.set_ticks_position('none')
            ax.spines["top"].set_alpha(0)
            ax.tick_params(labelsize=6)

        plt.tight_layout()
        plt.show()

    #grangers_causation_matrix(df, variables=df.columns)
    def grangers_causation_matrix(self, maxlag, test='ssr_chi2test', verbose=False):
        """Check Granger Causality of all possible combinations of the Time series.
        The rows are the response variable, columns are predictors. The values in the table
        are the P-Values. P-Values lesser than the significance level (0.05), implies
        the Null Hypothesis that the coefficients of the corresponding past values is
        zero, that is, the X does not cause Y can be rejected.

        data      : pandas dataframe containing the time series variables
        variables : list containing names of the time series variables.
        """
        variables = self.df.columns
        df = pd.DataFrame(np.zeros((len(variables), len(variables))), columns=variables, index=variables)
        for c in df.columns:
            for r in df.index:
                test_result = statsmodels.grangercausalitytests(self.df[[r, c]], maxlag=maxlag, verbose=False)
                p_values = [round(test_result[i + 1][0][test][1], 4) for i in range(maxlag)]
                if verbose: print(f'Y = {r}, X = {c}, P Values = {p_values}')
                min_p_value = np.min(p_values)
                df.loc[r, c] = min_p_value
        df.columns = [var + '_x' for var in variables]
        df.index = [var + '_y' for var in variables]
        print(df)

    def select_order_of_VAR_model(self):
        model = VAR(self.df)
        print("\n*********checking different orders of lag************\n")
        for i in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            result = model.fit(i)
            print('Lag Order =', i)
            print('AIC : ', result.aic)
            print('BIC : ', result.bic)
            print('FPE : ', result.fpe)
            print('HQIC: ', result.hqic, '\n')

        #alternative
        print("\n*********select_order method used: ************\n")
        x = model.select_order(maxlags=self.max_lags)
        print(x.summary())

    def fit_VAR_model(self, lags):
        model = VAR(self.df)
        self.model_fitted = model.fit(lags)
        print("\n**********model_fitted, lag: " + str(lags) + "***********\n")
        print(self.model_fitted.summary())

        return self.model_fitted

    def check_for_serial_correlation(self, model):
        print("*********durbin watson serial correlation test**********")
        out = durbin_watson(model.resid)

        for col, val in zip(self.df.columns, out):
            print(col, ':', round(val, 2))

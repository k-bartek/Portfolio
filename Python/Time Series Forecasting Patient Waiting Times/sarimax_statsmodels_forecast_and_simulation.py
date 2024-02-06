
import pandas as pd
import glob
import numpy as np
import seaborn as sn
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_pacf, plot_acf
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import pacf
from pmdarima.arima import auto_arima
import pmdarima
import statsmodels.api as sm
import math
import seaborn as sns

from sarimax import norm_order,season_order
    

def forecast_accuracy(forecast, actual):
    mape = np.mean(np.abs(forecast - actual)/np.abs(actual))  # MAPE
    mape1 =  np.mean(np.abs((actual - forecast) /actual))
    me = np.mean(forecast - actual)             # ME
    mae = np.mean(np.abs(forecast - actual))    # MAE
    
    MAE1 = np.mean(np.abs(actual - forecast))
    mpe = np.mean((forecast - actual)/actual)   # MPE
    rmse = np.mean((forecast - actual)**2)**.5  # RMSE
   
    MSE = np.square(np.subtract(actual,forecast)).mean() 
    RMSE1 = math.sqrt(MSE)
    
    corr = np.corrcoef(forecast, actual)[0,1]   # corr
    mins = np.amin(np.hstack([forecast[:,None], 
                              actual[:,None]]), axis=1)
    maxs = np.amax(np.hstack([forecast[:,None], 
                              actual[:,None]]), axis=1)
    minmax = 1 - np.mean(mins/maxs)             # minmax
    #acf1 = acf(fc-test)[1]                      # ACF1
    return({'mape':mape, 'mape1':mape1,'me':me, 'mae': mae, 'mae1': MAE1,
            'mpe': mpe, 'rmse':rmse, 'RMSE1':RMSE1, 
            'corr':corr, 'minmax':minmax})

    
def denormalize_data(normalized_data, mean, std):
    denormalized_data = (normalized_data * std) + mean
    return denormalized_data

data = pd.read_csv('___exo.csv', parse_dates=['datetime'], index_col='datetime', header=0,sep=",")

#normalize data
#number of calls
mean_c = data['number_of_calls_hr'].mean()
std_c = data['number_of_calls_hr'].std()
data['number_of_calls_hr_n'] = (data['number_of_calls_hr'] - mean_c) / std_c

#number of shifts
____

#outcome
____





data = data[['wait_time_average_normalized', ______]]


TEST_SIZE = 24*30
train, test = data.iloc[:-TEST_SIZE], data.iloc[-TEST_SIZE:]
x_train, x_test = np.array(range(train.shape[0])), np.array(range(train.shape[0], data.shape[0]))
train.shape, x_train.shape, test.shape, x_test.shape

#if no norm_order and season_order is given - can also be selected manually in form (AR,d,MA)(SAR, D, SMA, season_m)
modelsx_calls = sm.tsa.statespace.SARIMAX(train[['wait_time_average_normalized']], exog=train[['open',_______]], order=norm_order,
                                 seasonal_order=season_order, trend=None,
                                 measurement_error=False,
                                 time_varying_regression=False,
                                 mle_regression=True, simple_differencing=False,
                                 enforce_stationarity=True,
                                 enforce_invertibility=True,
                                 hamilton_representation=False,
                                 concentrate_scale=False, trend_offset=1,
                                 use_exact_diffuse=False, dates=None,
                                 freq='H', missing='none',
                                 validate_specification=True)
result = modelsx_calls.fit()

# Print the model summary if needed
#print(result.summary())

#save the model
#result.save('model_try.pkl')


##necessary to load the model properly 
#from statsmodels.tsa.statespace.sarimax import SARIMAXResults
## patch around bug in SARIMAX class
#def __getnewargs__(self):
# return ((self.endog),(self.k_lags, self.k_diff, self.k_ma))
#SARIMAX.__getnewargs__ = __getnewargs__
#loaded = SARIMAXResults.load('model_try.pkl')




#predict
#provide the ____specifications, open/not open, number of calls etc for each hour instead of test in exog=
prediction = result.predict(exog=test[['open', _____]], start=train.shape[0], end=train.shape[0] + TEST_SIZE - 1)



#denormalize the predictions
pred1 = denormalize_data(prediction, mean_wt,std_wt)


#see forecast accuracy if needed
#test1 = denormalize_data(test['wait_time_average_normalized'],mean_wt,std_wt)
#print(forecast_accuracy(pred1,test1))


#append new data
#load df_t (new data that we want to append with exog variables)
#data = pd.read_csv('data_exo.csv', parse_dates=['datetime'], index_col='datetime', header=0,sep=",")
#df_t = df_t[['wait_time_average_normalized', 'open', _____]]

    #make sure the data follows right after the data used for training the model
#last_index_df1 = train.index.max()
#subset_df_t = df_t.loc[last_index_df1 + pd.Timedelta(days=0):] #subset based on last value of the train dataset

#subset_df_t = subset_df_t.resample('H').asfreq()
#subset_df_t = subset_df_t.drop(subset_df_t.index[0]) #get rid of the first observation because it is the same

#result.append(subset_df_t[['wait_time_average_normalized']], exog=subset_df_t[['open', ________]], refit=False, fit_kwargs=None)
#can change refit to True to refit the model

#denormalize after prediction
#pred1 = denormalize_data(prediction, mean_wt,std_wt)

#make the below 0s 0
#pred1 = pred1[pred1 < 0] = 0


"""
#simulation - Monte Carlo Simulation

import seaborn as sns



SARIMAX.simulate(params, nsimulations, measurement_shocks=None, state_shocks=None, initial_state=None, anchor=None, repetitions=None, exog=None, extend_model=None, extend_kwargs=None, transformed=True, includes_fixed=False, pretransformed_measurement_shocks=True, pretransformed_state_shocks=True, pretransformed_initial_state=True, random_state=None, **kwargs)
exog for adding the exogenous variables




#length = 20
#result.simulate(length, exog = subset_df_t[['open', _____]].tail(length), anchor = "end")

#end is determined from the train df, on which the model was trained - simulates into teh future


samples = []
length = 24
for sample in range(20): #specify number of simulations to run
    samples.append(result.simulate(length, exog = subset_df_t[['open', ________]].tail(length), anchor = "end"))
sns.lineplot(data=samples)


#save the average prediction to a df 
average_sim = sum(samples) / len(samples)
df_sim = pd.DataFrame({'average_sim': [average_sim]})

denormalize after simulation
df_sim['denormalized_sim'] = denormalize_data(df_sim['average_sim'], mean_wt,std_wt)

convert to 0 those below 0
df_sim['denormalized_sim']  = df_sim['denormalized_sim'] .apply(lambda x: x if x >= 0 else 0)

"""




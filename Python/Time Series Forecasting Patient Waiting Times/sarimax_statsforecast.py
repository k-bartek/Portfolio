

import pandas as pd
import numpy as np
import math
from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA
#new docu link here https://nixtla.github.io/statsforecast/src/core/models.html

#function for accuracy, if needed 
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


#function for denormalization
def denormalize_data(normalized_data, mean, std):
    denormalized_data = (normalized_data * std) + mean
    return denormalized_data


data = pd.read_csv('____.csv', parse_dates=['datetime'], index_col='datetime', header=0,sep=",")
#data = pd.read_csv('data_exo.csv', parse_dates=['datetime'], index_col='datetime', header=0,sep=",")
#for future exogenous values from intershift data (might be enriched by predicted numbr of calls)
#exogenous_df = _____

#normalization 
#number of calls
mean_c = data['number_of_calls_hr'].mean()
std_c = data['number_of_calls_hr'].std()
data['number_of_calls_hr_norm'] = (data['number_of_calls_hr'] - mean_c) / std_c

#number of shifts
____

#outcome
_______



#getting the data in the right shape
dataY = data['wait_time_average_normalized']

dataX = data[['open', 'Day_-1', 'Day_0', 'Day_1',
       'Day_2', 'Day_3', 'Day_4', 'Day_5', 'Day_6', _________]]
#add Number of Shifts_normalized optonal

dataY = data['wait_time_average_normalized']


dataY = pd.DataFrame(
    {
        'ds': dataY.index,
        'y': dataY.values,
    },
    index=pd.Index([0] * dataY.size, name='unique_id')
)
dataY['ds'] = pd.to_datetime(dataY['ds'])


dataX['unique_id'] = 1  # Adding the 'unique_id' column with value 0 for all observations

dataX['ds'] = pd.to_datetime(dataX.index) 

dataX.reset_index(drop=True, inplace=True)
dataY.reset_index(drop=True, inplace=True)

dataY['unique_id'] = 1


dataX = dataX[['unique_id','ds',________]]

dataX['unique_id'] = dataX.unique_id.astype(str)

dataY['unique_id'] = dataY.unique_id.astype(str)


dates = dataY['ds'].unique()
dtrain = dates[:-720] 
dtest = dates[-720:]

Y_train = dataY.query('ds in @dtrain')
Y_test = dataY.query('ds in @dtest') 

X_train = dataX.query('ds in @dtrain') 
X_test = dataX.query('ds in @dtest')



train = Y_train.merge(dataX, how = 'left', on = ['unique_id', 'ds']) 

models = [AutoARIMA(season_length = 24)]

sfx = StatsForecast(df = train,
    models=models, 
    freq='H')

#adjust horizon for prediction
horizon = 720 #in hours
level = [95]


#provide X (calendar values, number of shifts etc) instead of X_test, can be found in exogenous.csv
            #needs to be in the right shape - follow the preprocessing of dataX
fcst = sfx.forecast(df=train, h=horizon, X_df=X_test, level=level)
#fcst = sfx.forecast (y:numpy.ndarray, h:int, X:Optional[numpy.ndarray]=None,
                          #X_future:Optional[numpy.ndarray]=None,
                          #level:Optional[List[int]]=None,
                          #fitted:bool=False)

#for different horizons just change horizon and use this forecast to take the first elements in the horizon
#sfx.forecast(df=train, h=horizon, X_df=X_test[:horizon], level=level)

fcst = fcst.reset_index()
#denormalize the data
denorm_predictions = denormalize_data(fcst['AutoARIMA'],mean_wt,std_wt)


#accuracy
#res = Y_test.merge(fcst, how='left', on=['unique_id', 'ds'])
#res['denorm'] = denormalize_data(res['AutoARIMA'],mean_wt,std_wt)
#res['denorm_y'] = denormalize_data(res['y'],mean_wt,std_wt)
#forecast_accuracy(res['denorm']/60,res['denorm_y']/60)

##check model configuration with
fit_model = sfx.fit(train)

#sfx.fitted_ # access an array of fitted models.
#sfx.fitted_[0][0].model_


#get the parameters for statsmodels
aic = sfx.fitted_[0][0].model_['aic']
arma_order = sfx.fitted_[0][0].model_['arma']
coef = sfx.fitted_[0][0].model_['coef']

print("AIC:", aic)
print("ARMA order:", arma_order)
print("Coefficients:")
for key, value in coef.items():
    print(key, ":", value)
    
AR = arma_order[0]
MA = arma_order[1]
SAR = arma_order[2]
SMA = arma_order[3]
season_m = arma_order[4]
d = arma_order[5]
D = arma_order[6]

norm_order = (AR,d,MA)
season_order = (SAR, D, SMA, season_m)





##Append new data for prediction, data needs to come right after old data
#applies fitted SARIMAX model to a new time series


    #make sure the data follows right after the data used for training the model
#last_index_df1 = train.index.max()
#subset_df_t = df_t.loc[last_index_df1 + pd.Timedelta(days=0):] #subset based on last value of the train dataset
#subset_df_t = subset_df_t.resample('H').asfreq()
#subset_df_t = subset_df_t.drop(subset_df_t.index[0]) #get rid of the first observation because it is the same



#sfx.forward (y:numpy.ndarray, h:horizon,
#                         X:Optional[numpy.ndarray]=None,
#                         X_future:Optional[numpy.ndarray]=None,
#                         level:Optional[List[int]]=None,
#                         fitted:bool=False)





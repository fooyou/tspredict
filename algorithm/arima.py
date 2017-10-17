#!/usr/bin/env python
# coding: utf-8
# @File Name: arima.py
# @Author: Joshua Liu
# @Email: liuchaozhenyu@gmail.com
# @Create Date: 2017-10-16 17:10:33
# @Last Modified: 2017-10-17 17:10:06
# @Description:
#   ARIMA(p, d, q) 模型
#       d: 差分次数，使用"ADF单位根平稳型检测"，得到合适的 d 
#       p, q: 使用自相关图(acf)和偏自相关图(pacf)，选择 p, q 值
#          赤池信息量:   AIC = -2 ln(L) + 2 k
#          贝叶斯信息量: BIC = -2 ln(L) + ln(n) * k
#          汉南奎恩标准: HQ = -2 ln(L) + ln(ln(n)) * k
#   ARIMA 模型检验
#       - 自相关图和偏自相关图
#       - D-W 检验
#       - Ljung-Box 检验
#   ARIMA 模型预测

import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.stattools import acf, pacf

# lambda 函数，解析时间
dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m')

class ArimaModel():

    def __init__(self, filepath):
        self.data = pd.read_csv(filepath, parse_dates=['Month'], index_col='Month', date_parser=dateparse)
        self.ts = self.data['#Passengers']
        self.api_dict = {
            'acf': self.acf,
            'pacf': self.pacf,
        }


    def callback(self, api):
        return self.api_dict[api]()

    def acf(self):
        return acf(self.ts, nlags=20)


    def pacf(self):
        return pacf(self.ts, nlags=20)



# data = pd.read_csv('./data/AirPassengers.csv', parse_dates=['Month'],
#         index_col='Month', date_parser=dateparse)
# ts = data['#Passengers']
# 
# ts_log = np.log(ts)
# moving_avg = pd.Series.rolling(ts_log, 12).mean()
# ts_log_moving_avg_diff = ts_log - moving_avg
# expwighted_avg = pd.ewma(ts_log, halflife=12)
# ts_log_ewma_diff = ts_log - expwighted_avg
# ts_log_diff = ts_log - ts_log.shift()
# 
# 
# # Decomposition
# decomposition = seasonal_decompose(ts_log)
# 
# # ACF & PACF Plots
# lag_acf = acf(ts_log_diff, nlags=20)
# lag_pacf = pacf(ts_log_diff, nlags=20, method='ols')
# 
# # AR Model
# ar_model = ARIMA(ts_log, order=(2, 1, 0))
# results_AR = ar_model.fit(disp=-1)
# 
# # MA Model
# ma_model = ARIMA(ts_log, order=(0, 1, 2))
# results_MA = ma_model.fit(disp=-1)
# 
# # ARIMA Model
# arima_model = ARIMA(ts_log, order=(2, 1, 2))
# results_ARIMA = arima_model.fit(disp=-1)
# 
# # Convert to original scale
# predictions_ARIMA_diff = pd.Series(results_ARIMA.fittedvalues, copy=True)
# predictions_ARIMA_log = pd.Series(ts_log.ix[0], index=ts_log.index)
# predictions_ARIMA_log = predictions_ARIMA_log.add(predictions_ARIMA_diff.cumsum(), fill_value=0)
# predictions_ARIMA = np.exp(predictions_ARIMA_log)

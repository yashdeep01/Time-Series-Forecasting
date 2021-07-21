# Q1. Decomposing

library("forecast", lib.loc="/Library/Frameworks/R.framework/Versions/3.4/Resources/library")
library("readxl", lib.loc="/Library/Frameworks/R.framework/Versions/3.4/Resources/library")
air_temp = read_xlsx("~/Desktop/elnino.xlsx", skip = 0)
library(zoo)
air_temp_timeseries = ts(na.spline(air_temp$`Sea Surface Temp`), frequency = 365.25, start = c(1993,1,1))
air_temp_timeseries
plot.ts(air_temp_timeseries)

air_temp_timeseries
plot.ts(air_temp_timeseries)

air_temp_timeseries_comp = decompose(air_temp_timeseries)
plot(air_temp_timeseries_comp)
air_temp_timeseries_seasonallyadj = air_temp_timeseries - air_temp_timeseries_comp$seasonal
plot(air_temp_timeseries_seasonallyadj)

# Q2. Exponential Smoothing
# Additive model
# Seasonality present
# use holt-winters exp smoothing

my_forecast <- function(x){
  model <- HoltWinters(x)
  plot(model)
  return(model)
}

air_temp_timeseries_forecasts = my_forecast(ts(air_temp_timeseries, start=c(1993,1,1), end = c(1996,12,31), frequency = 365))
air_temp_timeseries_forecasts2 = forecast(air_temp_timeseries_forecasts, h=150)
plot(air_temp_timeseries_forecasts2$residuals)
plot(air_temp_timeseries_forecasts2)

Box.test(air_temp_timeseries_forecasts2$residuals, lag=20, type="Ljung-Box")

#Q3. a. Non-stationarity tests
library(tseries)
adf.test(air_temp_timeseries)
# stationary

pp.test(air_temp_timeseries)
kpss.test(air_temp_timeseries)
# non stationary

air_temp_timeseries_diff1 = diff(air_temp_timeseries, differences=1)

#b. ARIMA
air_temp_timeseries_arima = auto.arima(air_temp_timeseries)
summary(air_temp_timeseries_arima)

air_temp_timeseries_forecasts1 <- forecast(air_temp_timeseries_arima, h=150)
plot(air_temp_timeseries_forecasts1)
acf(air_temp_timeseries_forecasts1$residuals, lag.max=20)
Box.test(air_temp_timeseries_forecasts1$residuals, type="Ljung-Box")

plot(air_temp_timeseries_forecasts1$residuals)
hist(air_temp_timeseries_forecasts1$residuals)

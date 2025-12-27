import datetime

x = 'heartrate.npy'
data_type = x[:x.index('.')]
print(data_type)

time = 1766758709.317431
time = round(time)
print(datetime.datetime.fromtimestamp(time).strftime('%Y%m%d'))
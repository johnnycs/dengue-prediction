import pandas as pd

print "dengue weather"

def split_data(data):
    train_mask = (data.index < "2011")
    train = data[train_mask]
    test_mask = (data.index > "2011")
    test = data[test_mask]
    return train, test

def remove_space(province):
    if type(province) == str:
        return province.replace(" ", "")

def get_dengue_weather_by_province(province_for_dengue,
                                   province_for_weather,
                                   all_dengue,
                                   all_weather):
    
    all_weather.stn_name = all_weather.stn_name.apply(remove_space)
    province_weather = all_weather[all_weather.stn_name == province_for_weather]
    province_weather.index = pd.DatetimeIndex(province_weather.date)
    mask = (province_weather.index > "2003") & (province_weather.index < "2016")
    province_weather = province_weather[mask]
    
    all_dengue.index = pd.DatetimeIndex(all_dengue.date)
    all_dengue = all_dengue.drop(['date','date.1'],axis=1)
    province_dengues = all_dengue[all_dengue['province'] == province_for_dengue].resample('W').size()
    province_dengues_df = pd.DataFrame(province_dengues,columns=['cases'])
    
    province_avg_weather = province_weather[['avgrh','dday','meantemp']].resample('W').mean()
    province_avg_weather['rain'] = province_weather[['rain']].resample('W').sum() # cumulative rainfall
    province_dengues_weather = pd.concat([province_avg_weather,province_dengues_df[:-52]],axis=1)
    province_dengues_weather = province_dengues_weather.fillna(0)

    province_dengues_weather_split = split_data(province_dengues_weather)
    province_dengues_train, province_dengues_test = province_dengues_weather_split[0], province_dengues_weather_split[1]
    
    return province_dengues_train, province_dengues_weather
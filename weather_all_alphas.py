import numpy as np
from scipy.optimize import fmin, minimize
import weather_all_costs, ws_from_csv

print 'getting bounded alphas with params for avgrh...'

# train comes in the form of dataframe
def get_alphas(LAG, TEMPERATURE_WEEKS, RAIN_WEEKS, AVGRH_WEEKS, train, ws_csv = [], week_forward = 16):
    W_CASE = LAG + 1
    W_SEASON = 2
    W_TEMP = TEMPERATURE_WEEKS + 1
    W_RAIN = RAIN_WEEKS + 1
    W_AVGRH = AVGRH_WEEKS + 1
    W_WEATHER = W_TEMP + W_RAIN + W_AVGRH
    # BETAS_SET = W_TEMP + W_CASE + W_SEASON # addition of ALL_WS betas

    # use poison instead of least square
    def cost(w):
        start_week, end_cases_week, end_temp_week, end_rain_week, end_avgrh_week = 0, LAG, TEMPERATURE_WEEKS, RAIN_WEEKS, AVGRH_WEEKS
        predicted_line_offset = week_forward + end_cases_week - 1 # 41

        all_penalties = []
        for real_week in range(len(train)-predicted_line_offset):
            cases_for_prediction = train.cases[start_week:end_cases_week]
            temps_for_prediction = train.meantemp[start_week:end_temp_week]
            rains_for_prediction = train.rain[start_week:end_rain_week]
            avgrh_for_prediction = train.avgrh[start_week:end_avgrh_week]
            # print rains_for_prediction

            cur_penalty = weather_all_costs.nweek_ahead_cost(
                w,
                week_forward,
                start_week,
                end_cases_week,
                train,
                cases_for_prediction,
                temps_for_prediction,
                rains_for_prediction,
                avgrh_for_prediction)

            all_penalties.append(cur_penalty)
            start_week+=1
            end_cases_week+=1
            end_temp_week+=1
            end_rain_week+=1
            end_avgrh_week+=1

        return np.sum(all_penalties) / float(len(all_penalties))

    mean_val = 1/float(LAG)
    head_arr = np.array([mean_val]*W_CASE)
    seasonality_starters = [0.75,20] # [constant,phase]
    temperature_starters = [0.1]*(W_TEMP)
    rain_starters = [0.05]*(W_RAIN) # don't start at 0 for rain
    avgrh_starters = [0.1]*(W_AVGRH)

    arr = np.append(head_arr,seasonality_starters) #  lag + 1 + 2 betas
    temp_arr = np.append(arr,temperature_starters) # lag + 1 + 2 + 10 betas
    rain_arr = np.append(temp_arr,rain_starters) # lag + 1 + 2 + 10 + 7 betas
    all_arr = np.append(rain_arr,avgrh_starters)
    print len(all_arr)

    bnds = [(0.,None)]*W_CASE
    tail_bnds = [(None,None),(1.,None)]
    bnds.extend(tail_bnds)
    [bnds.extend([(None,None)]) for i in range(W_WEATHER)]
    print "LAG, TEMP, RAIN, AVGRH", LAG, TEMPERATURE_WEEKS, RAIN_WEEKS, AVGRH_WEEKS
    print 'bnds',LAG, len(bnds)

    myfactr = 1e2
    if len(ws_csv) < 1:
        print 'all_arr'
        w = minimize(cost, all_arr, bounds = bnds, options={'ftol' : myfactr * np.finfo(float).eps})
        # return w

    elif len(ws_csv) > 1:
        print 'ws_csv'

    w = minimize(cost, ws_csv, bounds = bnds, options={'ftol' : myfactr * np.finfo(float).eps})

    return w

print "done getting alphas ..."

import numpy as np
from scipy.optimize import fmin, minimize
import weather_costs

print 'getting bounded alphas ...'

# train comes in the form of dataframe
def get_alphas(LAG, TEMPERATURE_WEEKS, train, week_forward = 16):
    W_CASE = LAG + 1
    W_SEASON = 2
    W_TEMP = 10
    BETAS_SET = W_TEMP + W_CASE + W_SEASON # addition of ALL_WS betas

    # use poison instead of least square
    def cost(w):
        start_week, end_cases_week, end_temp_week = 0, LAG, TEMPERATURE_WEEKS
        predicted_line_offset = week_forward + end_cases_week - 1 # 41
        
        all_penalties = []
        for real_week in range(len(train)-predicted_line_offset):
            cases_for_prediction = train.cases[start_week:end_cases_week]
            temps_for_prediction = train.meantemp[start_week:end_temp_week]

            cur_penalty = weather_costs.nweek_ahead_cost(
                w, 
                week_forward, 
                start_week, 
                end_cases_week, 
                train, 
                cases_for_prediction,
                temps_for_prediction)

            all_penalties.append(cur_penalty)
            start_week+=1
            end_cases_week+=1
            end_temp_week+=1
            
        return np.sum(all_penalties) / float(len(all_penalties))

    head_arr = np.array([0.05]*W_CASE)
    seasonality_starters = [0.75,20] # [constant,phase]
    temperature_starters = [0.]*W_TEMP 

    arr = np.append(head_arr,seasonality_starters) #  lag + 1 + 2 betas
    all_arr = np.append(arr,temperature_starters) # lag + 1 + 2 + 2 betas
    bnds = [(0.,None)]*W_CASE
    tail_bnds = [(None,None),(1.,None)]
    bnds.extend(tail_bnds)
    [bnds.extend([(None,None)]) for i in range(W_TEMP)]
    print "bnds",len(bnds),bnds
    print "arr",len(all_arr),all_arr
    myfactr = 1e2
    w = minimize(cost,all_arr,bounds = bnds,options={'ftol' : myfactr * np.finfo(float).eps})
    return w

print "done getting alphas ..."
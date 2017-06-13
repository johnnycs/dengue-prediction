import numpy as np
from scipy.optimize import fmin, minimize
import weather_costs

print 'getting bounded alphas ...'

# train comes in the form of dataframe
def get_alphas(LAG, train, week_forward = 16):
    W_CASE = LAG + 1
    W_POP = 1
    W_SEASON = 2
    BETAS_SET = W_POP + W_CASE + W_SEASON # addition of ALL_WS betas

    # use poison instead of least square
    def cost(w):
        start_week,end_week = 0,LAG
        predicted_line_offset = week_forward + end_week - 1 # 41
        
        all_penalties = []
        for real_week in range(len(train)-predicted_line_offset):
            cases_for_pred = train.cases[start_week:end_week]

            cur_penalty = weather_costs.nweek_ahead_cost(
                w, 
                week_forward, 
                start_week, 
                end_week, 
                train, 
                cases_for_pred)

            all_penalties.append(cur_penalty)
            start_week+=1
            end_week+=1
            
        return np.sum(all_penalties) / float(len(all_penalties))

    seasonality_starters = [0.75,20] # [constant,phase]
    temperature_starters = [0.,0.]
    head_arr = np.array([0.05]*W_CASE) 
    arr = np.append(head_arr,seasonality_starters) #  lag + 1 + 2 betas
    all_arr = np.append(arr,temperature_starters) # lag + 1 + 2 + 2 betas
    bnds = [(0.,None)]*W_CASE
    tail_bnds = [(None.,None),(None,None),(0.,None),(None,None)]
    bnds.extend(tail_bnds)
    # print "bnds",len(bnds),bnds
    # print "arr",len(arr),arr
    w = minimize(cost,all_arr,bounds = bnds)
    return w

print "done getting alphas ..."
import numpy as np
from scipy.optimize import fmin, minimize
import weighted_costs

print 'getting bounded alphas ...'

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
            cases_for_pred = train[start_week:end_week]
            cur_penalty = weighted_costs.nweek_ahead_cost(
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
    arr = np.array([0.05]*W_CASE) #  27 betas
    arr = np.append(arr,seasonality_starters) # 29 betas
    #bnds = [(-2.14e-6,0.8)]*W_CASE
    bnds = [(-1.0,1.0)]*W_CASE
    bnds = bnds.append((0.0,30.0))
    w = minimize(cost,arr,bounds = bnds)
    return w

print "done getting alphas ..."
import numpy as np
from scipy.optimize import fmin, minimize
import costs

print 'getting alphas ...'

def get_alphas(LAG, train, week_forward = 16):
    W_CASE = LAG + 1
    W_POP = 1
    W_SEASON = 2
    BETAS_SET = W_POP + W_CASE + W_SEASON # addition of ALL_WS betas

    # use poison instead of least square
    def cost(w):
        start_week,end_week = 0,LAG
        predicted_line_offset = week_forward + end_week - 1

        all_penalties = []
        for real_week in range(len(train)-predicted_line_offset):
            cases_for_pred = train[start_week:end_week]
            cur_penalty = costs.nweek_ahead_cost(w, week_forward, start_week, end_week, train, cases_for_pred)
            all_penalties.append(cur_penalty)
            start_week+=1
            end_week+=1

        return np.sum(all_penalties) / float(len(all_penalties))

    # seasonality_starters = [0.75,20] # [constant,phase]
    # arr = np.array([0.05]*W_CASE) #  27 betas
    # arr = np.append(arr,seasonality_starters) # 29 betas

    bnds = [(0.,None)]*W_CASE
    tail_bnds = [(None,None),(1.,None)]
    bnds.extend(tail_bnds)
    # w = minimize(cost,arr)

    arr = [6.49449041e-01,  -5.78203433e-09,  -7.65191141e-09,
        -5.54996757e-09,  -5.22802065e-09,  -7.20315375e-09,
        -1.50623385e-08,  -7.30523211e-09,  -5.81808115e-09,
        -1.59275580e-08,  -2.78562559e-08,  -2.56935169e-08,
        -3.44347331e-08,   1.39206973e-07,   7.10788802e-02,
        -4.16707175e-07,  -3.58686498e-07,  -5.43876179e-07,
         9.67994192e-02,   1.59664830e-01,  -2.13872978e-06,
        -5.54658889e-07,  -1.33777980e-07,  -3.04532977e-08,
        -6.02759551e-08,  -1.40581707e-07,   7.44264376e-01,
        -2.88676959e-07,   2.12438461e+01]

    myfactr = 1e2
    w = minimize(cost, arr, bounds = bnds, options={'ftol' : myfactr * np.finfo(float).eps})
    return w

print "done getting alphas ..."

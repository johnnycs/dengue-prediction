def guess(w, x_week, y_case):
    
    def omega(w, y_case):
        pad_y = np.concatenate(([1],np.array(y_case)))
        all_cases = np.dot(w[:-2],pad_y)
        return all_cases

    # there's no amplitude in the season since the omega is absorbed in the above f'n
    def season_cos_sq(w, x_week):
        pi = np.math.pi
        coeff = pi/52.
        shift_phase = w[-1]
        inside = coeff*(x_week - shift_phase)
        cosine_sq = np.math.cos(inside)**2
        c = w[-2]
        score = cosine_sq + c
        return score    

#     def season_sin(w,x_week):
#         coeff = np.math.pi / 52.
#         inside = coeff*(x_week - w[-2])
#         score = np.math.sin(inside) + w[-3]
#         return score
    
    return omega(w,y_case) * season_cos_sq(w,x_week)

def get_alphas(LAG, train, week_forward_for_cost=52):
    W_CASE = LAG + 1
    W_POP = 1
    W_SEASON = 2
    BETAS_SET = W_POP + W_CASE + W_SEASON # addition of ALL_WS betas

    # use poison instead of least square
    def cost(w):
        
#         ret = 0
#         for week_no in range(len(train)-LAG):
#             week_to_predict = week_no+LAG 
#             real_case = train[week_to_predict] + 1 # avoid getting zeros
#             predicted_case = guess(w,week_to_predict,train[week_no:week_to_predict]) # w, 26 (since we start 0-25)
#             sigma_sq = real_case + 1 # assume poisson and avoid division by zero
#             ret += ((real_case - predicted_case)**2)/float(sigma_sq)
#         return ret

        # week_forward_for_cost = 5
        week_forward = range(1,week_forward_for_cost+1)
        rets = []
        for ifuture in week_forward:
            future_week = ifuture + LAGG - 1
            ret = 0
            for aweek in range(len(train)-future_week):
                week_to_predict = aweek+LAG 
                real_case = train[week_to_predict] + 1 # avoid getting zeros
                predicted_case = guess(w, week_to_predict, train[aweek:week_to_predict]) # w, 26 (since we start 0-25)
                sigma_sq = real_case + 1 # assume poisson and avoid division by zero
                ret += ((real_case - predicted_case)**2)/float(sigma_sq)
            rets.append(ret)
        return np.sum(rets)/float(week_to_predict+1)

    seasonality_starters = [0.75,20] # [constant,phase]
    arr = np.array([0.]*W_CASE) #  27 betas
    arr = np.append(arr,seasonality_starters) # 29 betas
    w = minimize(cost,arr)
    return w

# get_alphas(26,cm_dengues_train,-9.26e-01)
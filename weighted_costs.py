import model
import numpy as np

print "getting cost from nweek ahead"

def nweek_ahead_cost(ws, week_forward ,start_week, end_week, data, cases_for_pred):
    
#     print end_week
    weight = np.linspace(1,2,week_forward)
    ret = 0
    for aweek in range(week_forward): # 14 loops; when you want to predict 14 weeks ahead
        week_to_predict = aweek+end_week
        real_case = data[aweek+end_week] +1 # avoid getting zeros
#         print 'wtp',week_to_predict
#         print cases_for_pred
#         print cases_for_pred
#         print "real",real_case
#         print len(cases_for_pred), week_to_predict
        predicted_case = model.guess(
          ws, 
          week_to_predict, 
          cases_for_pred)

        cur_weight = weight[aweek]
        weighted_predicted_case = cur_weight * predicted_case
        cases_for_pred = np.append(cases_for_pred[1:],weighted_predicted_case)
        sigma_sq = real_case + 1
        ret += ((real_case - weighted_predicted_case)**2)/float(sigma_sq)
    return ret
    
# data = range(1,100)
# start_week,end_week = 0,26
# week_forward = 16

# all_penalties = []
# for real_week in range(len(data)-(week_forward+end_week-1)):
#     cases_for_pred = data[start_week:end_week]
# #     print 'fw',future_week

#     cur_penalty = nweek_ahead_cost(cm_26.x, week_forward, start_week, end_week, data, cases_for_pred)
#     all_penalties.append(cur_penalty)
        
#     start_week+=1
#     end_week+=1

# all_penalties
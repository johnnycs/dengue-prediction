import model_01
import numpy as np

print "getting cost from nweek ahead"

def nweek_ahead_cost(
        ws,
        week_forward,
        start_week,
        end_cases_week,
        data,
        cases_for_prediction,
        temps_for_prediction,
        rains_for_prediction,
        hmids_for_prediction):

#   print end_cases_week
    ret = 0
    for aweek in range(week_forward): # 16 loops; when you want to predict 14 weeks ahead
        week_to_predict = aweek+end_cases_week
        real_case = data.cases[aweek+end_cases_week] +1 # avoid getting zeros
#         print 'wtp',week_to_predict
#         print cases_for_prediction
#         print cases_for_prediction
#         print "real",real_case
#         print len(cases_for_prediction), week_to_predict
        predicted_case = model_01.guess(
          ws,
          week_to_predict,
          cases_for_prediction,
          temps_for_prediction,
          rains_for_prediction,
          hmids_for_prediction)

        cases_for_prediction = np.append(cases_for_prediction[1:],predicted_case)
        sigma_sq = real_case + 1

        # if aweek == week_forward - 1:
        #   ret += ((real_case - predicted_case)**2)/float(sigma_sq)
        ret += ((real_case - predicted_case)**2)/float(sigma_sq)

    return ret

# data = range(1,100)
# start_week,end_cases_week = 0,26
# week_forward = 16

# all_penalties = []
# for real_week in range(len(data)-(week_forward+end_cases_week-1)):
#     cases_for_prediction = data[start_week:end_cases_week]
# #     print 'fw',future_week

#     cur_penalty = nweek_ahead_cost(cm_26.x, week_forward, start_week, end_cases_week, data, cases_for_prediction)
#     all_penalties.append(cur_penalty)

#     start_week+=1
#     end_cases_week+=1

# all_penalties

import model_02
import numpy as np

print "getting cost from nweek ahead: humidity"

def nweek_ahead_cost(
        ws,
        week_forward,
        start_week,
        end_cases_week,
        data,
        cases_for_prediction,
        temps_for_prediction,
        rains_for_prediction,
        avgrh_for_prediction):

    ret = 0
    for aweek in range(week_forward): # 14 loops; when you want to predict 14 weeks ahead
        week_to_predict = aweek+end_cases_week
        real_case = data.cases[aweek+end_cases_week] +1 # avoid getting zeros
        predicted_case = model_02.guess(
          ws,
          week_to_predict,
          cases_for_prediction,
          temps_for_prediction,
          rains_for_prediction,
          avgrh_for_prediction)

        cases_for_prediction = np.append(cases_for_prediction[1:],predicted_case)
        sigma_sq = real_case + 1

        # if aweek == week_forward - 1:
        #   ret += ((real_case - predicted_case)**2)/float(sigma_sq)
        ret += ((real_case - predicted_case)**2)/float(sigma_sq)

    return ret

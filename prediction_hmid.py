import numpy as np
import model_01

def get_predictions(LAG, TEMPERATURE_WEEKS, RAIN_WEEKS, HUMID_WEEKS, real, ws, province = "", nweeks_to_predict=[1,2,4,8,16]):

    def n_week_ahead(cases_for_prediction, temps_for_prediction,
                     rains_for_prediction, hmids_for_prediction,
                     weeks_ahead, case_week_to_predict):

        cur_prediction = 0
        prev_cases = np.array(cases_for_prediction.cases)
        for i in range(weeks_ahead):
            week_to_predict = case_week_to_predict + i
#             print week_to_predict
#             print case_week_to_predict + i
#             print case_week_to_predict
#             mean_temp = real.meantemp[]
            cur_prediction = model_01.guess(
                ws,
                week_to_predict,
                prev_cases,
                temps_for_prediction,
                rains_for_prediction,
                hmids_for_prediction)
            prev_cases = np.append(prev_cases[1:],cur_prediction) # deduct the first elm out
        return cur_prediction

    all_predictions = []
    for nweek in nweeks_to_predict: # 1,2,4,8,16
        predictions = []
        for start_week in range(len(real)-(LAG)):
            case_week_to_predict = start_week + LAG
            cases_for_prediction = real[start_week:case_week_to_predict]

            temp_week_to_predict = start_week+TEMPERATURE_WEEKS
            temps_for_prediction = real.meantemp[start_week:temp_week_to_predict]

            rain_week_to_predict = start_week+RAIN_WEEKS
            rains_for_prediction = real.meantemp[start_week:rain_week_to_predict]

            hmid_week_to_predict = start_week+HUMID_WEEKS
            hmids_for_prediction = real.avgrh[start_week:hmid_week_to_predict]

            prediction = n_week_ahead(
                cases_for_prediction,
                temps_for_prediction,
                rains_for_prediction,
                hmids_for_prediction,
                nweek,
                case_week_to_predict)
            predictions.append(prediction)
        all_predictions.append(predictions)
    return all_predictions

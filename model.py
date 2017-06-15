import numpy as np

print "running model"

def guess(all_ws, nth_week, cases_for_prediction, temps_for_prediction):

    n_omega = 17 # lag + 1
    n_season = 2
    n_temp = 10 # 9 weeks temp + 1
    # n_rain = 
    # n_humid = 
    
    def omega(w_omega, cases_for_prediction):
        pad_y = np.concatenate(([1], np.array(cases_for_prediction)))
        weights = np.array(w_omega)
        positive_weights = weights**2 # force the weights to be positive
        all_cases = np.dot(positive_weights,pad_y)
        return all_cases

    # there's no amplitude in the season since the omega is absorbed in the above f'n
    def season_sin(w_season, nth_week):
        pi = np.math.pi
        coeff = pi/26.
        shift_phase = w_season[1]
        inside = coeff*(nth_week - shift_phase)
        sine = np.math.sin(inside)
        c_sq = w_season[0]**2
        score = 1 + c_sq + sine # avoid going to negative
        return score    

    def temperature_term(w_temp, temps_for_prediction):
        # print "len temps_for_prediction",len(temps_for_prediction)
        pad_y = np.concatenate(([1], np.array(temps_for_prediction)))
        # print "len py",len(pad_y)
        # print "py",pad_y
        # print "w",len(w_temp)
        weights = np.array(w_temp)
        all_temps = np.dot(weights,pad_y)
        return all_temps

    def rain_term(w, rain):
        return

    def humidity_term(w, humidity):
        return
    
    w_omega = all_ws[:n_omega]
    # print "omega",w_omega
    omega = omega(w_omega, cases_for_prediction) # takes the first part of w

    w_season = all_ws[n_omega:n_omega+n_season]
    # print "season",w_season
    seasonality_part = season_sin(w_season, nth_week) # takes the second part of w

    w_temp = all_ws[n_omega+n_season:]
    # print "temps_for_prediction",temps_for_prediction
    temperature_part = temperature_term(w_temp, temps_for_prediction) # takes the third part of w

    # rain_part = rain_term(w, rain)
    # humidity_part = humidity_term(w, humidity)

    return omega * seasonality_part * temperature_part






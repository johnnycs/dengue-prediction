import numpy as np

print "running model"

def guess(w, nth_week, cases_for_prediction):
    
    def omega(w, cases_for_prediction):
        pad_y = np.concatenate(([1], np.array(cases_for_prediction)))
        weights = np.array(w[:-4])
        positive_weights = weights**2 # force the weights to be positive
        all_cases = np.dot(positive_weights,pad_y)
        return all_cases

    # there's no amplitude in the season since the omega is absorbed in the above f'n
    def season_sin(w, nth_week):
        pi = np.math.pi
        coeff = pi/26.
        shift_phase = w[-3]
        inside = coeff*(nth_week - shift_phase)
        sine = np.math.sin(inside)
        c_sq = w[-4]**2
        score = 1 + c_sq + sine # avoid going to negative
        return score    

    
    return omega(w,cases_for_prediction) * season_sin(w,nth_week)

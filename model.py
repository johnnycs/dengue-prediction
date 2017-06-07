import numpy as np

print "running model"

def guess(w, nth_week, cases_for_prediction):
    
    def omega(w, cases_for_prediction):
        pad_y = np.concatenate(([1],np.array(cases_for_prediction)))
        all_cases = np.dot(w[:-2],pad_y)
        return all_cases

    # there's no amplitude in the season since the omega is absorbed in the above f'n
    def season_cos_sq(w, nth_week):
        pi = np.math.pi
        coeff = pi/52.
        shift_phase = w[-1]
        inside = coeff*(nth_week - shift_phase)
        cosine_sq = np.math.cos(inside)**2
        c = w[-2]
        score = cosine_sq + c
        return score    

#     def season_sin(w,nth_week):
#         coeff = np.math.pi / 52.
#         inside = coeff*(nth_week - w[-2])
#         score = np.math.sin(inside) + w[-3]
#         return score
    
    return omega(w,cases_for_prediction) * season_cos_sq(w,nth_week)

import numpy as np

def get_validations(LAG, all_predictions, real):

    def validation(prediction, real):
        residual_sq = (real - prediction)**2
        real = np.array(real)
        sigma = np.mean(real)**0.5
        score = residual_sq / float(sigma)
        return sum(score) / len(real)

    weeks = [1,2,4,8,16]
    ret = []
    for idx,prediction in enumerate(all_predictions):
        cur_pred = np.array(prediction)
        # compare with real
        # doesnt take into the accout of the predicted week(s)
        cur_pred_range = cur_pred[:-weeks[idx]]
        real_range = real.cases[LAG+weeks[idx]:]
        ret.append(validation(cur_pred_range,real_range))

    return ret

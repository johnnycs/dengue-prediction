def ws_helper(LAG, ws):
    n_ws = len(ws)
    if LAG == n_ws:
        arr = ws
    elif LAG < n_ws:
        arr = ws[:-(n_ws - LAG)]
    else:
        tail = LAG - n_ws
        mean_val = 1/(float(LAG)*tail)
        arr = np.append(ws,[mean_val]*tail)
    return arr

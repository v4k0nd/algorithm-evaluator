import pandas as pd

def create_roc_label(x_conf: list, threshold: float = 0.5) -> list:
    """Creates labels (0 or 1) from confidence values (0.0 to 1.0) based on the threshold value.

    Parameters
    ----------
    x_conf (list): list of confidence values
    threshold (float, optional): threshold number to cut off at. Defaults to 0.5.

    Returns
    -------
    list: list of label values
    
    Examples
    --------
    
    >>> x_conf = [0.32, 0.81, 0.45, 0.5]
    >>> print(create_roc_label(x_conf, 0.5))
    .. output ::
        [0, 1, 0, 1]
    """    
    X_label = [1 if c >= threshold else 0 for c in x_conf]
    return X_label

def conf_matrix_to_list(tn, fn, fp, tp) -> list:
    return [str(tn),  str(fn), str(fp), str(tp)]

def table_setup(tn, fn, fp, tp) -> pd.DataFrame:
    _data = [[str(tn),  str(fn)], [str(fp), str(tp)]]
    return pd.DataFrame(data=_data, index=['predicted 0', 'predicted 1'], columns=['actual 0', 'actual 1'])

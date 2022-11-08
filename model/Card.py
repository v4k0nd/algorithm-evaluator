from sklearn.metrics import RocCurveDisplay
import pandas as pd

class Card:
    tn: int 
    fp: int
    fn: int
    tp: int
    f1: float
    fig: RocCurveDisplay
    
    # def __init__(self, conf_matix: list, f1: float):
    #     self.tn, self.fp, self.fn, self.tp = conf_matix
    #     self.f1 = f1
        
    def __init__(self, fig: RocCurveDisplay, tn: int, fp: int, fn: int, tp: int, f1: float):
        self.fig = fig
        self.tn, self.fp, self.fn, self.tp = tn, fp, fn, tp
        self.f1 = f1
        
    def set_fig(self, fig: RocCurveDisplay):
        self.fig = fig
    
    def set_conf_matrix_list(self, tn: int, fp: int, fn: int, tp: int):
        self.tn, self.fp, self.fn, self.tp = tn, fp, fn, tp
    
    def set_f1(self, f1: float):
        self.f1 = f1
    
    def get_conf_matrix_list(self):
        return list([str(self.tn), str(self.tp), str(self.fn), str(self.fp)])
    
    def get_conf_matrix_pd(self,) -> pd.DataFrame:
        return pd.DataFrame(data=[[str(self.tn),  str(self.fn)], [str(self.fp), str(self.tp)]], index=['predicted 0', 'predicted 1'], columns=['actual 0', 'actual 1'])
    
    def get_f1(self) -> float:
        return round(self.f1,2)
    
    def get_fig(self) -> RocCurveDisplay:
        return self.fig
    
# class CardMultiGraph(Card):
    
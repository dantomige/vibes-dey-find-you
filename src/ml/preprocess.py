import pandas as pd

class MusicPreprocessor:

    def __init__(self):
        raise NotImplementedError

    def load_data(self) -> pd.DataFrame:
        raise NotImplementedError
    
    def transform_data(self, df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError("Should return ml features")
    
    def save_feature(self, df: pd.DataFrame):
        raise NotImplementedError
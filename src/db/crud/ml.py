from src.schemas.audio_features import AudioFeatures

class FeatureRepository:

    def __init__(self, db):
        self.db = db
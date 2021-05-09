from google.cloud import firestore
from models.chain import Chain


class HandleCalculate:
    def __init__(self):
        self.db = firestore.Client()

    def calculate_overall_growth(self, chain: Chain):
        return NotImplemented

    def calculate_fast_growth(self, chain: Chain):
        return NotImplemented

    def calculate_drip_growth(self, chain: Chain):
        return NotImplemented

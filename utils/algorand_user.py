from utils import Algorand


class AlgorandUser():
    
    def __init__(self, private_key):
        self.private_key = private_key
        self.address = self._get_address()
    
    def _get_address(self):
        return Algorand.get_address_from_private_key(self.private_key)
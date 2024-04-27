class ApiException(Exception):
    
    def __init__(self, error_code, args):
        self.error_code = error_code
        self.data = args
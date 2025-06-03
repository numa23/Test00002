from lib import Singleton

class Cloud(Singleton):
    def __init__(self):
        if not hasattr(self, 'log_path_name'):
            self.log_path_name = ''
            self.is_disp = False
        if not hasattr(self, 'dict'):
            self.dict = {}

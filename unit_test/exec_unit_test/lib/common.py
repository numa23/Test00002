class Common:
    def __init__(self) -> None:
        self.is_trace = False
        self.is_disp = False
    def trace(self, data):
        if not self.is_trace:
            return
        print(f'TRACE:{data}')

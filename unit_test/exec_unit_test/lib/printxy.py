from lib import Cloud

def print_(log_text, end='\n', mode='a', is_disp=True):
    print(log_text, end=end) if is_disp else 'pass'
    log_path_name = Cloud.log_path_name
    if log_path_name == '':
        return
    with open(log_path_name, mode, encoding='utf-8') as f:
        print(log_text, end=end, file=f)

def printx(log_text, end='\n', mode='a'):
    print_(log_text, end=end, mode=mode, is_disp=Cloud.is_disp)

def printy(log_text, end='\n', mode='a'):
    print_(log_text, end=end, mode=mode)

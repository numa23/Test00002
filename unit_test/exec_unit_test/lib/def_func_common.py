import os
import sys
import datetime as dt
import time
import yaml
import subprocess
import shutil
from lib.def_func_ros import *
if os.name == 'nt':
    from lib.def_func_ros_sim import *
else:
    from lib.def_func_ros_py import *
from lib import Cloud

funcs = []

def func_regist(genv):
    global funcs
    funcs += get_funcs_ros()
    if os.name == 'nt':
        funcs += get_funcs_ros_sim()
    else:
        funcs += get_funcs_ros_py()
    [func_regist_helper(genv, func) for func in funcs]

def func_regist_helper(genv, func_name):
    genv[func_name] = ['func_in', func_name]

funcs += ['get_os_name']
def get_os_name():
    # win:'nt',ubuntu:'posix'
    return os.name

funcs += ['exit']
def exit():
    sys.exit()

funcs += ['range2']
def range2(num):
    return [x for x in range(num)]

funcs += ['factorial']
def factorial(n):
    result = 1
    for value in range(1, n + 1):
        result *= value
    return result

funcs += ['permutation']
def permutation(n, r):
    result = 1
    index = 1
    for value in range(n, 1, -1):
        result *= value
        if r == index:
            break
        index += 1
    return result

funcs += ['combination']
def combination(n, r):
    result = permutation(n, r)
    result //= factorial(r)
    return result

funcs += ['now']
def now(mode):
    if mode == 99:     # '?'
        doc = ''
        doc += '-' * 30 + '\n'
        doc += '[now(mode=0)]\n'
        doc += 'Get now info.\n'
        doc += 'mode:desc\n'
        doc += '0:YYYYMMDDhhmmss\n'
        doc += '1:[Y,M,D,h,m,s,f]\n'
        doc += 'else:YYYY,MM,DD,hh,mm,ss,f\n'
        doc += '-' * 30 + '\n'
        print(doc)
        return 
    now = dt.datetime.now()
    if mode == 0:
        result = now.strftime('%Y%m%d%H%M%S')
    elif mode == 1:
        now_str = now.strftime('%Y,%m,%d,%H,%M,%S,%f')
        result = now_str.split(',')
        result = [int(x) for x in result]
    else:
        result = now.strftime('%Y,%m,%d,%H,%M,%S,%f')
    return result

funcs += ['getcwd']
def getcwd():
    return os.getcwd().replace('\\', '/')

funcs += ['chdir']
def chdir(path):
    os.chdir(path)

funcs += ['path_join']
def path_join(path, file):
    return os.path.join(path, file)

funcs += ['isfile']
def isfile(path):
    is_file = os.path.isfile(path)
    return is_file

funcs += ['isdir']
def isdir(path):
    is_dir = os.path.isdir(path)
    return is_dir

funcs += ['mkdir']
def mkdir(path):
    os.makedirs(path, exist_ok=True)

funcs += ['remove_file']
def remove_file(src):
    try:
        os.remove(src)
    except Exception as ex:
        print(str(ex))

funcs += ['copy_file']
def copy_file(src, dst):
    if not os.path.exists(src):
        print('not exist file:' + src)
        return
    shutil.copy2(src, dst)
    #print(f'copy file:{src} -> {dst}')

funcs += ['move_file']
def move_file(src, dst):
    if not os.path.exists(src):
        print('not exist file:' + src)
        return
    os.rename(src, dst)
    #print(f'rename file:{src} -> {dst}')

funcs += ['copy_dir']
def copy_dir(src, dst):
    shutil.copytree(src, dst)

funcs += ['read_text']
def read_text(file):
    with open(file, encoding='utf-8') as f:
        text = f.read()
    return text

funcs += ['write_text']
def write_text(file, text):
    mkdir(os.path.dirname(file))
    with open(file, 'w', encoding='utf-8') as f:
        f.write(text)

#funcs += ['write_list']
#def write_list(file, list):
#    mkdir(os.path.dirname(file))
#    with open(file, 'w', encoding='utf-8') as f:
#        [f.write(f'{line}\n') for line in list]

funcs += ['read_yaml']
def read_yaml(file):
    with open(file, encoding='utf-8') as yml:
        dict = yaml.safe_load(yml)
    return dict

funcs += ['write_yaml']
def write_yaml(file, dict):
    with open(file, 'w', encoding='utf-8') as yml:
        yaml.safe_dump(dict, yml, default_flow_style=False, allow_unicode=True, sort_keys=False)

funcs += ['write_sort_yaml']
def write_sort_yaml(file, dict):
    with open(file, 'w', encoding='utf-8') as yml:
        yaml.dump(dict, yml, default_flow_style=False, allow_unicode=True, sort_keys=True)

funcs += ['cmp_file_time_stamp']
def cmp_file_time_stamp(src, dst):
    if not os.path.exists(src):
        return -1
    if not os.path.exists(dst):
        return -2
    if os.path.getmtime(src) == os.path.getmtime(dst):
        return 0
    if os.path.getmtime(src) < os.path.getmtime(dst):
        return 1
    return 2

funcs += ['zfill']
def zfill(num, len):
    return str(num).zfill(len)

funcs += ['rjust']
def rjust(string, len, char):
    return str(string).rjust(len, char)

funcs += ['center']
def center(string, len, char):
    return str(string).center(len, char)

funcs += ['ljust']
def ljust(string, len, char):
    return str(string).ljust(len, char)

funcs += ['randint']
def randint(s, e):
    import random
    return random.randint(s, e)

funcs += ['random']
def random():
    import random
    return random.random()

funcs += ['split']
def split(text, key):
    return text.split(key)

funcs += ['trim']
def trim(text):
    return text.strip()

funcs += ['replace']
def replace(text, old, new):
    return text.replace(old, new)

funcs += ['substr']
def substr(text, s, e):
    return text[s:e]

funcs += ['isnumeric']
def isnumeric(text):
    return str(text).replace('.', '').isnumeric()

funcs += ['disp_main_title']
def disp_main_title(text):
    print('=' * (len(text.encode('shift-jis')) + 2))
    print(f' {text}')
    print('=' * (len(text.encode('shift-jis')) + 2))

funcs += ['disp_sub_title']
def disp_sub_title(text):
    print('-' * (len(text.encode('shift-jis')) + 2))
    print(f' {text}')
    print('-' * (len(text.encode('shift-jis')) + 2))

funcs += ['disp_item']
def disp_item(text, mode=None):
    mode = 0 if mode == None else mode if mode <= 3 else 0
    type_dict = {0: ('(', ')'), 1: ('[', ']'), 2: ('{', '}'), 3: ('<', '>'), }
    type = type_dict[mode]
    print(f'{type[0]}{text}{type[1]}')

funcs += ['disp_item2']
def disp_item2(text, type=None):
    type = ('(', ')') if type == None else (type, type)
    print(f'{type[0]} {text} {type[1]}')

funcs += ['disp_item3']
def disp_item3(text, count=None):
    count = 4 if count == None else count
    type = '#' * count
    print(f'{type} {text} {type}')

funcs += ['disp_line']
def disp_line(mark, count=None):
    count = 80 if count == None else count
    print(mark * count)

funcs += ['exec']
def exec(cmd_line):
    ps = subprocess.run(cmd_line, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, text=True)
    return ps.stdout.splitlines()

funcs += ['exec2']
def exec2(cmd_line):
    #printx('exec2:' + cmd_line) if quiet == False else do_nothing()
    ps = subprocess.Popen(cmd_line, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    return ps

funcs += ['wait_start_ps']
def wait_start_ps(ps_list):     # for ubuntu
    for ps in ps_list:
        ps_wait = exec(f'pgrep -l {ps}')
        if ps not in ps_wait.stdout:
            return False
    return True

funcs += ['sleep']
def sleep(sec):
    time.sleep(sec)

funcs += ['save']
def save(key, value):
    cloud = Cloud()
    cloud.dict[key] = value

funcs += ['load']
def load(key):
    cloud = Cloud()
    return cloud.dict.get(key)

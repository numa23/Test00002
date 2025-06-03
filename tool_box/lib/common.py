import os
import subprocess
import shutil

def get_list(file_name):
    text_list = []
    with open(file_name, encoding='utf-8') as f:
        text_list = [s.rstrip() for s in f.readlines()]
    return text_list
def put_list(file_name, list_all):
    with open(file_name, mode='w', encoding='utf-8') as f:
        f.writelines([f'{s}\n' for idx, s in enumerate(list_all, start=1)])
def exec(cmd_line):
    ps = subprocess.run(cmd_line, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, text=True)
def mkdir(path):
    os.makedirs(path, exist_ok=True)
def remove_file(src):
    try:
        os.remove(src)
    except Exception as ex:
        print(str(ex))
def copy_file(src, dst):
    if not os.path.exists(src):
        print('not exist file:' + src)
        return
    shutil.copy2(src, dst)
    print(f'copy file:{src} -> {dst}')
def move_file(src, dst):
    if not os.path.exists(src):
        print('not exist file:' + src)
        return
    os.rename(src, dst)
    print(f'rename file:{src} -> {dst}')
def copy_dir(src, dst):
    shutil.copytree(src, dst)

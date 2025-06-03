import os
import pyperclip
from tkinter import messagebox

svn_path = os.getcwd().replace(r'\tool_box', '')
if os.path.exists(os.path.join(svn_path, 'ヒヤリハット_relate_table.xlsm')):
    pyperclip.copy(f"svn_path: {svn_path}")
else:
    msg = 'svn配下の(00_exec_at_svn.py)を実行してね!!'
    print(msg)
    messagebox.showwarning('警告', msg)

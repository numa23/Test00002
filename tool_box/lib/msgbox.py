import tkinter as tk
import tkinter.ttk as ttk
import os
import sys
from lib.singleton import Singleton
from enum import Enum

class EnumMode(Enum):
    QUESTION = 0
    INFORMATION = 1
    WARNING = 2
    ERROR = 3
    PROGRESS = 4
    SPLASH = 5
    ERRORRETRY = 6

class MainFrame(tk.Frame):
    mycls = None
    def __init__(self, parent=None, message=None, mode=None, topmost=True):
        master = tk.Toplevel()
        super().__init__(master)
        MainFrame.mycls = self
        self.master.wm_overrideredirect(True)
        self.master.configure(relief='raised', bd=3) 
        self.master.attributes('-toolwindow', True)
        self.master.attributes('-topmost', topmost)
        self.master.protocol('WM_DELETE_WINDOW', (lambda: 'pass')())
        self.have_button = mode not in [EnumMode.PROGRESS, EnumMode.SPLASH]
        self.have_one_button = mode in [EnumMode.INFORMATION, EnumMode.WARNING, EnumMode.ERROR]
        self.have_two_button = mode in [EnumMode.QUESTION, EnumMode.ERRORRETRY]
        self.widht, self.height = 350, 150 if self.have_button else 120
        self.master.geometry(self.get_my_geometry(parent.geometry(), f'{self.widht}x{self.height}'))
        self.master.minsize(self.widht, self.height)
        self.master.maxsize(self.widht + 200, self.height + 200)
        self.master.grab_set()
        self.frame_icon = tk.Frame(self.master)
        self.frame_message = tk.Frame(self.master)
        self.frame_button = tk.Frame(self.master)
        self.canvas = tk.Canvas(self.frame_icon, height=48, width=48)
        self.message = tk.StringVar()
        self.message.set(message)
        self.label_right = tk.Label(self.frame_message, textvariable=self.message, anchor=tk.NW, justify=tk.LEFT)
        self.button_right = tk.Button(self.frame_button, text='YES', width=10, height=2, background='PaleGreen', command=self.on_btn_yes)
        self.button_right2 = tk.Button(self.frame_button, text='NO', width=10, height=2, background='pink', command=self.on_btn_no)
        self.button_right['text'] = 'OK' if self.have_one_button else 'YES' if mode != EnumMode.ERRORRETRY else 'RETRY'
        self.button_right2['text'] = 'NO' if mode != EnumMode.ERRORRETRY else 'CANCEL'
        self.canvas.pack(side=tk.LEFT, anchor=tk.N, padx=20, pady=10)
        self.label_right.pack(side=tk.LEFT, padx=0, pady=10)
        self.button_right.grid(row=0, column=0, padx=10, pady=10) if self.have_button else 'pass'
        self.button_right2.grid(row=0, column=1, padx=10, pady=10) if self.have_two_button else 'pass'
        # pack
        self.frame_button.pack(side=tk.BOTTOM)
        self.frame_icon.pack(side=tk.LEFT)
        self.frame_message.pack(side=tk.LEFT, fill=tk.Y)
        # image
        img_list = ['question.png', 'information.png', 'warning.png', 'error.png', 'progress.png', 'splash.png', 'error.png']
        msgbox_path = os.path.dirname(__file__)
        img_file = os.path.join(msgbox_path, img_list[mode.value])
        self.img = tk.PhotoImage(file=img_file, width=48, height=48)
        self.canvas.create_image(2, 2, image=self.img, anchor=tk.NW)
        self.is_yes = False
        self.index = 0
        self.after(2000, self.on_timer)
        self.master.wait_window()
    def on_timer(self):
        self.index += 1
        self.after(2000, self.on_timer)
    def get_my_geometry(self, parent_geometry, my_geometry):
        print(f'parent_geometry:{parent_geometry},geometry:{my_geometry}')
        parent_geometry = parent_geometry.split('+')
        parent_left, parent_top = int(parent_geometry[1]), int(parent_geometry[2])
        parent_geometry = parent_geometry[0].split('x')
        prrent_widht, parent_height = int(parent_geometry[0]), int(parent_geometry[1])
        tmp_geometry = my_geometry.split('x')
        my_widht, my_height = int(tmp_geometry[0]), int(tmp_geometry[1])
        my_left, my_top = parent_left + (prrent_widht - my_widht) // 2, parent_top + (parent_height - my_height) // 2
        geometry = f'{my_geometry}+{my_left}+{my_top}'
        return geometry
    def on_btn_yes(self):
        self.is_yes = True
        self.master.destroy()
    def on_btn_no(self):
        self.master.destroy()
    @classmethod
    def set_message(cls, message):
        cls.mycls.message.set(message)
    @classmethod
    def close(cls):
        cls.mycls.master.destroy()

class MsgBox(Singleton):
    def __init__(self):
        if not hasattr(self, '_parent'):
            self._parent = None
    @classmethod
    def set_parent(cls, parent):
        cls()._parent = parent
    @classmethod
    def question(cls, message):
        frame = MainFrame(parent=cls()._parent, message=message, mode=EnumMode.QUESTION)
        return frame.is_yes
    @classmethod
    def errorretry(cls, message):
        frame = MainFrame(parent=cls()._parent, message=message, mode=EnumMode.ERRORRETRY)
        return frame.is_yes
    @classmethod
    def information(cls, message):
        MainFrame(parent=cls()._parent, message=message, mode=EnumMode.INFORMATION)
    @classmethod
    def warning(cls, message):
        MainFrame(parent=cls()._parent, message=message, mode=EnumMode.WARNING)
    @classmethod
    def error(cls, message):
        MainFrame(parent=cls()._parent, message=message, mode=EnumMode.ERROR)
    @classmethod
    def progress(cls, message):
        MainFrame(parent=cls()._parent, message=message, mode=EnumMode.PROGRESS)
    @classmethod
    def splash(cls, message):
        MainFrame(parent=cls()._parent, message=message, mode=EnumMode.SPLASH, topmost=False)
    @classmethod
    def set_message(cls, message):
        MainFrame.set_message(message)
    @classmethod
    def close(cls):
        MainFrame.close()

def open_msgbox(parent, message):
    MsgBox.set_parent(parent)
    MsgBox.progress(message=message)
    frame = MsgBox.question(message=message)
    MsgBox.error(message=message)
    MsgBox.information(message=message)
    MsgBox.warning(message=message)
    MsgBox.errorretry(message=message)
    return frame.is_yes
def set_message(message):
    MsgBox.set_message(message)
def close_msgbox():
    MsgBox.close()

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('400x200')
    index = 0
    def stop():
        global index
        index += 1
        if index <= 15:
            hello = f'hello world!! ({index}/5) '
            hello *= 5
            hello2 = f'{hello}\n{hello}\n{hello}'
            print(hello2)
            set_message(hello2)
            root.after(1000,stop)
        else:
            index = 0
            close_msgbox()
    def on_button():
        root.after(1000,stop)
        result = open_msgbox(root, 'hello world!\n' * 2 + 'hello world!')
        label['text'] = str(result)
    label = tk.Label(text='??')
    button = tk.Button(text='msgbox', bg='#00ffff', command=on_button)
    label.pack()
    button.pack()
    root.mainloop()

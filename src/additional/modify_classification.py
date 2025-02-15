# -*- coding: utf-8 -*-

# std
import os
import threading

# install
import time
import win32gui
import ttkbootstrap

# project
import core
from constant import *


illegalchat = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']


class selfstatus (object):
    action = threading.Lock()


class NewClassification (object):
    def __init__(self, new_class: bool = False):
        result = selfstatus.action.acquire(timeout=0.01)
        if not result:
            core.window.messagebox.showerror(title='互斥锁请求超时', message='互斥锁正在被其他线程占用\n上一次操作未结束或锁没有被正确释放\n亦或是你想测试这个操作是不是线程安全的')
            return

        self.install(new_class)


    def install(self, new_class: bool = False):
        if new_class:
            self.mark_newclass = True

        else:
            self.classname = core.window.interface.mods_manage.value_classification_item
            self.mark_newclass = True if self.classname in ["", None, "未分类"] else False

        # self.classname = core.window.interface.mods_manage.sbin_get_select_classification()
        # self.mark_newclass = True if self.classname in [None, '未分类'] else False
        windowsname = '添加分类' if self.mark_newclass else '修改分类'
        self.windows = ttkbootstrap.Toplevel(windowsname)
        self.windows.transient(core.window.mainwindow)
        # self.windows.grab_set()

        try:
            self.windows.iconbitmap(default=core.env.file.local.iconbitmap)
            self.windows.iconbitmap(bitmap=core.env.file.local.iconbitmap)
        except Exception:
            ...

        width = 60

        self.Frame_classname = ttkbootstrap.Frame(self.windows)
        self.Label_classname = ttkbootstrap.Label(self.Frame_classname, text='分类名称')
        self.Entry_classname = ttkbootstrap.Entry(self.Frame_classname, width=width)
        self.Frame_content = ttkbootstrap.Frame(self.windows)
        self.Text_content = ttkbootstrap.Text(self.Frame_content, height=20)
        self.Scrollbar_content = ttkbootstrap.Scrollbar(self.Frame_content, command=self.Text_content.yview)
        self.Frame_options = ttkbootstrap.Frame(self.windows)
        self.Button_ok = ttkbootstrap.Button(self.Frame_options, text='保存', width=10, bootstyle="success-outline", command=self.bin_ok)
        self.Button_cancel = ttkbootstrap.Button(self.Frame_options, text='取消', width=10, bootstyle="warning-outline", command=self.bin_cancel)
        self.Button_delete = ttkbootstrap.Button(self.Frame_options, text='删除', width=10, bootstyle="danger-outline", command=self.bin_delete)
        self.Label_errormsg = ttkbootstrap.Label(self.Frame_options, text='', bootstyle="danger")

        self.Text_content.config(yscrollcommand=self.Scrollbar_content.set)

        self.Frame_classname.pack(side='top', fill='x', padx=10, pady=10)
        self.Label_classname.pack(side='left', padx=0, pady=0)
        self.Entry_classname.pack(side='left', fill='x', expand=True, padx=(10, 0), pady=0)
        self.Frame_content.pack(side='top', fill='both', expand=True, padx=10, pady=(0, 10))
        self.Scrollbar_content.pack(side='right', fill='y', padx=(5, 0), pady=0)
        self.Text_content.pack(side='right', fill='both', expand=True, padx=0, pady=0)
        self.Frame_options.pack(side='top', fill='x', padx=10, pady=(0, 10))
        self.Button_ok.pack(side='right', padx=0, pady=0)
        self.Button_cancel.pack(side='right', padx=(0, 5), pady=0)
        if not self.mark_newclass: self.Button_delete.pack(side='right', padx=(0, 5), pady=0)
        self.Label_errormsg.pack(side='left', padx=(0, 5), pady=0)

        self.windows.protocol('WM_DELETE_WINDOW', self.bin_cancel)

        _alt_set = core.window.annotation_toplevel.register
        _alt_set(self.Entry_classname, T.ANNOTATION_CLASS_NAME, 2)
        _alt_set(self.Button_ok, T.ANNOTATION_MODIFY_CLASS_OK, 2)
        _alt_set(self.Button_cancel, T.ANNOTATION_MODIFY_CLASS_CANCEL, 2)
        _alt_set(self.Button_delete, T.ANNOTATION_MODIFY_CLASS_DELETE, 2)

        self.correction()


    def __get_classification_file_content(self):
        filepath = os.path.join(core.userenv.directory.classification, self.classname)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

        except Exception:
            content = ''

        return content


    def __set_classification_file_content(self, newclassname, content):
        ...


    def correction(self):
        if not self.mark_newclass:
            self.Entry_classname.insert(0, self.classname)
            self.Text_content.insert(0.0, self.__get_classification_file_content())

        # time.sleep(0.01)
        self.windows.update()

        width = self.windows.winfo_width()
        height = self.windows.winfo_height()

        _x, _y = win32gui.GetCursorInfo()[2]

        x = _x - width // 2
        y = _y - height // 2 - 20

        if x < 0: x = 0
        if y < 0: y = 0

        self.windows.geometry(f'+{x}+{y}')
        self.windows.resizable(False, False)


    def bin_ok(self, *args):
        newclassname = self.Entry_classname.get().strip()
        core.log.debug(f"分类名称 \"{newclassname}\" ")

        if not newclassname:
            self.Label_errormsg.config(text="分类名称不能为空")
            return

        for chat in illegalchat:
            if chat in newclassname:
                self.Label_errormsg.config(text="分类名称包含非法字符")
                return

        content = self.Text_content.get(0.0, 'end')[:-1]

        newfilepath = os.path.join(core.userenv.directory.classification, newclassname)

        if not self.mark_newclass:
            oldfilepath = os.path.join(core.userenv.directory.classification, self.classname)
            if newfilepath != oldfilepath:
                if os.path.exists(newfilepath):
                    self.Label_errormsg.config(text="分类名称已存在或被占用")
                    return

                else:
                    os.remove(oldfilepath)

        else:
            if os.path.exists(newfilepath):
                self.Label_errormsg.config(text="分类名称已存在或被占用")
                return

        with open(newfilepath, 'w', encoding='utf-8') as f:
            f.write(content)

        self.bin_over_content()


    def bin_cancel(self, *args):
        self.windows.destroy()
        selfstatus.action.release()


    def bin_delete(self, *args):
        filepath = os.path.join(core.userenv.directory.classification, self.classname)
        os.remove(filepath)
        self.bin_over_content()


    def bin_over_content(self):
        self.bin_cancel()
        core.module.mods_manage.refresh()


def modify_classification(*args):
    NewClassification()
    # threading.Thread(None, NewClassification, 'modify', (), {}, daemon=True).start()

import os
import sys
import yaml
import subprocess
import openpyxl
from openpyxl.styles.borders import Border, Side
from enum import Enum
#sys.path.append('../common_lib')
from lib.yaml_loader import YamlLoader
from lib.msgbox import MsgBox

class EnumCtrlLoop(Enum):
    NEXT = 0
    CONTINUE = 1
    BREAK = 2

class ExcelApplication(YamlLoader):
    __hit = False
    __break_count = 0
    def __init__(self, module_name):
        super().__init__(module_name)
        yaml = YamlLoader(__file__)
        self.MSG_SAVE_NG = yaml.get_yaml_info('message', 'msg_save_ng')
    def __del__(self):
        pass
    def get_excel_path(self):
        yaml = YamlLoader(__file__)
        path = yaml.get_yaml_info('path', 'excel_path')
        print(path)
        return path
    def wait_close(self, excel_file):
        is_retry = True 
        while is_retry:
            result, desc = self._is_opened(excel_file)
            if result:
                MsgBox.close()
                is_retry = MsgBox.errorretry(f'close {excel_file}!\n{desc}')
                print(f'is_retry:{is_retry}')
            else:
                is_retry = False
    def open(self, excel_file):
        openpyxl.reader.excel.warnings.simplefilter('ignore')
        self._wb = openpyxl.load_workbook(excel_file)
        self._excel_file = excel_file
    def reopen(self):
        self.close()
        self.open(self._excel_file)
    def save(self):
        is_retry = True 
        while is_retry:
            result, desc = self._save(self._excel_file)
            if result == False:
                is_retry = MsgBox.errorretry(f'{self.MSG_SAVE_NG}\n{desc}')
                print(f'is_retry:{is_retry}')
            else:
                is_retry = False
    def close(self):
        self._wb.close()
    def get_sheet_name_list(self):
        return self._wb.sheetnames
    def find_sheet_name(self, key):
        sheet_names = self._wb.sheetnames
        target_list = [x for x in sheet_names if key in x]
        return target_list
    def get_work_sheet(self, sheet_name):
        return self._wb[sheet_name]
    def exec(self, cmd_line):
        print('exec:', cmd_line)
        ps = subprocess.run(cmd_line, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, text=True)
    def copy_work_sheet(self, src_excel_file, sheet_name):
        try:
            import xlwings as xw
        except:
            self.exec('pip install xlwings')
            import xlwings as xw
        app = xw.App(visible=False)
        dst_wb = app.books.open(self._excel_file)
        src_wb = app.books.open(src_excel_file)
        #dst_wb = xw.Book(self._excel_file)
        #src_wb = xw.Book(src_excel_file)
        sheet_name_list = self.get_sheet_name_list()
        dst_wb.sheets[sheet_name].delete() if sheet_name in sheet_name_list else 'pass'
        src_wb.sheets[sheet_name].copy(after=dst_wb.sheets[0])
        dst_wb.save()
        dst_wb.close()
        print(f'xw.books.count:{xw.books.count}')
        if xw.books.count == 1:
            app = xw.apps.active
            app.quit()
        else:
            src_wb.close()
    def get_posi(self, sheet_name, sheet_name_list):
        for index, x in enumerate(sheet_name_list):
            if sheet_name == x:
                posi = index
                break
        return posi
    def select_work_sheet(self, sheet_name):
        self._ws = self._wb[sheet_name]
        return self._ws
    def selected_top_sheet(self):
        for ws in self._wb.worksheets:
            ws.sheet_view.tabSelected = False
        self._wb.active = self._wb.worksheets[0]
    def rename_work_sheet(self, new_sheet_name):
        self._ws.title = new_sheet_name
    def move_work_sheet(self, offset):
        self._wb.move_sheet(self._ws, offset=offset)
    def remove_work_sheet(self, sheet_name):
        self._wb.remove(self._wb[sheet_name])
    def sort_sheet_list(self, sheet_name):
        sheet_name_list = self.get_sheet_name_list()
        sheet_name_list = sheet_name_list[1:]
        print(f'sheet_name_list(pre):{sheet_name_list}')
        posi_before = self.get_posi(sheet_name, sheet_name_list)
        sheet_name_list.sort()
        list_under100 = [d for d in sheet_name_list if len(d.split('(')[0]) <= 2]
        list_over100 = [d for d in sheet_name_list if len(d.split('(')[0]) > 2]
        sheet_name_list = list_under100 + list_over100
        posi_after = self.get_posi(sheet_name, sheet_name_list)
        print(f'sheet_name_list(sorted):{sheet_name_list}')
        self.select_work_sheet(sheet_name)
        offset = posi_after - posi_before
        print(f'offset:{offset}')
        self.move_work_sheet(offset=offset)
        self.selected_top_sheet()
        self.save()
        sheet_name_list = self.get_sheet_name_list()
    def insert_row(self, row):
        self._ws.insert_rows(row)
    def insert_rows(self, row, lines=1):
        self._ws.insert_rows(row, lines)
    def delete_row(self, row):
        self._ws.delete_rows(row)
    def delete_rows(self, row, lines=1):
        self._ws.delete_rows(row, lines)
    def get_column_from_string(self, column_str):
        return openpyxl.utils.column_index_from_string(column_str)
    def get_max_row_column(self):
        return self._ws.max_row, self._ws.max_column
    def get_list(self, column_str, header):
        list = []
        self.__init_start_end()
        for _, cell in enumerate(self._ws[column_str]):
            judge = self.__judge_start_end(cell, header)
            if judge == EnumCtrlLoop.CONTINUE:
                continue
            elif judge == EnumCtrlLoop.BREAK:
                break
            if cell.value == None:
                continue
            list += [str(cell.value).strip().replace("`", '').replace("'", '')]
        return list
    def get_row_value_list(self, column_str, header):
        list = []
        self.__init_start_end()
        for index, cell in enumerate(self._ws[column_str], start=1):
            judge = self.__judge_start_end(cell, header)
            if judge == EnumCtrlLoop.CONTINUE:
                continue
            elif judge == EnumCtrlLoop.BREAK:
                break
            if cell.value == None:
                continue
            list += [(index, str(cell.value).strip().replace("`", '').replace("'", ''))]
        return list
    def get_row_value_dict(self, column_str, header):
        list = self.get_row_value_list(column_str, header)
        return {key: value for (key, value) in list}
    def get_column_name_dict(self, column_str, far_left_name):
        list = []
        self.__init_start_end()
        index_row = -1
        max_info = self.get_max_row_column()
        for index, cell in enumerate(self._ws[column_str], start=1):
            if str(cell.value) == far_left_name:
                index_row = index
                break
            if max_info[0] < index:
                break
        for column, _ in enumerate(range(max_info[1]), start=1):
            cell = self.get_cell(index_row, column)
            if cell.value == None or str(cell.value) == '':
                continue
            list += [(column, str(cell.value).strip().replace("`", '').replace("'", ''))]
        return {key: value for (key, value) in list}
    def get_column_value_dict(self, row):
        list = []
        max_info = self.get_max_row_column()
        for column, _ in enumerate(range(max_info[1]), start=1):
            cell = self.get_cell(row, column)
            if cell.value == None or str(cell.value) == '':
                value = ''
            else:
                value = str(cell.value).strip().replace("`", '').replace("'", '')
            list += [(column, value)]
        return {key: value for (key, value) in list}
    def find_keyword_row(self, column_str, header, keyword):
        self.__init_start_end()
        for index, cell in enumerate(self._ws[column_str], start=1):
            judge = self.__judge_start_end(cell, header)
            if judge == EnumCtrlLoop.CONTINUE:
                continue
            elif judge == EnumCtrlLoop.BREAK:
                break
            if str(cell.value).strip().replace("`", '').replace("'", '') == keyword:
                return index
        return -1
    def get_value(self, row, column):
        if str(column).isalpha():
            column = self.get_column_from_string(column)
        #return str(self._ws[column][row].value)
        return str(self.get_cell(row, column).value)
    def get_cell(self, row, column):
        if str(column).isalpha():
            column = self.get_column_from_string(column)
        return self._ws.cell(row=row, column=column)
    def draw_rect(self, row, column):
        side = Side(style='thin', color='000000')
        border = Border(bottom=side, left=side, right=side)
        self.get_cell(row, column).border = border
    def _save(self, excel_file):
        try:
            self._wb.save(excel_file)
            return True, None
        except Exception as ex:
            print(str(ex))
            return False, str(ex)
    def _is_opened(self, excel_file):
        try:
            f = open(excel_file, 'a')
            f.close()
            return False, None
        except Exception as ex:
            print(str(ex))
            return True, str(ex)
    def __init_start_end(self):
        ExcelApplication.__hit = False
        ExcelApplication.__break_count = 0
    def __judge_start_end(self, cell, header):
        if str(cell.value) == header:
            ExcelApplication.__hit = True
            return EnumCtrlLoop.CONTINUE
        if not ExcelApplication.__hit:
            return EnumCtrlLoop.CONTINUE
        if ExcelApplication.__break_count > 10:
            return EnumCtrlLoop.BREAK
        if str(cell.value) == '':
            ExcelApplication.__break_count += 1
            return EnumCtrlLoop.CONTINUE
        else:
            ExcelApplication.__break_count = 0
            return EnumCtrlLoop.NEXT

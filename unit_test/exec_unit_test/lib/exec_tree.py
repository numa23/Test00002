from lib import printx, printy
from lib.def_func_common import *

class ExecTree():
    def __init__(self):
        self.OPERATIONS = []
        self.OPERATIONS += ['+', '-', '*', '@', '/', '//', '%', '^', '**']
        self.OPERATIONS += ['<<', '>>']
        self.OPERATIONS += ['<', '<=', '==', '!=', '>=', '>', '<>', '&', '|', 'and', 'or', 'in', 'not in']
        self.DEBUG_FUNCS = ['peep_genv', 'peep_lenv', 'debug_print']
        self.ALIAS_FUNCS = {'range': 'range2'}
        self.cnvquot = lambda x: x.replace('"', '\\"').replace("'", "\\'")
        self.cnvstr = lambda x: f"'{self.cnvquot(x)}'" if type(x) == str else x
        self.cnvint = lambda x: str(x) if type(x) == int else x
        #self.print_genv = False
        self.print_var_ref = False
        self.print_var_def = False
        self.print_operation = False
        self.print_func_info = False
        self.print_func_in = False
        self.print_func_out = False
    def exec_calc(self, tree):
        genv = {}
        lenv = {}
        self._func_regist(genv)
        try:
            result = self._exec_calc(tree, genv, lenv)
        except Exception as ex:
            printy(f'{str(ex.with_traceback())}')
        return result
    def _func_regist(self, genv):
        # python function
        genv['p'] = ['func_in', 'print']
        genv['print'] = ['func_in', 'print']
        genv['abs'] = ['func_in', 'abs']
        genv['bin'] = ['func_in', 'bin']
        genv['str'] = ['func_in', 'str']
        genv['int'] = ['func_in', 'int']
        genv['bool'] = ['func_in', 'bool']
        genv['complex'] = ['func_in', 'complex']
        genv['divmod'] = ['func_in', 'divmod']
        genv['help'] = ['func_in', 'help']
        genv['len'] = ['func_in', 'len']
        genv['max'] = ['func_in', 'max']
        genv['min'] = ['func_in', 'min']
        genv['round'] = ['func_in', 'round']
        genv['sorted'] = ['func_in', 'sorted']
        genv['sum'] = ['func_in', 'sum']
        # define function
        func_regist(genv)
    def _exec_calc(self, tree, genv, lenv):
        if tree[0][0] == '#':
            return
        #print(f'{tree}:{type(tree)}')
        if tree[0] in ['num', 'str', 'bool', 'none']:
            return tree[1]
        elif tree[0] in self.OPERATIONS:
            return self._exec_operation(tree, genv, lenv)
        elif tree[0] == 'stmts':
            last = None
            for item in tree[1:]:
                last = self._exec_calc(item, genv, lenv)
            return last
        elif tree[0] == 'stmt':
            last = None
            for item in tree[1:]:
                last = self._exec_calc(item, genv, lenv)
            return last
        elif tree[0] == 'var_def':
            result = self._exec_calc(tree[2], genv, lenv)
            if type(result) == list and len(result) and result[0] == 'user_def':
                genv[tree[1]] = result
            else:
                lenv[tree[1]] = result
                printy(f'var_def:{lenv}') if self.print_var_def else 'pass'
            return result
        elif tree[0] == 'var_ref':
            printy(f'var_ref:{lenv}') if self.print_var_ref else 'pass'
            return lenv[tree[1]]
        elif tree[0] == 'list_new':
            list_new = []
            for item in tree[1:]:
                list_new += [self._exec_calc(item, genv, lenv)]
            return list_new
        elif tree[0] == 'list_ref':
            list_ref = self._exec_calc(tree[1], genv, lenv)
            if len(tree) == 2:
                return list_ref
            if type(list_ref) == list:
                index = self._exec_calc(tree[2], genv, lenv)
                return list_ref[index]
            else:
                dict_ref = list_ref
                for item in tree[2:]:
                    key = self._exec_calc(item, genv, lenv)
                    dict_ref = dict_ref.get(key)
                return dict_ref
        elif tree[0] == 'list_upd':
            list_name = tree[1][1][1]
            key_list = []
            for index, item in enumerate(tree[1][2:]):
                key_list += [self._exec_calc(item, genv, lenv)]
            data = self._exec_calc(tree[2], genv, lenv)
            dict_tmp = lenv[list_name]
            dict_ref = dict_tmp
            count = len(key_list)
            for index, key in enumerate(key_list, start=1):
                if index >= count:
                    break
                dict_ref = dict_ref[key]
            dict_ref[key] = data
            lenv[list_name] = dict_tmp
        elif tree[0] == 'dict_upd':
            data = self._exec_calc(tree[3], genv, lenv)
            key_list = tree[2].split('.')
            dict_tmp = lenv[tree[1]]
            dict_ref = dict_tmp
            count = len(key_list)
            for index, key in enumerate(key_list, start=1):
                if index >= count:
                    break
                dict_ref = dict_ref[key]
            dict_ref[key] = data
            lenv[tree[1]] = dict_tmp
        elif tree[0] == 'dict_ref':
            dict_ref = self._exec_calc(tree[1], genv, lenv)
            if len(tree) == 2:
                return dict_ref
            key_list = self._exec_calc(tree[2], genv, lenv).split('.')
            for key in key_list:
                dict_ref = dict_ref.get(key)
            return dict_ref
        elif tree[0] == 'dict_new':
            dict = {}
            for item in tree[1:]:
                dict[self._exec_calc(item[0], genv, lenv)] = self._exec_calc(item[1], genv, lenv)
            return dict
        elif tree[0] == 'if':
            if self._exec_calc(tree[1], genv, lenv):
                return self._exec_calc(tree[2], genv, lenv)
            else:
                return self._exec_calc(tree[3], genv, lenv)
        elif tree[0] == 'else':
            return self._exec_calc(tree[1], genv, lenv)
        elif tree[0] == 'wl':
            while self._exec_calc(tree[1], genv, lenv):
                try:
                    self._exec_calc(tree[2], genv, lenv)
                except Exception as ex:
                    if str(ex) == 'break':
                        break
                    elif str(ex) == 'continue':
                        continue
                    raise ex
        elif tree[0] == 'break':
            raise ValueError('break')
        elif tree[0] == 'continue':
            raise ValueError('continue')
        elif tree[0] == 'iif':
            if self._exec_calc(tree[1], genv, lenv):
                return self._exec_calc(tree[2], genv, lenv)
            else:
                return self._exec_calc(tree[3], genv, lenv)
        elif tree[0] == 'func_def':
            genv[tree[1]] = ['user_def', tree[2], tree[3]]
        elif tree[0] == 'lambda':
            return ['user_def', tree[1], ['stmts', ['stmt', ['return', tree[2]]]]]
        elif tree[0] == 'func_call':
            if tree[1] in self.DEBUG_FUNCS:
                self._debug(tree[1:], genv, lenv)
                return None
            return self._exec_func_call(tree, genv, lenv)
        elif tree[0] == 'return':
            lenv['return'] = self._exec_calc(tree[1], genv, lenv)
            raise ValueError('return')
        elif tree[0] == 'import':
            self._import(tree, genv, lenv)
    def _debug(self, tree, genv, lenv):
        mode = tree[0]
        if mode == 'peep_genv':
            printy(f'genv:{genv}')
        elif mode == 'peep_lenv':
            printy(f'lenv:{lenv}')
        elif mode == 'debug_print':
            #print(f'len(tree):{len(tree)},tree:{tree}')
            option = tree[1][1]
            length = len(tree[1:])
            if option == None:
                printy('-' * 25)
                printy('(debug_print)')
                printy('0:print_var_ref')
                printy('1:print_var_def')
                printy('2:print_operation')
                printy('3:print_func_info')
                printy('4:print_func_in')
                printy('5:print_func_out')
                printy('-' * 25)
                return
            flag = True if length == 1 else tree[2][1]
            if option == 0:
                self.print_var_ref = flag
            elif option == 1:
                self.print_var_def = flag
            elif option == 2:
                self.print_operation = flag
            elif option == 3:
                self.print_func_info = flag
            elif option == 4:
                self.print_func_in = flag
            elif option == 5:
                self.print_func_out = flag
        else:
            printy(f'not exist mode:{mode}')
    def _import(self, tree, genv, lenv):
        from lib.ctrl_import import CtrlImport
        from lib import Lexer, Parser, AstTree
        #from lib.parser_stmt import Parser
        #from lib.ast_tree import AstTree
        ctrl_import = CtrlImport(tree, genv)
        import_file = ctrl_import.get_import_file()
        printx(import_file)
        if ctrl_import.is_update():
            with open(import_file, encoding='utf-8', newline=None) as f:
                input = f.read()
            tokens = Lexer.cnv_tokens(input)
            parser = Parser()
            token = parser.exec(tokens)
            del_list = []
            for index, child in enumerate(token.children):
                if child.children[0].type not in ['FUNC_DEF', 'IMPORT']:
                    del_list += [index]
            for index in reversed(del_list):
                token.children.pop(index)
            token.print_token_tree()
            tree = AstTree()
            ast_tree = tree.exec(token)
            ctrl_import.create_cache(ast_tree)
        else:
            ast_tree = ctrl_import.get_ast_tree()
        self._exec_calc(eval(ast_tree), genv, lenv)
    def _exec_operation(self, tree, genv, lenv):
        item0 = self.cnvint(self.cnvstr(self._exec_calc(tree[1], genv, lenv)))
        item1 = self.cnvint(self.cnvstr(self._exec_calc(tree[2], genv, lenv)))
        printy(f'{item0} {tree[0]} {item1}') if self.print_operation else 'pass'
        return eval(f'{item0} {tree[0]} {item1}')
    def _exec_func_call(self, tree, genv, lenv):
        #print(f'genv:{genv}') if self.print_genv else 'pass'
        func_info, argc, args, args2 = self._get_func_info(tree, genv, lenv)
        printy(f'func_info:{func_info}\nargc:{argc},args:{args},args2:{args2}') if self.print_func_info else 'pass'
        if func_info == None:
            return f"error:Not found '{tree[1]}' in func_list."
        if func_info[0] == 'func_in':
            return self._func_in(func_info, argc, args2)
        else:
            return self._func_out(func_info, argc, args, genv)
    def _get_func_info(self, tree, genv, lenv):
        func_info = genv.get(tree[1])
        if func_info is None:
            func_info = genv.get(self.ALIAS_FUNCS.get(tree[1]))
            if func_info is None:
                return None, None, None, None
        args = []
        args2 = []
        argc = len(tree[2:])
        if argc > 1:
            for item in tree[2:]: 
                result = self._exec_calc(item, genv, lenv)
                args += [result]
                args2 += [self.cnvint(self.cnvstr(result))]
        else:
            item = tree[2:][0]
            result = self._exec_calc(item, genv, lenv)
            args = result
            args2 = self.cnvint(self.cnvstr(result))
        return func_info, argc, args, args2
    def _func_in(self, func_info, argc, args):
        printy(f'argc:{argc},args:{args}') if self.print_func_in else 'pass'
        if argc == 1:
            arg_line = args if args != None else ''
        elif argc > 1:
            args = [str(x) for x in args]
            arg_line = ','.join(args)
        else:
            arg_line = ''
        cmd_line = f'{func_info[1]}({arg_line})'
        printy(f'func_info:{cmd_line}') if self.print_func_in else 'pass'
        return eval(cmd_line)
    def _func_out(self, func_info, argc, args, genv):
        lenv_new = {}
        params = func_info[1]
        count = len(params)
        if count > 1:
            for index, param in enumerate(params):
                lenv_new[param] = args[index]
        elif count == 1:
            lenv_new[params[0]] = args
        else:
            pass
        try:
            printy(f'lenv_new:{lenv_new}') if self.print_func_out else 'pass'
            printy(f'func_info:{func_info[2]}') if self.print_func_out else 'pass'
            result = self._exec_calc(func_info[2], genv, lenv_new)
        except Exception as ex:
            if str(ex) == 'return':
                result = lenv_new['return']
            else:
                raise ex
        return result

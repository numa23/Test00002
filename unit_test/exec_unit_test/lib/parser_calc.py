import sys
from lib import Token, printx, printy
from lib.common import Common

class ParserCalc(Common):
    def __init__(self) -> None:
        self.NUM_LIST = [chr(x) for x in range(ord('0'), ord('9') + 1)]
        self.reverse_poland = ''
        self.len_total = 0
        self.prev_tokens = ''
        self.create_func_map()
    def create_func_map(self):
        self.func_map = {}
        self.func_map['or_test'] = [['or'], self.func_ope, 'and_test', self.func_ope, 'and_test']
        self.func_map['and_test'] = [['and'], self.not_test, '', self.not_test, '']
        self.func_map['expr'] = [['|'], self.func_ope, 'xor_expr', self.func_ope, 'xor_expr']
        self.func_map['xor_expr'] = [['^'], self.func_ope, 'and_expr', self.func_ope, 'and_expr']
        self.func_map['and_expr'] = [['&'], self.func_ope, 'shift_expr', self.func_ope, 'shift_expr']
        self.func_map['shift_expr'] = [['<<', '>>'], self.func_ope, 'arith_expr', self.func_ope, 'arith_expr']
        self.func_map['arith_expr'] = [['+', '-'], self.func_ope, 'term', self.func_ope, 'term']
        self.func_map['term'] = [['*', '@', '/', '%', '//'], self.factor, '', self.factor, '']
    def error(self, message, tokens, func_name=''):
        error_func = f' @{func_name}' if func_name != '' else ''
        printy(f'{message}{error_func} ', end='')
        if len(tokens):
            tokens[0].print(is_error=True)
        else:
            printy('tokens is empty!')
    def print_token_type_list(sellf, tokens):
        types = []
        for token in tokens:
            types += [token.type]
        printx(f"type_list:{','.join(types)}")
    def exec(self, tokens):
        printx(f'input:{Token.print_list(tokens)}')
        self.len_total = len(tokens)
        _, token = self.expr_stmt(tokens)
        printx(f'output:{self.reverse_poland}')
        return token
    #func_ope: func_ope (OPE func_ope)*
    def func_ope(self, func_name, tokens):
        self.trace(f'{sys._getframe().f_code.co_name}:({func_name}):{tokens[0].literal}')
        func_info = self.func_map[func_name]
        work = []
        tokens_tmp, token = func_info[1](func_info[2], tokens) if func_info[2] != '' else func_info[1](tokens)
        if token == None:
            printy(f'token is empty!:{sys._getframe().f_code.co_name}:({func_name})')
        work += [token]
        while len(tokens_tmp) != 0 and tokens_tmp[0].type != 'STR' and tokens_tmp[0].literal in func_info[0]:
            token_ope = tokens_tmp[0]
            ope = token_ope.literal
            tokens_tmp, token = func_info[3](func_info[4], tokens_tmp[1:]) if func_info[4] != '' else func_info[3](tokens_tmp[1:])
            if token == None:
                printy(f'token is empty2!:{sys._getframe().f_code.co_name}:({func_name})')
            work += [token]
            token_ope.children.insert(0, work.pop())
            token_ope.children.insert(0, work.pop())
            work += [token_ope]
            self.reverse_poland += f'{ope} '
        return tokens_tmp, work.pop()
    #expr_stmt: test (augassign test | ('=' test)*)
    def expr_stmt(self, tokens):
        self.trace(f'{sys._getframe().f_code.co_name}:{tokens[0].type},{tokens[0].literal}')
        work = []
        tokens_tmp, token = self.test(tokens)
        if token == None:
            printy(f'token is empty!:{sys._getframe().f_code.co_name}')
        work += [token]
        if len(tokens_tmp) != 0 and tokens_tmp[0].literal == '=':
            while len(tokens_tmp) != 0 and tokens_tmp[0].literal == '=':
                token_ope = tokens_tmp[0]
                ope = token_ope.literal
                tokens_tmp, token = self.test(tokens_tmp[1:])
                if token == None:
                    printy(f'token is empty2!:{sys._getframe().f_code.co_name}')
                work += [token]
                token_ope.children.insert(0, work.pop())
                token_ope.children.insert(0, work.pop())
                work += [token_ope]
                self.reverse_poland += f'{ope} '
        elif len(tokens_tmp) != 0 and '=' in tokens_tmp[0].literal:
            token_var = work.pop()
            self.reverse_poland += f'{token_var.literal} '
            token_ope = Token('ASSIGN', '=')
            ope = token_ope.literal
            token_ope.children += [token_var]
            tokens_tmp, token = self.augassign(tokens_tmp)
            if token == None:
                printy(f'token is empty3!:{sys._getframe().f_code.co_name}')
            token_ope2 = token
            ope2 = token_ope2.literal
            token_ope2.children += [token_var]
            tokens_tmp, token = self.test(tokens_tmp)
            if token == None:
                printy(f'token is empty4!:{sys._getframe().f_code.co_name}')
            token_ope2.children += [token]
            self.reverse_poland += f'{ope2} '
            token_ope.children += [token_ope2]
            work += [token_ope]
            self.reverse_poland += f'{ope} '
        return tokens_tmp, work.pop()
    #augassign: ('+=' | '-=' | '*=' | '@=' | '/=' | '%=' | '&=' | '|=' | '^=' | '<<=' | '>>=' | '**=' | '//=')
    def augassign(self, tokens):
        self.trace(f'{sys._getframe().f_code.co_name}:{tokens[0].type},{tokens[0].literal}')
        work = []
        tokens_tmp = tokens
        if len(tokens_tmp) != 0 and tokens_tmp[0].literal in ['+=', '-=', '*=', '@=', '/=', '%=', '&=', '|=', '^=', '<<=', '>>=', '**=', '//=']:
            token = Token('OPE', tokens_tmp[0].literal.replace('=', ''))
            tokens_tmp = tokens_tmp[1:]
            work += [token]
        else:
            printy(f'error:augassign expected! remain:{len(tokens)},token:{tokens[0].type},{tokens[0].literal}')
            exec()
        return tokens_tmp, work.pop()
    #test: or_test ['if' or_test 'else' test] | lambdef
    def test(self, tokens):
        self.trace(f'{sys._getframe().f_code.co_name}:{tokens[0].type},{tokens[0].literal}')
        self.prev_tokens = ''
        work = []
        tokens_tmp = tokens
        if len(tokens_tmp) != 0 and tokens_tmp[0].type == 'LAMBDA':
            tokens_tmp, token = self.lambdef(tokens_tmp)
            if token == None:
                printy(f'token is empty!:{sys._getframe().f_code.co_name}')
            work += [token]
        else:
            tokens_tmp, token = self.func_ope('or_test', tokens)
            if token == None:
                printy(f'token is empty!:{sys._getframe().f_code.co_name}')
            work += [token]
            if len(tokens_tmp) != 0 and tokens_tmp[0].type == 'IIF':
                token_ope = tokens_tmp[0]
                ope = token_ope.literal
                tokens_tmp, token = self.func_ope('or_test', tokens_tmp[1:])
                work += [token]
                token_ope.children += [work.pop()]
                token_ope.children += [work.pop()]
                if token == None:
                    printy(f'token is empty2!:{sys._getframe().f_code.co_name}')
                if len(tokens_tmp) != 0 and tokens_tmp[0].type == 'ELSE':
                    tokens_tmp, token = self.test(tokens_tmp[1:])
                    if token == None:
                        printy(f'token is empty3!:{sys._getframe().f_code.co_name}')
                    work += [token]
                    token_ope.children += [work.pop()]
                    work += [token_ope]
                else:
                    printy(f'error:ELSE expected! remain:{len(tokens)},token:{tokens[0].type},{tokens[0].literal}')
                self.reverse_poland += f'{ope} '
        return tokens_tmp, work.pop()
    #lambdef: 'lambda' [typedargslist] ':' test
    def lambdef(self, tokens):
        self.trace(f'{sys._getframe().f_code.co_name}:{tokens[0].type},{tokens[0].literal}')
        work = []
        tokens_tmp = tokens
        if not (len(tokens_tmp) != 0 and tokens_tmp[0].type == 'LAMBDA'):
            printy(f'error:LAMBDA expected! remain:{len(tokens_tmp)},token:{tokens_tmp[0].type},{tokens_tmp[0].literal}')
            return tokens_tmp, None
        token_ope = tokens_tmp[0]
        ope = token_ope.literal
        tokens_tmp, token = self.typedargslist(tokens_tmp[1:])
        if token == None:
            printy(f'token is empty!:{sys._getframe().f_code.co_name}')
        if not (len(tokens_tmp) != 0 and tokens_tmp[0].literal == ':'):
            printy(f'error:COLON expected! remain:{len(tokens_tmp)},token:{tokens_tmp[0].type},{tokens_tmp[0].literal}')
            return tokens_tmp, None
        work += [token]
        token_ope.children += [work.pop()]
        tokens_tmp, token = self.test(tokens_tmp[1:])
        if token == None:
            printy(f'token is empty2!:{sys._getframe().f_code.co_name}')
            return tokens_tmp, None
        work += [token]
        token_ope.children += [work.pop()]
        work += [token_ope]
        self.reverse_poland += f'{ope} '
        return tokens_tmp, work.pop()
    #not_test: 'not' not_test | comparison
    def not_test(self, tokens):
        self.trace(f'{sys._getframe().f_code.co_name}:{tokens[0].type},{tokens[0].literal}')
        work = []
        tokens_tmp = tokens
        if len(tokens_tmp) != 0 and tokens_tmp[0].literal in ['not']:
            token_ope = tokens_tmp[0]
            ope = token_ope.literal
            tokens_tmp, token = self.not_test(tokens_tmp[1:])
            if token == None:
                printy(f'token is empty!:{sys._getframe().f_code.co_name}')
            work += [token]
            token_ope.children.insert(0, work.pop())
            work += [token_ope]
            self.reverse_poland += f'{ope} '
        elif len(tokens_tmp) != 0:
            tokens_tmp, token = self.comparison(tokens_tmp)
            if token == None:
                printy(f'token is empty2!:{sys._getframe().f_code.co_name}')
            work += [token]
        else:
            printy(f'error:not_test token is empty!')
        return tokens_tmp, work.pop()
    #comparison: expr (comp_op expr)*
    def comparison(self, tokens):
        self.trace(f'{sys._getframe().f_code.co_name}:{tokens[0].type},{tokens[0].literal}')
        work = []
        #tokens_tmp, token = self.expr(tokens)
        tokens_tmp, token = self.func_ope('expr', tokens)
        if token == None:
            printy(f'token is empty!:{sys._getframe().f_code.co_name}')
        work += [token]
        while len(tokens_tmp) != 0 and tokens_tmp[0].type == 'COMP':
            tokens_tmp, token_ope = self.comp_op(tokens_tmp)
            ope = token_ope.literal
            #tokens_tmp, token = self.expr(tokens_tmp)
            tokens_tmp, token = self.func_ope('expr', tokens_tmp)
            if token == None:
                printy(f'token is empty2!:{sys._getframe().f_code.co_name}')
            work += [token]
            token_ope.children.insert(0, work.pop())
            token_ope.children.insert(0, work.pop())
            work += [token_ope]
            self.reverse_poland += f'{ope} '
        return tokens_tmp, work.pop()
    #comp_op: '<'|'>'|'=='|'>='|'<='|'<>'|'!='|'in'|'not' 'in'|'is'|'is' 'not'
    def comp_op(self, tokens):
        self.trace(f'{sys._getframe().f_code.co_name}:{tokens[0].type},{tokens[0].literal}')
        token = None
        if tokens[0].literal in ['<', '>', '==', '>=', '<=', '<>', '!=']:
            token = tokens[0]
            self.reverse_poland += f'{tokens[0].literal} '
        elif (tokens[0].literal, tokens[1].literal) == ('not', 'in'):
            token = tokens[0]
            token.literal = 'not in'
            self.reverse_poland += f'{tokens[1].literal} '
            tokens = tokens[1:]
        elif (tokens[0].literal, tokens[1].literal) == ('is', 'not'):
            token = tokens[0]
            token.literal = '!='
            self.reverse_poland += f'{tokens[0].literal} '
            tokens = tokens[1:]
        elif tokens[0].literal in ['in', 'is']:
            token = tokens[0]
            self.reverse_poland += f'{tokens[0].literal} '
        else:
            printy(f'error:comp_op not expect! remain:{len(tokens)},token:{tokens[0].type},{tokens[0].literal}')
        return tokens[1:], token
    #factor: ('+'|'-'|'~') factor | power
    def factor(self, tokens):
        self.trace(f'{sys._getframe().f_code.co_name}:{tokens[0].type},{tokens[0].literal}')
        work = []
        tokens_tmp = tokens
        if len(tokens_tmp) != 0 and tokens_tmp[0].type != 'STR' and tokens_tmp[0].literal in ['+', '-', '~']:
            token_ope = tokens_tmp[0]
            ope = token_ope.literal
            tokens_tmp, token = self.factor(tokens_tmp[1:])
            if token == None:
                printy(f'token is empty!:{sys._getframe().f_code.co_name}')
            work += [token]
            token_ope.children.insert(0, work.pop())
            work += [token_ope]
            self.reverse_poland += f'{ope} '
        elif len(tokens_tmp) != 0:
            tokens_tmp, token = self.power(tokens_tmp)
            if token == None:
                printy(f'token is empty2!:{sys._getframe().f_code.co_name}')
            work += [token]
        else:
            printy(f'error:factor token is empty!')
        return tokens_tmp, work.pop()
    #power: atom_expr ['**' factor]
    def power(self, tokens):
        self.trace(f'{sys._getframe().f_code.co_name}:{tokens[0].type},{tokens[0].literal}')
        work = []
        tokens_tmp, token = self.atom_expr(tokens)
        if token == None:
            printy(f'token is empty!:{sys._getframe().f_code.co_name}')
        work += [token]
        if len(tokens_tmp) != 0 and tokens_tmp[0].literal in ['**']:
            token_ope = tokens_tmp[0]
            ope = token_ope.literal
            tokens_tmp, token = self.factor(tokens_tmp[1:])
            if token == None:
                printy(f'token is empty2!:{sys._getframe().f_code.co_name}')
            work += [token]
            token_ope.children.insert(0, work.pop())
            token_ope.children.insert(0, work.pop())
            work += [token_ope]
            self.reverse_poland += f'{ope} '
        return tokens_tmp, work.pop()
    #atom_expr: atom trailer*
    def atom_expr(self, tokens):
        self.trace(f'{sys._getframe().f_code.co_name}:{tokens[0].type},{tokens[0].literal}')
        work = []
        token_atom = tokens[0]
        tokens_tmp, token = self.atom(tokens)
        work += [token]
        if len(tokens_tmp) != 0 and tokens_tmp[0].literal == '(':
            token_ope = work.pop()
            token_ope.type = 'FUNC_CALL'
            ope = token_ope.literal
            tokens_tmp, token = self.trailer(tokens_tmp)
            if token == None:
                printy(f'token is empty!:{sys._getframe().f_code.co_name}')
            work += [token]
            token_ope.children += [work.pop()]
            work += [token_ope]
            self.reverse_poland += f'{ope} '
        elif len(tokens_tmp) != 0 and tokens_tmp[0].literal == '[':
            token_ope = work.pop()
            token_ope.type = 'LIST_REF'
            ope = token_ope.literal
            while len(tokens_tmp) != 0 and tokens_tmp[0].literal == '[':
                tokens_tmp, token = self.trailer(tokens_tmp)
                if token == None:
                    printy(f'token is empty!:{sys._getframe().f_code.co_name}')
                for token_sub in token.children:
                    token_ope.children += [token_sub]
                work += [token_ope]
                self.reverse_poland += f'{ope} '
        elif len(tokens_tmp) != 0 and tokens_tmp[0].literal == '.':
            token_ope = work.pop()
            token_ope.type = 'DICT_REF'
            ope = token_ope.literal
            tokens_tmp, token = self.dotted_name(tokens_tmp[1:])
            if token == None:
                printy(f'token is empty!:{sys._getframe().f_code.co_name}')
            token.type = 'STR'
            token_ope.children += [token]
            work += [token_ope]
        return tokens_tmp, work.pop()
    #atom: ('(' [testlist] ')' | '[' [testlist] ']' | '{' [dictionary] '}' | (NAME | NUMBER | STRING+ | 'None' | 'True' | 'False'))
    def atom(self, tokens):
        self.trace(f'{sys._getframe().f_code.co_name}:{tokens[0].type},{tokens[0].literal}')
        if len(tokens) == len(self.prev_tokens):
            printy(f'error:Detected infinite loop! token position is {str(self.len_total - len(tokens)).zfill(4)}')
            exit()
        self.prev_tokens = tokens
        token = None
        if tokens[0].literal == '(':
            #tokens_tmp, token = self.trailer(tokens[1:])
            tokens_tmp, token = self.test(tokens[1:])
            if tokens_tmp[0].literal != ')':
                printy("error:not ')'")
            else:
                tokens = tokens_tmp
        elif tokens[0].literal == '[' and tokens[1].literal == ']':
            tokens = tokens[1:]
            token = Token('LIST', 'list')
        elif tokens[0].literal == '[':
            tokens_tmp, token = self.testlist(tokens[1:])
            if tokens_tmp[0].literal != ']':
                printy("error:not ']'")
            else:
                tokens = tokens_tmp
        elif tokens[0].literal == '{' and tokens[1].literal == '}':
            tokens = tokens[1:]
            token = Token('DICT', 'dict')
        elif tokens[0].literal == '{':
            tokens_tmp, token = self.dictionary(tokens[1:])
            if tokens_tmp[0].literal != '}':
                printy("error:not '}'")
            else:
                tokens = tokens_tmp
        elif tokens[0].type in ['VAR', 'NUM', 'STR', 'NONE', 'BOOL']:
            token = tokens[0]
            self.reverse_poland += f'{tokens[0].literal} '
        else:
            printy(f'error:atom not expect! remain:{len(tokens)},token:{tokens[0].type},{tokens[0].literal}')
        return tokens[1:], token
    #testlist: test (',' test)*
    def testlist(self, tokens):
        self.trace(f'{sys._getframe().f_code.co_name}:{tokens[0].type},{tokens[0].literal}')
        token_ope = Token('LIST', 'list')
        ope = token_ope.literal
        tokens_tmp, token = self.test(tokens)
        token_ope.children += [token]
        self.reverse_poland += f'{ope} '
        while len(tokens_tmp) != 0 and tokens_tmp[0].literal == ',':
            tokens_tmp = tokens_tmp[1:]
            tokens_tmp, token = self.test(tokens_tmp)
            token_ope.children += [token]
            self.reverse_poland += f'{ope} '
        return tokens_tmp, token_ope
    #dictionary: test ':' test (',' test ':' test)*
    def dictionary(self, tokens):
        self.trace(f'{sys._getframe().f_code.co_name}:{tokens[0].type},{tokens[0].literal}')
        token_ope = Token('DICT', 'dict')
        ope = token_ope.literal
        tokens_tmp, token_key = self.test(tokens)
        if len(tokens_tmp) != 0 and tokens_tmp[0].literal != ':':
            printy("error:not ':")
        tokens_tmp, token = self.test(tokens_tmp[1:])
        token_key.children += [token]
        token_ope.children += [token_key]
        self.reverse_poland += f'{ope} '
        while len(tokens_tmp) != 0 and tokens_tmp[0].literal == ',':
            tokens_tmp, token_key = self.test(tokens_tmp[1:])
            if len(tokens_tmp) != 0 and tokens_tmp[0].literal != ':':
                printy("error:not ':")
            tokens_tmp, token = self.test(tokens_tmp[1:])
            token_key.children += [token]
            token_ope.children += [token_key]
            self.reverse_poland += f'{ope} '
        return tokens_tmp, token_ope
    #trailer: '(' [arglist] ')' | '[' subscript ']'
    def trailer(self, tokens):
        self.trace(f'{sys._getframe().f_code.co_name}:{tokens[0].type},{tokens[0].literal}')
        token = None
        tokens_tmp = tokens
        if tokens_tmp[0].literal == '(':
            if tokens_tmp[1].literal == ')':
                tokens_tmp = tokens_tmp[1:]
                token = Token('NONE', 'None')
            else:
                tokens_tmp, token = self.arglist(tokens[1:])
            if tokens_tmp[0].literal != ')':
                printy("error:not ')'")
            tokens_tmp = tokens_tmp[1:]
        elif tokens_tmp[0].literal == '[':
            tokens_tmp, token = self.subscript(tokens[1:])
            if tokens_tmp[0].literal != ']':
                printy("error:not ']'")
            tokens_tmp = tokens_tmp[1:]
        else:
            printy(f'error:trailer not expect! remain:{len(tokens)},token:{tokens[0].type},{tokens[0].literal}')
        return tokens_tmp, token
    #subscript: test | [test] ':' [test]
    def subscript(self, tokens):
        self.trace(f'{sys._getframe().f_code.co_name}:{tokens[0].type},{tokens[0].literal}')
        token_ope = Token('SUBSC', 'subsc')
        ope = token_ope.literal
        tokens_tmp, token = self.test(tokens)
        token_ope.children += [token]
        self.reverse_poland += f'{ope} '
        return tokens_tmp, token_ope
    #arglist: argument (',' argument)*
    def arglist(self, tokens):
        self.trace(f'{sys._getframe().f_code.co_name}:{tokens[0].type},{tokens[0].literal}')
        token_ope = Token('ARG_LIST', 'ARG_list')
        ope = token_ope.literal
        tokens_tmp, token = self.argument(tokens)
        token_ope.children += [token]
        self.reverse_poland += f'{ope} '
        while len(tokens_tmp) != 0 and tokens_tmp[0].literal == ',':
            tokens_tmp = tokens_tmp[1:]
            tokens_tmp, token = self.argument(tokens_tmp)
            token_ope.children += [token]
            self.reverse_poland += f'{ope} '
        return tokens_tmp, token_ope
    #argument: ( test )
    def argument(self, tokens):
        self.trace(f'{sys._getframe().f_code.co_name}:{tokens[0].type},{tokens[0].literal}')
        tokens_tmp, token = self.test(tokens)
        self.reverse_poland += f'{tokens_tmp[0].literal} '
        return tokens_tmp, token

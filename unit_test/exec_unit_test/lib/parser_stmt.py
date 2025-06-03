import sys
from lib import Token, ParserCalc, printx, printy

class Parser(ParserCalc):
    def __init__(self) -> None:
        super().__init__()
        self.is_trace = False
    def exec(self, tokens):
        printx(f'input:{Token.print_list(tokens)}')
        self.len_total = len(tokens)
        _, token = self.stmts(tokens)
        printx(f'output:{self.reverse_poland}')
        return token
    #stmts: stmt*
    def stmts(self, tokens):
        self.trace(f'{sys._getframe().f_code.co_name}:{tokens[0].type},{tokens[0].literal}')
        work = []
        tokens_tmp = tokens
        if len(tokens_tmp) != 0 and tokens_tmp[0].type == 'STMTS':
            token_ope = tokens_tmp[0]
            ope = token_ope.literal
            tokens_tmp = tokens_tmp[1:]
            while len(tokens_tmp):
                tokens_tmp, token = self.stmt(tokens_tmp)
                if token == None:
                    printy(f'token is empty!:{sys._getframe().f_code.co_name}')
                work += [token]
                token_ope.children += [work.pop()]
            self.reverse_poland += f'{ope} '
            work += [token_ope]
        else:
            tokens_tmp, token = self.stmt(tokens_tmp)
            if token == None:
                printy(f'token is empty!:{sys._getframe().f_code.co_name}')
            work += [token]
        return tokens_tmp, work.pop()
    #stmt: small_stmt | compound_stmt
    def stmt(self, tokens):
        self.trace(f'{sys._getframe().f_code.co_name}:{tokens[0].type},{tokens[0].literal}')
        self.prev_tokens = ''
        work = []
        tokens_tmp = tokens
        if len(tokens_tmp) != 0 and tokens_tmp[0].type == 'STMT':
            token_ope = tokens_tmp[0]
            ope = token_ope.literal
            if len(tokens_tmp) > 1 and tokens_tmp[1].type in ['IF', 'WL', 'WHILE', 'FOR', 'DO', 'DEF']:
                tokens_tmp, token = self.compound_stmt(tokens_tmp[1:])
            else:
                tokens_tmp, token = self.small_stmt(tokens_tmp[1:])
            if token == None:
                printy(f'token is empty!:{sys._getframe().f_code.co_name}')
            work += [token]
            self.reverse_poland += f'{ope} '
            token_ope.children.insert(0, work.pop())
            work += [token_ope]
        else:
            tokens_tmp, token = self.expr_stmt(tokens_tmp)
            if token == None:
                printy(f'token is empty!:{sys._getframe().f_code.co_name}')
            work += [token]
        return tokens_tmp, work.pop()
    #small_stmt: (expr_stmt | pass_stmt | flow_stmt | import_stmt)
    def small_stmt(self, tokens):
        self.trace(f'{sys._getframe().f_code.co_name}:{tokens[0].type},{tokens[0].literal}')
        work = []
        tokens_tmp = tokens
        if len(tokens_tmp) != 0 and  tokens_tmp[0].type == 'PASS':
            tokens_tmp, token = self.pass_stmt(tokens_tmp)
            if token == None:
                printy(f'token is empty!:{sys._getframe().f_code.co_name}')
            work += [token]
        elif len(tokens_tmp) != 0 and  tokens_tmp[0].type in ['BREAK', 'CONTINUE', 'RETURN']:
            tokens_tmp, token = self.flow_stmt(tokens_tmp)
            work += [token]
        elif len(tokens_tmp) != 0 and  tokens_tmp[0].type == 'IMPORT':
            tokens_tmp, token = self.import_stmt(tokens_tmp)
            work += [token]
        else:
            tokens_tmp, token = self.expr_stmt(tokens_tmp)
            if token == None:
                printy(f'token is empty!:{sys._getframe().f_code.co_name}')
            work += [token]
        return tokens_tmp, work.pop()
    #pass_stmt: 'pass'
    def pass_stmt(self, tokens):
        self.trace(f'{sys._getframe().f_code.co_name}:{tokens[0].type},{tokens[0].literal}')
        work = []
        tokens_tmp = tokens
        if len(tokens_tmp) != 0 and tokens_tmp[0].type == 'PASS':
            token = tokens_tmp[0]
            tokens_tmp = tokens_tmp[1:]
            if token == None:
                printy(f'token is empty!:{sys._getframe().f_code.co_name}')
            work += [token]
        else:
            self.error(f'error:expected {sys._getframe().f_code.co_name}!', tokens_tmp)
            return tokens_tmp, None
        return tokens_tmp, work.pop()
    #flow_stmt: break_stmt | continue_stmt | return_stmt
    def flow_stmt(self, tokens):
        self.trace(f'{sys._getframe().f_code.co_name}:{tokens[0].type},{tokens[0].literal}')
        work = []
        tokens_tmp = tokens
        if len(tokens_tmp) != 0 and tokens_tmp[0].type == 'BREAK':
            tokens_tmp, token = self.break_stmt(tokens_tmp)
            work += [token]
        elif len(tokens_tmp) != 0 and tokens_tmp[0].type == 'CONTINUE':
            tokens_tmp, token = self.continue_stmt(tokens_tmp)
            work += [token]
        elif len(tokens_tmp) != 0 and tokens_tmp[0].type == 'RETURN':
            tokens_tmp, token = self.return_stmt(tokens_tmp)
            work += [token]
        else:
            self.error(f'error:expected {sys._getframe().f_code.co_name}!', tokens_tmp)
            return tokens_tmp, None
        return tokens_tmp, work.pop()
    #break_stmt: 'break'
    def break_stmt(self, tokens):
        self.trace(f'{sys._getframe().f_code.co_name}:{tokens[0].type},{tokens[0].literal}')
        work = []
        tokens_tmp = tokens
        if len(tokens_tmp) != 0 and tokens_tmp[0].type == 'BREAK':
            token = tokens_tmp[0]
            tokens_tmp = tokens_tmp[1:]
            if token == None:
                printy(f'token is empty!:{sys._getframe().f_code.co_name}')
            work += [token]
        else:
            self.error(f'error:expected {sys._getframe().f_code.co_name}!', tokens_tmp)
            return tokens_tmp, None
        return tokens_tmp, work.pop()
    #continue_stmt: 'continue'
    def continue_stmt(self, tokens):
        self.trace(f'{sys._getframe().f_code.co_name}:{tokens[0].type},{tokens[0].literal}')
        work = []
        tokens_tmp = tokens
        if len(tokens_tmp) != 0 and tokens_tmp[0].type == 'CONTINUE':
            token = tokens_tmp[0]
            tokens_tmp = tokens_tmp[1:]
            if token == None:
                printy(f'token is empty!:{sys._getframe().f_code.co_name}')
            work += [token]
        else:
            self.error(f'error:expected {sys._getframe().f_code.co_name}!', tokens_tmp)
            return tokens_tmp, None
        return tokens_tmp, work.pop()
    #return_stmt: 'return' [test]
    def return_stmt(self, tokens):
        self.trace(f'{sys._getframe().f_code.co_name}:{tokens[0].type},{tokens[0].literal}')
        work = []
        tokens_tmp = tokens
        if len(tokens_tmp) != 0 and tokens_tmp[0].type == 'RETURN':
            token_ope = tokens_tmp[0]
            ope = token_ope.literal
            tokens_tmp, token = self.test(tokens_tmp[1:])
            if token == None:
                printy(f'token is empty!:{sys._getframe().f_code.co_name}')
            token_ope.children += [token]
            self.reverse_poland += f'{ope} '
            work += [token_ope]
        else:
            self.error(f'error:expected {sys._getframe().f_code.co_name}!', tokens_tmp)
            return tokens_tmp, None
        return tokens_tmp, work.pop()

    #import_stmt: 'import' dotted_name
    def import_stmt(self, tokens):
        self.trace(f'{sys._getframe().f_code.co_name}:{tokens[0].type},{tokens[0].literal}')
        work = []
        tokens_tmp = tokens
        if len(tokens_tmp) != 0 and tokens_tmp[0].type == 'IMPORT':
            token_ope = tokens_tmp[0]
            ope = token_ope.literal
            tokens_tmp, token = self.dotted_name(tokens_tmp[1:])
            if token == None:
                printy(f'token is empty!:{sys._getframe().f_code.co_name}')
            token_ope.literal = token.literal
            work += [token_ope]
        else:
            self.error(f'error:expected {sys._getframe().f_code.co_name}!', tokens_tmp)
            return tokens_tmp, None
        return tokens_tmp, work.pop()
    #dotted_name: NAME ('.' NAME)*
    def dotted_name(self, tokens):
        self.trace(f'{sys._getframe().f_code.co_name}:{tokens[0].type},{tokens[0].literal}')
        work = []
        tokens_tmp = tokens
        path = ''
        while len(tokens_tmp) != 0 and tokens_tmp[0].type in ['VAR', '.']:
            path += tokens_tmp[0].literal
            tokens_tmp = tokens_tmp[1:]
        work += [Token('NAME', path)]
        return tokens_tmp, work.pop()
    #compound_stmt: if_stmt | while_stmt | for_stmt | do_stmt | funcdef
    def compound_stmt(self, tokens):
        self.trace(f'{sys._getframe().f_code.co_name}:{tokens[0].type},{tokens[0].literal}')
        work = []
        tokens_tmp = tokens
        if len(tokens_tmp) != 0 and tokens_tmp[0].type == 'IF':
            tokens_tmp, token = self.if_stmt(tokens_tmp)
            if token == None:
                printy(f'token is empty!:{sys._getframe().f_code.co_name}')
            work += [token]
        elif len(tokens_tmp) != 0 and tokens_tmp[0].type in ['WL', 'WHILE']:
            tokens_tmp, token = self.while_stmt(tokens_tmp)
            if token == None:
                printy(f'token is empty!:{sys._getframe().f_code.co_name}')
            work += [token]
        elif len(tokens_tmp) != 0 and tokens_tmp[0].type == 'FOR':
            tokens_tmp, token = self.for_stmt(tokens_tmp)
            if token == None:
                printy(f'token is empty!:{sys._getframe().f_code.co_name}')
            work += [token]
        elif len(tokens_tmp) != 0 and tokens_tmp[0].type == 'DO':
            tokens_tmp[0].type = 'WHILE'
            tokens_tmp.insert(1, Token('BOOL', 'True'))
            tokens_tmp, token = self.while_stmt(tokens_tmp)
            if token == None:
                printy(f'token is empty!:{sys._getframe().f_code.co_name}')
            tokens_break = [Token('STMT', 'stmt'), Token('BREAK', 'break')]
            tokens_break, token_break = self.stmt(tokens_break)
            token.children[-1].children += [token_break]
            work += [token]
        elif len(tokens_tmp) != 0 and tokens_tmp[0].type == 'DEF':
            tokens_tmp, token = self.funcdef(tokens_tmp)
            if token == None:
                printy(f'token is empty!:{sys._getframe().f_code.co_name}')
            work += [token]
        else:
            self.error(f'error:expected {sys._getframe().f_code.co_name}!', tokens_tmp)
            return tokens_tmp, None
        return tokens_tmp, work.pop()
    #if_stmt: 'if' test ':' suite (elif_stmt)* [else_stmt]
    def if_stmt(self, tokens):
        self.trace(f'{sys._getframe().f_code.co_name}:{tokens[0].type},{tokens[0].literal}')
        work = []
        tokens_tmp = tokens
        if len(tokens_tmp) != 0 and tokens_tmp[0].type == 'IF':
            token_ope = tokens_tmp[0]
            ope = token_ope.literal
            tokens_tmp, token = self.test(tokens_tmp[1:])
            if token == None:
                printy(f'token is empty!:{sys._getframe().f_code.co_name}')
            work += [token]
            token_ope.children += [work.pop()]
            if len(tokens_tmp) != 0 and tokens_tmp[0].type == ':':
                tokens_tmp, token = self.suite(tokens_tmp[1:])
                if token == None:
                    printy(f'token is empty!:{sys._getframe().f_code.co_name}')
                work += [token]
                token_ope.children += [work.pop()]
                #token_ope.children += [Token('PASS', 'pass')]
                self.reverse_poland += f'{ope} '
                work += [token_ope]
                while len(tokens_tmp) != 0 and tokens_tmp[0].type == 'ELIF':
                    tokens_tmp, token = self.elif_stmt(tokens_tmp)
                    if token == None:
                        printy(f'token is empty!:{sys._getframe().f_code.co_name}')
                    token_ope.children += [token]
                    token_ope = token
                tokens_tmp, token = self.else_stmt(tokens_tmp)
                if token == None:
                    printy(f'token is empty!:{sys._getframe().f_code.co_name}')
                token_ope.children += [token]
                token_ope = token
            else:
                self.error(f'error:expected colon!', tokens_tmp, sys._getframe().f_code.co_name)
                return tokens_tmp, None
        else:
            self.error(f'error:expected {sys._getframe().f_code.co_name}!', tokens_tmp)
            return tokens_tmp, None
        return tokens_tmp, work.pop()
    #elif_stmt: 'elif' test ':' suite
    def elif_stmt(self, tokens):
        self.trace(f'{sys._getframe().f_code.co_name}:{tokens[0].type},{tokens[0].literal}')
        work = []
        tokens_tmp = tokens
        if len(tokens_tmp) != 0 and tokens_tmp[0].type == 'ELIF':
            token_ope = tokens_tmp[0]
            ope = token_ope.literal
            tokens_tmp, token = self.test(tokens_tmp[1:])
            if token == None:
                printy(f'token is empty!:{sys._getframe().f_code.co_name}')
            work += [token]
            token_ope.children += [work.pop()]
            if len(tokens_tmp) != 0 and tokens_tmp[0].type == ':':
                tokens_tmp, token = self.suite(tokens_tmp[1:])
                if token == None:
                    printy(f'token is empty!:{sys._getframe().f_code.co_name}')
                work += [token]
                token_ope.children += [work.pop()]
                self.reverse_poland += f'{ope} '
                work += [token_ope]
            else:
                self.error(f'error:expected colon!', tokens_tmp, sys._getframe().f_code.co_name)
                return tokens_tmp, None
        else:
            self.error(f'error:expected {sys._getframe().f_code.co_name}!', tokens_tmp)
            return tokens_tmp, None
        return tokens_tmp, work.pop()
    #else_stmt: 'else' ':' suite
    def else_stmt(self, tokens):
        self.trace(f'{sys._getframe().f_code.co_name}:{tokens[0].type},{tokens[0].literal}')
        work = []
        tokens_tmp = tokens
        if len(tokens_tmp) != 0 and tokens_tmp[0].type == 'ELSE':
            token_ope = tokens_tmp[0]
            ope = token_ope.literal
            if len(tokens_tmp) != 0 and tokens_tmp[1].type == ':':
                tokens_tmp, token = self.suite(tokens_tmp[2:])
                if token == None:
                    printy(f'token is empty!:{sys._getframe().f_code.co_name}')
                work += [token]
                token_ope.children += [work.pop()]
                self.reverse_poland += f'{ope} '
                work += [token_ope]
            else:
                self.error(f'error:expected colon!', tokens_tmp, sys._getframe().f_code.co_name)
                return tokens_tmp, None
        elif len(tokens_tmp) != 0:
            token_ope = Token('ELSE', 'else')
            ope = token_ope.literal
            work += [Token('PASS', 'pass')]
            token_ope.children += [work.pop()]
            self.reverse_poland += f'{ope} '
            work += [token_ope]
        else:
            self.error(f'error:expected {sys._getframe().f_code.co_name}!', tokens_tmp)
            return tokens_tmp, None
        return tokens_tmp, work.pop()
    #while_stmt: 'while' test ':' suite
    def while_stmt(self, tokens):
        self.trace(f'{sys._getframe().f_code.co_name}:{tokens[0].type},{tokens[0].literal}')
        work = []
        tokens_tmp = tokens
        if len(tokens_tmp) != 0 and tokens_tmp[0].type in ['WL', 'WHILE']:
            token_ope = tokens_tmp[0]
            ope = token_ope.literal
            tokens_tmp, token = self.test(tokens_tmp[1:])
            if token == None:
                printy(f'token is empty!:{sys._getframe().f_code.co_name}')
            work += [token]
            token_ope.children += [work.pop()]
            if len(tokens_tmp) != 0 and tokens_tmp[0].type == ':':
                tokens_tmp, token = self.suite(tokens_tmp[1:])
                if token == None:
                    printy(f'token is empty!:{sys._getframe().f_code.co_name}')
                work += [token]
                token_ope.children += [work.pop()]
                self.reverse_poland += f'{ope} '
                work += [token_ope]
            else:
                self.error(f'error:expected colon!', tokens_tmp, sys._getframe().f_code.co_name)
                return tokens_tmp, None
        else:
            self.error(f'error:expected {sys._getframe().f_code.co_name}!', tokens_tmp)
            return tokens_tmp, None
        return tokens_tmp, work.pop()
    #for_stmt: 'for' atom 'in' testlist ':' suite
    def for_stmt(self, tokens):
        self.trace(f'{sys._getframe().f_code.co_name}:{tokens[0].type},{tokens[0].literal}')
        work = []
        tokens_tmp = tokens
        if not (len(tokens_tmp) != 0 and tokens_tmp[0].type == 'FOR'):
            printy(f'error:FOR expected! remain:{len(tokens_tmp)},token:{tokens_tmp[0].type},{tokens_tmp[0].literal}')
            return tokens_tmp, None
        token_ope = Token('WHILE', 'while')
        tokens_tmp, token = self.atom(tokens_tmp[1:])
        if token == None:
            printy(f'token is empty!:{sys._getframe().f_code.co_name}')
            return tokens_tmp, None
        token_var = token
        if not (len(tokens_tmp) != 0 and tokens_tmp[0].literal == 'in'):
            printy(f'error:COLON expected! remain:{len(tokens_tmp)},token:{tokens_tmp[0].type},{tokens_tmp[0].literal}')
            return tokens_tmp, None
        tokens_tmp, token = self.test(tokens_tmp[1:])
        if token == None:
            printy(f'token is empty2!:{sys._getframe().f_code.co_name}')
            return tokens_tmp, None
        token_list = token
        if not (len(tokens_tmp) != 0 and tokens_tmp[0].literal == ':'):
            printy(f'error:COLON expected! remain:{len(tokens_tmp)},token:{tokens_tmp[0].type},{tokens_tmp[0].literal}')
            return tokens_tmp, None
        tokens_tmp, token = self.suite(tokens_tmp[1:])
        if token == None:
            printy(f'token is empty2!:{sys._getframe().f_code.co_name}')
            return tokens_tmp, None
        token_stmts = self.for_stmt_helper(token_ope, token_var, token_list, token)
        work += [token_stmts]
        return tokens_tmp, work.pop()
    def for_stmt_helper(self, token_ope, token_var, token_list, token_suite):
        ope = token_ope.literal
        tokens_judge = Token.cnv_tokens([('VAR', '#index'), ('COMP', '<'), ('VAR', '#count')])
        tokens_edit, token_edit = self.test(tokens_judge)
        token_ope.children += [token_edit]
        tokens_edit = Token.cnv_tokens([('STMT', 'stmt'), ('VAR', '#index'), ('OPE', '+='), ('NUM', '1')])
        tokens_edit, token_edit = self.stmt(tokens_edit)
        token_suite.children.insert(0, token_edit)
        var = token_var.literal
        tokens_edit = Token.cnv_tokens([('STMT', 'stmt'), ('VAR', var), ('ASSIGN', '='), ('VAR', '#list'), ('LBRACK', '['), ('VAR', '#index'), ('RBRACK', ']')])
        tokens_edit, token_edit = self.stmt(tokens_edit)
        token_suite.children.insert(0, token_edit)
        token_ope.children += [token_suite]
        self.reverse_poland += f'{ope} '
        token_stmts = Token('STMTS', 'stmts')
        ope = token_stmts.literal
        tokens_edit = Token.cnv_tokens([('STMT', 'stmt'), ('VAR', '#index'), ('ASSIGN', '='), ('NUM', '0')])
        tokens_edit, token_edit = self.stmt(tokens_edit)
        token_stmts.children += [token_edit]
        tokens_edit = Token.cnv_tokens([('STMT', 'stmt'), ('VAR', '#list'), ('ASSIGN', '='), ('VAR', '#dummy')])
        tokens_edit, token_edit = self.stmt(tokens_edit)
        printx(f'len(token_edit.children):{len(token_edit.children)}')
        if len(token_edit.children):
            token_edit.children[0].children[1] = token_list
        else:
            token_edit.type = token_list.type
            token_edit.literal = token_list.literal
        token_stmts.children += [token_edit]
        tokens_edit = Token.cnv_tokens([('STMT', 'stmt'), ('VAR', '#count'), ('ASSIGN', '='), ('VAR', 'len'), ('LPAREN', '('), ('VAR', '#list'), ('RPAREN', ')')])
        tokens_edit, token_edit = self.stmt(tokens_edit)
        token_stmts.children += [token_edit]
        token_stmts.children += [token_ope]
        self.reverse_poland += f'{ope} '
        return token_stmts
    #funcdef: 'def' NAME parameters':' suite
    def funcdef(self, tokens):
        self.trace(f'{sys._getframe().f_code.co_name}:{tokens[0].type},{tokens[0].literal}')
        work = []
        tokens_tmp = tokens
        if len(tokens_tmp) != 0 and tokens_tmp[0].type == 'DEF':
            token_ope = Token('FUNC_DEF', 'func_def')
            self.reverse_poland += f'{token_ope.literal} '
            ope = token_ope.literal
            tokens_tmp = tokens_tmp[1:]
            if len(tokens_tmp) != 0 and tokens_tmp[0].type == 'VAR':
                token = tokens_tmp[0]
                token_ope.literal = token.literal
                #self.reverse_poland += f'{token.literal} '
                tokens_tmp = tokens_tmp[1:]
                #work += [token]
                #token_ope.children += [work.pop()]
                if len(tokens_tmp) != 0 and tokens_tmp[0].type == 'LPAREN':
                    printx(tokens_tmp[0].type)
                    tokens_tmp, token = self.parameters(tokens_tmp)
                    if token == None:
                        printy(f'token is empty!:{sys._getframe().f_code.co_name}')
                    work += [token]
                    token_ope.children += [work.pop()]
                    self.reverse_poland += f'{ope} '
                    self.print_token_type_list(tokens_tmp)
                    if len(tokens_tmp) != 0 and tokens_tmp[0].type == ':':
                        tokens_tmp, token = self.suite(tokens_tmp[1:])
                        if token == None:
                            printy(f'token is empty!:{sys._getframe().f_code.co_name}')
                        work += [token]
                        token_ope.children += [work.pop()]
                        self.reverse_poland += f'{ope} '
                        work += [token_ope]
                    else:
                        self.error(f'error:expected colon!', tokens_tmp, sys._getframe().f_code.co_name)
                        return tokens_tmp, None
            else:
                self.error(f'error:expected VAR!', tokens_tmp, sys._getframe().f_code.co_name)
                return tokens_tmp, None

        else:
            self.error(f'error:expected DEF!', tokens_tmp, sys._getframe().f_code.co_name)
            return tokens_tmp, None
        return tokens_tmp, work.pop()
    #suite: NEWLINE INDENT stmt+ DEDENT 
    def suite(self, tokens):
        self.trace(f'{sys._getframe().f_code.co_name}:{tokens[0].type},{tokens[0].literal}')
        work = []
        token_ope = Token('STMTS', 'stmts')
        ope = token_ope.type
        tokens_tmp = tokens
        if len(tokens_tmp) >= 3 and tokens_tmp[0].type in ['INDENT']:
            tokens_tmp = tokens_tmp[1:]
            while len(tokens_tmp):
                tokens_tmp, token = self.stmt(tokens_tmp)
                if token == None:
                    printy(f'token is empty!:{sys._getframe().f_code.co_name}')
                work += [token]
                token_ope.children += [work.pop()]
                if len(tokens_tmp) and tokens_tmp[0].type == 'DEDENT':
                    break
            work += [token_ope]
            self.reverse_poland += f'{ope} '
            if len(tokens_tmp) != 0 and tokens_tmp[0].type in ['DEDENT']:
                tokens_tmp = tokens_tmp[1:]
            else:
                self.error(f'error:expected DEDENT!', tokens_tmp)
                return tokens_tmp, None
        else:
            self.error(f'error:expected INDENT!', tokens_tmp)
            return tokens_tmp, None
        return tokens_tmp, work.pop()
    #parameters: '(' [typedargslist] ')'
    def parameters(self, tokens):
        self.trace(f'{sys._getframe().f_code.co_name}:{tokens[0].type},{tokens[0].literal}')
        token = None
        if tokens[0].literal == '(':
            tokens_tmp, token = self.typedargslist(tokens[1:])
            if tokens_tmp[0].literal != ')':
                printy("error:not ')'")
            else:
                tokens = tokens_tmp[1:]
        else:
            printy(f'error:parameters not expect! remain:{len(tokens)},token:{tokens[0].type},{tokens[0].literal}')
        return tokens, token
    #typedargslist: NAME (',' NAME)*
    def typedargslist(self, tokens):
        self.trace(f'{sys._getframe().f_code.co_name}:{tokens[0].type},{tokens[0].literal}')
        token_ope = Token('PARA_LIST', 'para_list')
        tokens_tmp = tokens
        if tokens_tmp[0].type == 'VAR':
            token = tokens_tmp[0]
            token_ope.children += [token]
            self.reverse_poland += f'{tokens_tmp[0].literal} '
            tokens_tmp = tokens_tmp[1:]
            while len(tokens_tmp) != 0 and tokens_tmp[0].literal == ',':
                tokens_tmp = tokens_tmp[1:]
                if tokens_tmp[0].type == 'VAR':
                    token = tokens_tmp[0]
                    token_ope.children += [token]
                    self.reverse_poland += f'{tokens_tmp[0].literal} '
                    tokens_tmp = tokens_tmp[1:]
        else:
            printy(f'error:typedargslist not expect! remain:{len(tokens)},token:{tokens[0].type},{tokens[0].literal}')
        return tokens_tmp, token_ope

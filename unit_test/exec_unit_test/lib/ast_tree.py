from lib import printx, printy

class AstTree():
    def __init__(self) -> None:
        pass
    def exec(self, token):
        ast_tree = self.create_ast(token)
        printx(ast_tree)
        return ast_tree
    def create_ast(self, token):
        if token == None:
            printy('token is empty!')
            return
        #print('-' * 25)
        token.print()
        if token.type == 'IMPORT':
            return f"['import', '{token.literal}']"
        elif token.type == 'STMTS':
            list_tmp = []
            printx(f'token.children:{len(token.children)}')
            for child in token.children:
                list_tmp += [self.create_ast(child)]
            csv = ','.join(list_tmp)
            return f"['stmts', {csv}]"
        elif token.type == 'STMT':
            return f"['stmt', {self.create_ast(token.children[0])}]"
        elif token.type == 'IIF':
            return f"['iif', {self.create_ast(token.children[0])}, {self.create_ast(token.children[1])}, {self.create_ast(token.children[2])}]"
        elif token.type in ['IF', 'ELIF']:
            return f"['if', {self.create_ast(token.children[0])}, {self.create_ast(token.children[1])}, {self.create_ast(token.children[2])}]"
        elif token.type == 'ELSE':
            return f"['else', {self.create_ast(token.children[0])}]"
        elif token.type == 'PASS':
            return f"['pass', 'pass']"
        elif token.type == 'BREAK':
            return f"['break', 'break']"
        elif token.type == 'CONTINUE':
            return f"['continue', 'continue']"
        elif token.type in ['WL', 'WHILE']:
            return f"['wl', {self.create_ast(token.children[0])}, {self.create_ast(token.children[1])}]"
        elif token.type == 'FUNC_CALL':
            return f"['func_call', '{token.literal}', {self.create_ast(token.children[0])}]"
        elif token.type == 'FUNC_DEF':
            return f"['func_def', '{token.literal}', {self.create_ast(token.children[0])}, {self.create_ast(token.children[1])}]"
        elif token.type == 'RETURN':
            return f"['return', {self.create_ast(token.children[0])}]"
        elif token.type == 'PARA_LIST':
            args = [f"'{token.literal}'" for token in token.children]
            return f"[{','.join(args)}]"
        elif token.type == 'LIST':
            list_tmp = [f"{self.create_ast(x)}" for x in token.children]
            return f"['list_new', {','.join(list_tmp)}]"
        elif token.type == 'DICT':
            #printx(f'{token.children[0].literal} {token.children[0].children[0].literal}')
            list_tmp = [f"[{self.create_ast(x)}, {self.create_ast(x.children[0])}]" for x in token.children]
            return f"['dict_new', {','.join(list_tmp)}]"
        elif token.type == 'LIST_REF':
            list_tmp = [f"{self.create_ast(x)}" for x in token.children]
            return f"['list_ref', ['var_ref', '{token.literal}'], {','.join(list_tmp)}]"
        elif token.type == 'DICT_REF':
            return f"['dict_ref', ['var_ref', '{token.literal}'], {self.create_ast(token.children[0])}]"
        elif token.type == 'ARG_LIST':
            args = [f"{self.create_ast(x)}" for x in token.children]
            return f"{','.join(args)}"
        elif token.type == 'ASSIGN':
            if token.children[0].type == 'LIST_REF':
                #return f"['list_upd', '{token.children[0].literal}', {self.create_ast(token.children[0].children[0])}, {self.create_ast(token.children[1])}]"
                return f"['list_upd', {self.create_ast(token.children[0])}, {self.create_ast(token.children[1])}]"
            elif token.children[0].type == 'DICT_REF':
                return f"['dict_upd', '{token.children[0].literal}', '{token.children[0].children[0].literal}', {self.create_ast(token.children[1])}]"
            else:
                return f"['var_def', '{token.children[0].literal}', {self.create_ast(token.children[1])}]"
        elif token.type == 'FACT':
            return f"['{token.literal}', {self.create_ast(token.children[0])}]"
        elif token.type == 'NUM':
            return f"['num', {token.literal}]"
        elif token.type == 'STR':
            return f"['str', '{token.literal}']"
        elif token.type == 'BOOL':
            return f"['bool', {token.literal}]"
        elif token.type == 'NONE':
            return f"['none', {token.literal}]"
        elif token.type == 'VAR':
            return f"['var_ref', '{token.literal}']"
        else:
            return f"['{token.literal}', {self.create_ast(token.children[0])}, {self.create_ast(token.children[1])}]"

from lib import printx, printy

class Token():
    def __init__(self, type, literal):
        super().__init__()
        self.type = type
        self.literal = literal
        self.children = []
        self.is_disp = False
    def print(self, is_error=False):
        if not is_error:
            printx(f'type:{self.type},literal:{self.literal}')
        else:
            printy(f'type:{self.type},literal:{self.literal}')
    def info(self):
        return f'type:{self.type},literal:{self.literal}'
    def print_token_tree(self):
        self._print_token_tree_helper(self)
    def _print_token_tree_helper(self, token, depth=0, tree=''):
        printx(f'{tree}', end='')
        if token == None:
            self.print('token is empty!')
            return
        token.print()
        count = len(token.children)
        for index, child in enumerate(token.children):
            tree = tree.replace('├─', '│ ').replace('└─', '  ')
            tmp = '├─' if index < count - 1 else '└─'
            token._print_token_tree_helper(child, depth + 1, tree + tmp)
    @classmethod
    def print_list(cls, tokens):
        for index, token in enumerate(tokens):
            printx(f'{str(index).zfill(4)}:', end='')
            token.print()
    @classmethod
    def cnv_tokens(cls, token_info_list):
        tokens = [Token(type, literal) for (type, literal) in token_info_list]
        return tokens        

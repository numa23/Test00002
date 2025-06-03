import unicodedata
from lib import Lexer, AstTree, ExecTree, Parser, Cloud, printx
import sys
import os
import datetime

input = []
if len(sys.argv) == 1:
    input = 'x = (1 + 2) * 3'   # ['var_def', 'x', ['*', ['+', ['num', 1], ['num', 2]], ['num', 3]]]
    #input = '(1 + 2) * 3'   # ['var_def', 'x', ['*', ['+', ['num', 1], ['num', 2]], ['num', 3]]]
else:
    arg1 = sys.argv[1]
    if '.txt' in arg1:
        cloud = Cloud()
        arglist = sys.argv[1:]
        arglist[0] = arglist[0].replace('.\\', '')
        cloud.dict['argv'] = arglist
        with open(arg1, encoding='utf-8', newline=None) as f:
            input = f.read()
    else:
        input = arg1

Cloud.log_path_name = os.path.splitext(__file__)[0] + '.log'
Cloud.is_disp = False
printx(datetime.datetime.now(), mode='w')

printx('[input]')
printx(f'{input}')
printx('[Lexer]')
tokens = Lexer.cnv_tokens(input)
Lexer.print(tokens)
#exit()
printx('[Parser]')
parser = Parser()
token = parser.exec(tokens)
token.print_token_tree()
printx('[AstTree]')
tree = AstTree()
ast_tree = tree.exec(token)
printx('[ExecTree]')
calc = ExecTree()
result = calc.exec_calc(eval(ast_tree))

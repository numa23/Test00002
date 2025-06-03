import unicodedata
from lib import Token, printx, printy

class Lexer:
    def __init__(self, input):
        self.ALPHA_LIST = ['_']
        self.ALPHA_LIST += [chr(x) for x in range(ord('a'), ord('z') + 1)]
        self.ALPHA_LIST += [chr(x) for x in range(ord('A'), ord('Z') + 1)]
        self.NUM_LIST = [chr(x) for x in range(ord('0'), ord('9') + 1)]
        self.ALPHA_NUM_LIST = self.ALPHA_LIST + self.NUM_LIST
        self.is_2byte = lambda x: True if len(x) > 0 and unicodedata.east_asian_width(x) in ['W', 'F'] else False
        self.OPE_LIST = ['+', '-', '*', '@', '/', '%', '&', '|', '^', '<<', '>>', '**', '//']
        self.SPEOPE_LIST = ['+=', '-=', '*=', '@=', '/=', '%=', '&=', '|=', '^=', '<<=', '>>=', '**=', '//=', '++']
        self.COMP_LIST = ['<', '>', '==', '>=', '<=', '<>', '!=', 'in', 'is', 'not']
        self.CTRL_LIST = ['import', 'if', 'while', 'do', 'continue', 'break', 'for', 'def', 'return', 'lambda', 'pass']
        self.BOOL_LIST = ['True', 'False']
        self.WORD_DICT = {}
        self.WORD_DICT[','] = 'COMMA'
        self.WORD_DICT['='] = 'ASSIGN'
        self.WORD_DICT['('] = 'LPAREN'
        self.WORD_DICT[')'] = 'RPAREN'
        self.WORD_DICT['['] = 'LBRACK'
        self.WORD_DICT[']'] = 'RBRACK'
        self.WORD_DICT['{'] = 'LBRACE'
        self.WORD_DICT['}'] = 'RBRACE'
        self.input = input
        self.cur_char = ''
        self.next_char = ''
        self.posi = 0
        self._read_char()
    def next_token(self):
        token = None
        while self.cur_char == '#':
            while self.cur_char  != '\n':
                self._read_char()
            self._read_char()
        two_words = self.cur_char + self.next_char
        three_words = self.cur_char + self.next_char + self.next2_char
        if self.cur_char in self.ALPHA_LIST or self.is_2byte(self.cur_char):
            word = self.cur_char
            while self.next_char in self.ALPHA_NUM_LIST or self.is_2byte(self.next_char):
                self._read_char()
                word += self.cur_char
            if word in self.CTRL_LIST:
                token = Token(word.upper(), word)
            elif word in self.COMP_LIST:
                token = Token('COMP', word)
            elif word in self.BOOL_LIST:
                token = Token('BOOL', word)
            elif word in ['if', 'elif', 'else']:
                token = Token(word.upper(), word)
            else:
                token = Token('NAME', word)
        elif self.cur_char in self.NUM_LIST:
            number = self.cur_char
            while self.next_char in self.NUM_LIST:
                self._read_char()
                number += self.cur_char
            token = Token('NUM', number)
        elif three_words in self.SPEOPE_LIST:
            token = Token('OPE', three_words)
            self._read_char()
            self._read_char()
        elif two_words in self.SPEOPE_LIST:
            token = Token('OPE', two_words)
            self._read_char()
        elif two_words in self.OPE_LIST:
            token = Token('OPE', two_words)
            self._read_char()
        elif two_words in self.COMP_LIST:
            token = Token('COMP', two_words)
            self._read_char()
        elif self.cur_char in self.SPEOPE_LIST:
            token = Token('OPE', two_words)
        elif self.cur_char in self.OPE_LIST:
            token = Token('OPE', self.cur_char)
        elif self.cur_char in self.COMP_LIST:
            token = Token('COMP', self.cur_char)
        elif self.cur_char in self.WORD_DICT.keys():
            token = Token(self.WORD_DICT[self.cur_char], self.cur_char)
        elif self.cur_char == '\n':
            token = Token('CR', 'CR')
        elif self.cur_char == ' ':
            space = ' '
            while self.next_char == ' ':
                self._read_char()
                space += self.cur_char
            if self.next_char == '#':
                token = Token('SP', ' ')
            elif space == ' ':
                token = Token('SP', ' ')
            elif len(space) % 4:
                token = Token('SP', str(len(space)))
            else:
                token = Token('TAB', str(len(space) // 4))
        elif self.cur_char == '':
            token = Token('EOF', '')
        else:
            token = Token(self.cur_char, self.cur_char)
        self._read_char()
        return token
    def _read_char(self):
        self.cur_char = '' if self.posi >= len(self.input) else self.input[self.posi] 
        self.next_char = '' if self.posi + 1 >= len(self.input) else self.input[self.posi + 1]
        self.next2_char = '' if self.posi + 2 >= len(self.input) else self.input[self.posi + 2]
        self.posi += 1
    @classmethod
    def cnv_tokens(cls, input):
        # Lexer
        do_print_token = False
        tokens = []
        tokens += [Token('STMTS', 'stmts')]
        lex = cls(input)
        token_prev = Token('CR', 'CR')
        quot_dict = {"'": 0, '"': 1}
        quot_list = ["'", '"']
        count_tab = 0
        while(True):
            token = lex.next_token()
            if token.literal == ' ':
                continue
            if token.type == 'CR' and token_prev.type == 'CR':
                continue
            if token.type == 'CR' and token_prev.type == 'TAB':
                tokens += [Token('PASS', 'pass')]
            printx(f'prev:({token_prev.info()}),cur:({token.info()})') if do_print_token else 'pass'
            if token.type in quot_list:
                quot_type = quot_dict[token.type]
                string = ''
                token = lex.next_token()
                while token.type != quot_list[quot_type]:
                    if token.type == 'SP' and token.literal != ' ':
                        token.literal = ' ' * int(token.literal)
                    string += token.literal.replace('"', '\"').replace("'", '\'')
                    token = lex.next_token()
                    if token.type == 'EOF':
                        printy("Not found 1xQuot('). ")
                        break
                if token_prev.type == 'VAR' and token_prev.literal == 'f':
                    tokens.pop(-1)
                    string = "'" + string.replace('{', "' + str(").replace('}', ") + '") + "'"
                    tokens2 = Lexer.cnv_tokens(string)
                    tokens += tokens2[2:]
                else:
                    token = Token('STR', string.replace('\\', '/')) if token.type != 'EOF' else token
            if token.type == 'NAME':
                token.type = 'VAR'
            if token.type == 'OPE' and token.literal == '++':
                tokens += [Token('OPE', '+=')]
                tokens += [Token('NUM', '1')]
                continue
            if token_prev.type == 'CR':
                if token.type == 'TAB':
                    if count_tab != int(token.literal):
                        tokens += [Token('INDENT', 'indent') if count_tab < int(token.literal) else Token('DEDENT', 'dedent')]
                        count_tab = int(token.literal)
                else:
                    if count_tab > 0:
                        for index in range(count_tab):
                            tokens += [Token('DEDENT', 'dedent')]
                    count_tab = 0
                if token.type != 'EOF':
                    tokens += [Token('STMT', 'stmt')]
            if token_prev.type not in ['CR', 'TAB'] and token.type == 'IF':
                token.type = 'IIF'
            if token.type in ['ELIF', 'ELSE']:
                if tokens[-1].type == 'STMT':
                    tokens.pop()
            token_prev = token
            if token.type in ['CR', 'TAB', "'"]:
                continue
            if token.type == 'EOF':
                break
            tokens += [token]
        return tokens
    @classmethod
    def print(cls, tokens):
        [token.print() for token in tokens]

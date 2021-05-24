import re

NUM     = 1     # number e.g. '123'
ID      = 2     # symbol e.g. 'LOOP'
OP      = 3     # = ; ( ) @ + - & | !
ERROR   = 4     # error in file

class lex(object):

    _num_re = r'\d+'
    _id_start = r'\w_.$:'
    _id_re = '['+_id_start+']['+_id_start+r'\d]*'
    _op_re = r'[=;()@+\-&|!]'
    _word = re.compile(_num_re+'|'+_id_re+'|'+_op_re)
    _comment = re.compile('//.*$')

    def __init__(self, file_name):
        file = open(file_name, 'r')
        self._lines = file.read()
        self._tokens = self._tokenize(self._lines.split('\n'))
        self.cur_command = []
        self.cur_token = (ERROR,0)   
    
    def __str__(self):
        pass
        
    def has_more_commands(self):
        return self._tokens != []
        
    def next_command(self):
        self.cur_command = self._tokens.pop(0)
        self.next_token()
        return self.cur_command
        
    def has_next_token(self):
        return self.cur_command != []
        
    def next_token(self):
        if self.has_next_token():
            self.cur_token = self.cur_command.pop(0)
        else:
            self.cur_token = (ERROR, 0)
        return self.cur_token
        
    def peek_token(self):
        if self.has_next_token():
            return self.cur_command[0]
        else:
            return (ERROR, 0)
        
    def _tokenize(self, lines):
        return [t for t in [self._tokenize_line(l) for l in lines] if t!=[]]
    
    def _tokenize_line(self, line):
        return [self._token(word) for word in self._split(self._remove_comment(line))]

    def _remove_comment(self, line):
        return self._comment.sub('', line)

    def _split(self, line):
        return self._word.findall(line)
        
    def _token(self, word):
        if   self._is_num(word):     return (NUM, word)
        elif self._is_id(word):      return (ID, word)
        elif self._is_op(word):      return (OP, word)
        else:                        return (ERROR, word)
            
    def _is_op(self, word):
        return self._is_match(self._op_re, word)
        
    def _is_num(self, word):
        return self._is_match(self._num_re, word)
        
    def _is_id(self, word):
        return self._is_match(self._id_re, word)
        
    def _is_match(self, re_str, word):
        return re.match(re_str, word) != None

class parser(object):

    # Enum for instruction type 
    A_COMMAND = 0
    C_COMMAND = 1
    L_COMMAND = 2
    
    def __init__(self, file):
        self.lex = lex(file)
        self._init_cmd_info()
    
    def _init_cmd_info(self):
        self._cmd_type = -1
        self._symbol = ''
        self._dest = ''
        self._comp = ''
        self._jmp = ''
    
    def __str__(self):
        pass
        
    def has_more_commands(self):
        return self.lex.has_more_commands()
    
    # Increment to next line
    def advance(self):
        self._init_cmd_info()

        self.lex.next_command()
        tok, val = self.lex.cur_token

        if tok == OP and val == '@':
            self._a_command()
        elif tok == OP and val == '(':
            self._l_command()
        else:
            self._c_command(tok, val)

    def command_type(self):
        return self._cmd_type 
        
    def symbol(self):
        return self._symbol
    
    def dest(self):
        return self._dest
    
    def comp(self):
        return self._comp
        
    def jmp(self):
        return self._jmp
        
    # @symbol or @number
    def _a_command(self):
        self._cmd_type = parser.A_COMMAND
        tok_type, self._symbol = self.lex.next_token()
        
    # (symbol)
    def _l_command(self):
        self._cmd_type = parser.L_COMMAND
        tok_type, self._symbol = self.lex.next_token()

    def _c_command(self, tok1, val1):
        self._cmd_type = parser.C_COMMAND
        comp_tok, comp_val = self._get_dest(tok1, val1)
        self._get_comp(comp_tok, comp_val)
        self._get_jump()

    # Get the 'dest' part if any.  Return the first token of the 'comp' part.
    def _get_dest(self, tok1, val1):
        tok2, val2 = self.lex.peek_token()
        if tok2 == OP and val2 == '=':
            self.lex.next_token()
            self._dest = val1
            comp_tok, comp_val = self.lex.next_token()
        else:
            comp_tok, comp_val = tok1, val1
        return (comp_tok, comp_val)
    
    # Get the 'comp' part - must be present.
    def _get_comp(self, tok, val):
        if tok == OP and (val == '-' or val == '!'):
            tok2, val2 = self.lex.next_token()
            self._comp = val+val2
        elif tok == NUM or tok == ID:
            self._comp = val
            tok2, val2 = self.lex.peek_token()
            if tok2 == OP and val2 != ';':
                self.lex.next_token()
                tok3, val3 = self.lex.next_token()
                self._comp += val2+val3
        
    # Get the 'jump' part if any
    def _get_jump(self):
        tok, val = self.lex.next_token()
        if tok == OP and val == ';':
            jump_tok, jump_val = self.lex.next_token()
            self._jmp = jump_val

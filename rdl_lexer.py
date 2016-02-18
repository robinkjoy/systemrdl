import re
from ply import lex

class RDLLexer():

    # Build the lexer
    def build(self,**kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def input(self, text):
        self.lexer.input(text)

    def token(self):
        self.last_token = self.lexer.token()
        return self.last_token
    
    keywords = (
            '_BOOL', 'ADDRMAP', 'REG', 'REGFILE', 'FIELD', 'ALL',
            'REF', 'EXTERNAL', 'INTERNAL', 'ALIAS', 'ENUM',
            'PROPERTY', 'TYPE', 'DEFAULT', 'COMPONENT',
            # Property type
            'BOOLEAN', 'STRING', 'NUMBER',
            # Property Names
            'NAME', 'DESC', 'ARBITER', 'RSET', 'RCLR', 'WOCLR', 'WOSET',
            'WE', 'WEL', 'SWWE', 'SWWEL', 'HWSET', 'HWCLR', 'SWMOD',
            'SWACC', 'STICKY', 'STICKYBIT', 'INTR', 'ANDED', 'ORED',
            'XORED', 'COUNTER', 'OVERFLOW', 'SHAREDEXTBUS', 'ERREXTBUS',
            'RESET', 'LITTLEENDIAN', 'BIGENDIAN', 'RSVDSET', 'RSVDSETX',
            'BRIDGE', 'SHARED', 'MSB0', 'LSB0', 'SYNC', 'ASYNC',
            'CPUIF_RESET', 'FIELD_RESET', 'ACTIVEHIGH', 'ACTIVELOW',
            'SINGLEPULSE', 'UNDERFLOW', 'INCR', 'DECR', 'INCRWIDTH',
            'DECRWIDTH', 'INCRVALUE', 'DECRVALUE', 'SATURATE',
            'DECRSATURATE', 'THRESHOLD', 'DECRTHRESHOLD', 'DONTCOMPARE',
            'DONTTEST', 'ALIGNMENT', 'REGWIDTH', 'FIELDWIDTH',
            'SIGNALWIDTH', 'ACCESSWIDTH', 'SW', 'HW', 'ADDRESSING',
            'PRECEDENCE', 'ENCODE', 'RESETSIGNAL', 'CLOCK', 'MASK',
            'ENABLE', 'HWENABLE', 'HWMASK', 'HALTMASK', 'HALTENABLE',
            'HALT', 'NEXT',
            # Property Value
            'TRUE', 'FALSE', 'RW', 'WR', 'R', 'W', 'NA', 'COMPACT',
            'REGALIGN', 'FULLALIGN',
            # Property Modifier
            'POSEDGE', 'NEGEDGE', 'BOTHEDGE', 'LEVEL', 'NONSTICKY'
            )
    
    keyword_map = {}
    for keyword in keywords:
        if keyword == '_BOOL':
            keyword_map['_Bool'] = keyword
        else:
            keyword_map[keyword.lower()] = keyword

    tokens = keywords + (
            'ID', 'NUM', 'WNUM', 'STR', 'LBRACE', 'RBRACE', 'LSQ',
            'RSQ', 'LPAREN', 'RPAREN', 'AT', 'OR', 'SEMI', 'COLON',
            'COMMA', 'DOT', 'DREF', 'EQ', 'INC', 'MOD'
            )

    t_LBRACE = r'{'
    t_RBRACE  = r'}'
    t_LSQ    = r'\['
    t_RSQ    = r'\]'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_AT     = r'@'
    t_OR     = r'\|'
    t_SEMI   = r';'
    t_COLON  = r':'
    t_COMMA  = r','
    t_DOT    = r'\.'
    t_DREF   = r'->'
    t_EQ     = r'='
    t_INC    = r'\+='
    t_MOD    = r'%='

    t_ignore = ' \t'

    def t_STR(self, t):
        r'"[^"]*"'
        t.value = t.value.lstrip('"').rstrip('"')
        return t

    def t_WNUM(self, t):
        r'(\d+)\'([bhd])([0-9a-fA-F_]+)'
        (width, radix, number) = re.search('(\d+)\'([bhd])([0-9a-fA-F_]+)', t.value).groups(0)
        try:
            value = int(number.replace('_', ''), {'b': 2, 'd': 10, 'h': 16}[radix])
            t.value = (int(width), value)
            return t
        except ValueError:
            print ("Illegal Verilog style number %s" % t.value)

    def t_NUM(self, t):
        r'0x[\da-fA-F]+|\d+'
        t.value = int(t.value, base=0)
        return t

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        t.type = self.keyword_map.get(t.value,'ID')    # Check for reserved words
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")
        
    def t_error(self, t):
        print ("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)
        
    # Comments
    def t_comment(self, t):
        r' (/\*(.|\n)*?\*/)|//.*'
        t.lineno += t.value.count('\n')

    # Test it output
    def test(self,data):
        self.lexer.input(data)
        while True:
             tok = self.lexer.token()
             if not tok: 
                 break
             print(tok)

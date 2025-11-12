import ply.lex as lex

reserved = {
    'int':'INT','float':'FLOAT','bool':'BOOL','string':'STRING',
    'if':'IF','else':'ELSE','while':'WHILE','for':'FOR','return':'RETURN',
    'true':'TRUE','false':'FALSE','Console':'CONSOLE','WriteLine':'WRITELINE',
    'new':'NEW','List':'LIST'
}

tokens = [
    'ID','NUMBER','STRING_LITERAL',
    'PLUS','MINUS','MULT','DIV',
    'EQ','NE','GT','LT','GE','LE',
    'ASSIGN','LPAREN','RPAREN','LBRACE','RBRACE','SEMICOLON','COMMA','DOT'
] + list(reserved.values())

t_PLUS=r'\+'; t_MINUS=r'-'; t_MULT=r'\*'; t_DIV=r'/'
t_EQ=r'=='; t_NE=r'!='; t_GE=r'>='; t_LE=r'<='; t_GT=r'>'; t_LT=r'<'
t_ASSIGN=r'='
t_LPAREN=r'\('; t_RPAREN=r'\)'; t_LBRACE=r'\{'; t_RBRACE=r'\}'
t_SEMICOLON=r';'; t_COMMA=r','; t_DOT=r'\.'
t_STRING_LITERAL = r'\"([^\\\"]|\\.)*\"'

def t_ID(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

def t_COMMENT(t):
    r'//.*'
    pass

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Error léxico: {t.value[0]!r} en línea {t.lexer.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()

import ply.lex as lex

class MyLexer(object):

    # Key words
    def __init__(self):
        self.keywords = {
            'program': 'PROGRAM',
            'if': 'IF',
            'else': 'ELSE',
            'vars': 'VARS',
            'int': 'INT',
            'for': 'FOR',
            'while': 'WHILE',
            'call': 'CALL',
            'body': 'BODY',
            'read': 'READ',
            'float': 'FLOAT',
            'char': 'CHAR',
            'bool': 'BOOL',
            'return': 'RETURN',
            'main': 'MAIN',
            'void': 'VOID',
            'func': 'FUNC',
            'to': 'TO',
            'print': 'PRINT',
            'True' : 'TRUE',
            'False' : 'FALSE'
    }

    # Tokens based on the parser

    tokens = ['SEMICOLON', 'LEFTBRACKET', 'RIGHTBRACKET', 'GREATER', 'LESS', 'NOTEQUAL', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
            'LEFTPAREN', 'RIGHTPAREN', 'ID', 'CTE_I', 'CTE_F', 'CTE_CH', 'COLON', 'ASSIGNMENT', 'CTE_STRING', 'COMMA', 'PROGRAM', 'PRINT',
            'IF', 'FOR', 'ELSE', 'VARS', 'INT', 'FLOAT', 'CHAR', 'RIGHTSQBRACKET', 'LEFTSQBRACKET', 'MAIN', 'BODY', 'TYPE_SIMPLE',
            'VARIABLE', 'BODY_RETURN', 'PARAMS', 'CALL', 'READ', 'EQUAL', 'FUNC', 'VOID', 'RETURN', 'TO', 'WHILE', 'OR', 'AND', 'BOOL', 'TRUE', 'FALSE']

    # Regular expressions

    t_SEMICOLON = r'\;'
    t_LEFTBRACKET = r'\{'
    t_RIGHTBRACKET = r'\}'
    t_GREATER = r'\>'
    t_LESS = r'\<'
    t_NOTEQUAL = r'\!='
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'\/'
    t_LEFTPAREN = r'\('
    t_RIGHTPAREN = r'\)'
    t_COLON = r'\:'
    t_ASSIGNMENT = r'\='
    t_EQUAL = r'\=='
    t_CTE_STRING = r'\".*\"'
    t_COMMA = r'\,'
    t_RIGHTSQBRACKET = r'\]'
    t_LEFTSQBRACKET = r'\['
    t_OR = r'\|'
    t_AND = r'\&'

    # A string containing ignored characters (spaces and tabs)
    t_ignore  = ' \t'


    # Regular expression with some action

    # Define an ID
    def t_ID(self,t):
        r'[A-za-z]([A-za-z]|[0-9])*'
        if t.value in self.keywords:
            t.type = self.keywords.get(t.value, 'ID')
        return t

    # Define a float number
    def t_CTE_F(self,t):
        r'[0-9]+(\.([0-9]+)?([eE][-+]?[0-9]+)?|[eE][-+]?[0-9]+)'
        t.value = float(t.value)
        return t
    
    # Define a variable int
    def t_CTE_I(self,t):
        r'[1-9][0-9]*'
        t.value = int(t.value)
        return t

    # Define a variable int
    def t_CTE_CH(self,t):
        r'\".*\"' 
        t.value = int(t.value)
        return t

    # Define a new line or multiple new lines
    def t_newline(self,t):
        r'\n+'
        t.lexer.lineno += len(t.value)


    # Define a comment
    def t_comment(self,t):
        r'\//.*'
        pass


    def t_error(self,t):
        print("Lexical error ' {0} ' found in line ' {1} ' ".format(t.value[0], t.lineno))
        t.lexer.skip(1)

     
     # Test its output
    def test(self,data):
        lexer = self.build()
        lexer.input(data)
        lexer.lineno = 1
        while True:
            tok = lexer.token()
            if not tok: 
                break
            print(tok)

    # Build the lexer
    def build(self,**kwargs):
        lexer = lex.lex(module=self, **kwargs)
        
        return lexer

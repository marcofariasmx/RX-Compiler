import sys
import ply.yacc as yacc

from lexer import MyLexer

from FuncsDir_Vars_Table import FuncsDir_Vars_Table

tokens = MyLexer.tokens

#Create DirFunc
dirTable = FuncsDir_Vars_Table()

# Grammar declaration

def p_program(p):
    '''program      :  PROGRAM program_id SEMICOLON globalVars MAIN LEFTPAREN RIGHTPAREN body 
       globalVars   :  vars globalFuncs
                    |  empty
       globalFuncs  :  functions globalFuncs globalVars
                    |  empty
    '''
    p[0] = "COMPILED"

def p_expression_program_id(p):
        '''
        program_id : ID
        '''

        #Add id-name and type program a DirFunc
        dirTable.insertFunction(p[1], 'program', 1, None, None)


def p_vars(p):
    ''' vars    :  VARS vars2
        vars2   :  type_simple vars1 SEMICOLON 
                |  type_simple vars1 SEMICOLON vars2
        vars1   :  variable
                |  variable COMMA vars1
    '''

    #If current Func doesn’t have a VarTable then Create VarTable and link it to current Func
    #if
    #dirTable.insertVariable()
    print("----VARS-----")
    #print(type(p))
    print(*p)

def p_functions(p):
    ''' functions    :   FUNC functionType
        functionType :   type_simple ID LEFTPAREN params RIGHTPAREN body_return
                     |   VOID ID LEFTPAREN RIGHTPAREN body
    '''
    print("-----FUNCTIONS------")
    print(*p)

def p_type_simple(p):
    ''' type_simple :   INT
                    |   FLOAT
                    |   CHAR
    '''
    print("-----TYPE SIMPLE------")
    print(*p)
    
def p_variable(p):
    ''' variable    :   ID
                    |   ID LEFTSQBRACKET exp RIGHTSQBRACKET
                    |   ID LEFTSQBRACKET exp RIGHTSQBRACKET LEFTSQBRACKET exp RIGHTSQBRACKET
    '''

    print("-----VARIABLE------")
    print(*p)

def p_params(p):
    ''' params  :   type_simple ID
                |   type_simple ID COMMA params
    '''
    
def p_body(p):
    ''' body    :   LEFTBRACKET body1 RIGHTBRACKET
        body1   :   statute
                |   statute body1
                |   empty
    '''

def p_body_return(p):
    ''' body_return    :   LEFTBRACKET body_return1 RETURN factor RIGHTBRACKET
        body_return1   :   statute
                       |   statute body_return1
                       |   empty
    '''

def p_call(p):
    ''' call    :   ID LEFTPAREN call1 RIGHTPAREN
        call1   :   exp
                |   exp COMMA call1
    '''

def p_statute(p):
    '''statute  :   vars
                |   assignment
                |   write
                |   read
                |   if
                |   for
                |   while
                |   call
    '''
def p_assignment(p):
    '''assignment :     ID ASSIGNMENT expression SEMICOLON
    '''

########## review cte_string
def p_write(p):
    '''write  :   PRINT LEFTPAREN write1 RIGHTPAREN SEMICOLON
       write1 :   expression COMMA write1
              |   expression
    '''

def p_read(p):
    '''read  :   READ LEFTPAREN read1 RIGHTPAREN SEMICOLON
       read1 :   variable 
             |   variable read2
       read2 :   COMMA read1 
    '''

def p_if(p):
    '''if  :   IF LEFTPAREN expression RIGHTPAREN body if1
       if1 :   ELSE body
           |   empty
    '''

def p_for(p):
    '''for  :   FOR LEFTPAREN expression TO factor RIGHTPAREN body
    '''

def p_while(p):
    '''while  :   WHILE LEFTPAREN expression RIGHTPAREN body
    '''

def p_expression(p):
    ''' expression  :   exp
                    |   exp GREATER exp
                    |   exp LESS exp
                    |   exp NOTEQUAL exp
                    |   exp EQUAL exp
    '''
def p_exp(p):
    ''' exp :   term
            |   term PLUS exp
            |   term MINUS exp
    '''

def p_term(p):
    '''term  :   factor
             |   factor TIMES term
             |   factor DIVIDE term   
    '''
def p_factor(p):
    '''factor :   LEFTPAREN exp RIGHTPAREN
              |   CTE_I
              |   CTE_F
              |   CTE_CH
              |   variable
              |   CALL
    '''

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input! - {} ".format(p))


def p_empty(p):
    '''empty :'''
    pass


# Build the parser and lexer
parser = yacc.yacc()
lexer = MyLexer()
lexer.build()

if __name__ == '__main__':

    if len(sys.argv) > 1:
        file = sys.argv[1]
        try:
            f = open(file, 'r')
            data = f.read()
            f.close()
            result = parser.parse(data)
            if result == "COMPILED":
                lexer.test(data)
                print("Valid input")
                print(result)
        except EOFError:
            print(EOFError)
    else:
        print("No file to compile found")


#####DEBUGS:

# 1) Resolver lo de CTE_String y CTE_CH
# 2) Al haberlo resuelto, cambiar la gramática para que incluya comillas y se de a entender que eso es el string o char
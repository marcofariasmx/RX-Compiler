import ply.yacc as yacc
import sys
from lexer import MyLexer
from FuncsDir_Vars_Table import FuncsDir_Vars_Table
from collections import defaultdict
from quadruples import quadruples

class MyParser(object):

    tokens = MyLexer.tokens

    def __init__(self):
    
        #Create DirFunc
        self.dirTable = FuncsDir_Vars_Table()
        self.quads = quadruples()

        # Build the parser and lexer
        self.lexer = MyLexer()
        self.lexer.build()
        self.parser = yacc.yacc(module=self)

        #Create some helpers to store data
        self.varType = ''
        self.varNames = []
        self.varIsArray = []
        #self.declaredVars = {'name': [], 'type': []}
        self.declaredVars = defaultdict(list)
        self.currScope = ''
        self.ownerFunc = ''

        #Quadruples
        self.operand1 = defaultdict(list)
        self.operand2 = defaultdict(list)
        self.operator = ''
        self.result = []

        #Temp factors list.
        self.factors = defaultdict(list)

        self.functionsInitDir = []


    #Helper functions
    def storeDeclaredVars(self):
        #print(self.varNames)
        #print(self.declaredVars)
        for var in self.varNames:
            self.declaredVars['name'].append(var)
            self.declaredVars['type'].append(self.varType)
            self.declaredVars['isArray'].append(self.varIsArray.pop(0))
        self.varNames.clear()
        self.varType = ''

    def insertVars(self):
        for idx, varName in enumerate(self.declaredVars['name']):

            #Before insert earch for var id-name in current VarTable if found throw Error “multiple declaration”
            #if not, add var id-name and current-type to current VarTable
            for idx2, varInDir in enumerate(self.dirTable.VarsDirectory['name']):
                if varInDir == varName and self.dirTable.VarsDirectory['ownerFunc'][idx2] == self.ownerFunc:
                    exitErrorText = " Error: multiple declaration of variable: “" + varName + '” ' 'in scope of “' + self.ownerFunc + '”'
                    sys.exit(exitErrorText)

            self.dirTable.insertVariable(varName, self.declaredVars['type'][idx], self.ownerFunc, self.currScope, self.declaredVars['isArray'][idx])
        self.declaredVars.clear()

    # Grammar declaration

    def p_program(self, p):
        '''program      :  PROGRAM program_id SEMICOLON globalVars globalFuncs main_keyword LEFTPAREN RIGHTPAREN main_body
        '''

        print("-----p_program------")
        print(*p)

        p[0] = "COMPILED"

        self.ownerFunc = 'main'
        self.insertVars()


        #print()
        print("AQUI VARNAMES!")
        print(self.varNames)
        print(self.varType)
        print('factors: ', self.factors)

        print("FuncsDirectory:")
        print(self.dirTable.FuncsDirectory)
        print("VarsDirectory:")
        print(self.dirTable.VarsDirectory)

        print("QUADRUPLES: ")
        for idx, operator in enumerate(self.quads.quadruples['operator']):
            print(idx+1, ', ', operator, ', ', self.quads.quadruples['operand1'][idx], ', ', self.quads.quadruples['operand2'][idx], ', ', self.quads.quadruples['result'][idx])

    def p_main_keyword(self, p):
        '''
            main_keyword    : MAIN
        '''
        #print("COUNTEEEEEEEEEEEEEEEEERRRRRRRR")
        #print(self.quads.counter)
        #print(self.dirTable.FuncsDirectory)
        self.functionsInitDir.append(self.quads.counter)
    
    def p_main_body(self, p):
        '''
            main_body   :   body
        '''
        mainInitDir = self.functionsInitDir.pop()
        self.dirTable.insertFunction('main', 'void', mainInitDir, None, None)
        self.quads.quadruples['result'][0] = str(mainInitDir) + ' (main)'

    def p_expression_program_id(self, p):
        '''
        program_id : ID
        '''

        print("-----p_expression_program_id------")
        print(*p)
        self.ownerFunc = p[1]

        #Add id-name and type program a DirFunc
        self.dirTable.insertFunction(p[1], 'program', 1, None, None)

    def p_globalVars(self, p):
        '''
            globalVars  :  vars
                        |  empty 
        '''
        print("-----p_globalVars------")
        print(*p)
        self.currScope = 'global'
        #*#*#*#*#
        self.insertVars()

    def p_globaFuncs(self, p):
        '''
            globalFuncs :  functions
                        |  empty
        '''
        print("-----p_globaFuncs------")
        print(*p)
        self.currScope = 'local'
        self.insertVars()

    def p_vars(self, p):
        ''' 
            vars    :   VARS vars_body
        '''
        print("----VARS-----")
        print(*p)


    def p_vars_body(self, p):
        ''' 
            vars_body   :   type_simple multiVar SEMICOLON vars_body
                        |   empty
        '''
        print("----p_vars_body-----")
        print(*p)

    def p_multiVar(self, p):
        ''' 
            multiVar    :   singleVar COMMA multiVar
                        |   singleVar 
        '''
        print("----p_multiVar-----")
        print(*p)

        self.storeDeclaredVars()

    def p_singleVar(self, p):
        ''' 
            singleVar  :  variable
        '''
        print("----p_singleVar-----")
        print(*p)

    def p_functions(self, p):
        ''' functions    :   FUNC type_simple function_id LEFTPAREN params RIGHTPAREN body_return
                         |   FUNC VOID function_id LEFTPAREN RIGHTPAREN body
        '''
        print("-----FUNCTIONS------")
        print(*p)

        #Add id-name and type program a DirFunc
        self.dirTable.insertFunction(p[2], p[1], self.functionsInitDir.pop(), None, None)
        self.ownerFunc = p[2]
    
    def p_function_id(self, p):
        '''
            function_id :   ID
        '''
        self.functionsInitDir.append(self.quads.counter)


    def p_type_simple(self, p):
        ''' type_simple :   INT
                        |   FLOAT
                        |   CHAR
                        |   BOOL
        '''
        print("-----TYPE SIMPLE------")
        print(*p)
        self.varType = p[1]
        
    def p_variable(self, p):
        ''' variable    :   var_matrix
                        |   var_array
                        |   var_id
        '''
        print("-----VARIABLE------")
        print(*p)
        ####Esto puede tronar cuando sea una nano exp al depender de p[1], OJO AQUI!!!!!!!!

    def p_var_id(self, p):
        '''
            var_id  : ID
        '''
        self.varNames.append(p[1])
        self.varIsArray.append(False)

    def p_var_matrix(self, p):
        '''
            var_matrix  :   var_id LEFTSQBRACKET nano_exp RIGHTSQBRACKET LEFTSQBRACKET nano_exp RIGHTSQBRACKET
        '''
        self.varIsArray[-1] = True

    def p_var_array(self, p):
        '''
            var_array  :   var_id LEFTSQBRACKET nano_exp RIGHTSQBRACKET 
        '''
        self.varIsArray[-1] = True
    

    def p_params(self, p):
        ''' params  :   type_simple ID COMMA params
                    |   type_simple ID 
        '''
        
    def p_body(self, p):
        ''' 
            body    :   LEFTBRACKET bodyContent RIGHTBRACKET
        '''
        print("-----p_body------")
        print(*p)

    def p_bodyContent(self, p):
        ''' bodyContent :   statute bodyContent
                        |   empty
        '''
        print("-----p_bodyContent------")
        print(*p)

    def p_body_return(self, p):
        ''' 
            body_return :   LEFTBRACKET bodyContent_return RETURN factor RIGHTBRACKET
        '''
        print("-----p_body_return------")
        print(*p)

    def p_bodyContent_return(self, p):
        ''' bodyContent_return  :   statute bodyContent_return
                                |   empty
        '''
        print("-----p_bodyContent_return------")
        print(*p)

    def p_call(self, p):
        ''' call    :   ID LEFTPAREN call1 RIGHTPAREN
            call1   :   expression
                    |   expression COMMA call1
        '''
        print("-----p_call------")
        print(*p)

    def p_statute(self, p):
        '''statute  :   vars
                    |   assignment
                    |   write
                    |   read
                    |   if
                    |   for
                    |   while
                    |   call
        '''
        print("-----p_statute------")
        print(*p)


    def p_assignment(self, p):
        '''
            assignment  :   factor_variable ASSIGNMENT expression SEMICOLON
        '''
        #Consulting ID type and pushing the operand is done through "factor_variable"

        #Push the operator assignment
        if p[2]:
            self.quads.operator_push(p[2])
        print("-----p_assignment------")
        print(*p)


    def p_write(self, p):
        '''
            write   :   PRINT LEFTPAREN write1 RIGHTPAREN SEMICOLON
            write1  :   expression COMMA write1
                    |   expression
        '''

        print("-----p_write------")
        print(*p)

    def p_read(self, p):
        ''' read    :   READ LEFTPAREN read1 RIGHTPAREN SEMICOLON
            read1   :   variable 
                    |   variable read2
            read2   :   COMMA read1 
        '''

        print("-----p_read------")
        print(*p)

    def p_if(self, p):
        ''' if          :   IF LEFTPAREN expression_if RIGHTPAREN body_if else_case body_else
        '''
        
        print("-----p_if------")
        print(*p)

        if p[1]:
            self.quads.endQuad()

    def p_else_case(self, p):
        '''
            else_case   :   ELSE
                        |   empty
        '''

        if p[1]:
            self.quads.generateQuad_else()
            self.quads.endQuad()

        print("-----p_else_case------####")
        print(*p)

    def p_expression_if(self, p):
        '''
            expression_if   :   expression
        '''

        self.quads.generateQuad_if()

        print("-----p_expression_if------")
        print(*p)

    def p_body_if(self, p):
        '''
            body_if : body
        '''

        print("-----p_body_if------")
        print(*p)

    def p_body_else(self, p):
        '''
            body_else   :   body
                        |   empty
                        
        '''

        print("-----p_body_else------")
        print(*p)

    def p_for(self, p):
        '''for  :   FOR for_id_exists ASSIGNMENT for_expression1 TO for_expression2 by_optional DO body
        '''

        print("-----p_for------")
        print(*p)
        #Check first if ID already exists in local vars, if exists then assign new value, if not, create a new variable
        self.quads.forLoop_end()

    def p_by_optional(self, p):
        '''
            by_optional :   BY expression
                        |   empty
        '''

        if p[1]:
            self.quads.forLoop_BySteps()

    def p_for_expression1(self, p):
        '''
            for_expression1 :   expression
        '''

        #Push the operator assignment to assign the val of exp1 to the declared variable
        self.quads.operator_push('=')
        #GENERATE VC
        self.quads.forLoop_VC()

    def p_for_expression2(self, p):
        '''
            for_expression2 :   expression
        '''
        #GENERATE VF
        self.quads.forLoop_VF()
    
    def p_for_id_exists(self, p):
        '''
            for_id_exists   :   variable
        '''

        #Check if variable to store exists locally in not yet saved function
        localVarFound = False
        for idx, varName in enumerate(self.declaredVars['name']):
            if varName == self.varNames[0]:
                #Before pushing to operands stack, validate type is numeric
                if self.declaredVars['type'][idx] == 'int' or self.declaredVars['type'][idx] == 'float':
                    self.quads.operand_push(self.declaredVars['name'][idx], self.declaredVars['type'][idx])
                    self.varNames.clear()
                    localVarFound = True
                else:
                    exitErrorText = 'Non valid type for for loop first expression: ' + self.declaredVars['type'][idx]
                    sys.exit(exitErrorText)
                break

        
        #If variable was not found locally, check if variable to store exists in VarsDirectory that belongs to a global var
        varType = None
        if not localVarFound:
            varType = self.dirTable.getVarType_Global(self.varNames[0])
        if not localVarFound and varType:
            #Before pushing to operands stack, validate type is numeric
            if varType == 'int' or varType == 'float':
                self.quads.operand_push(self.varNames[0], varType)
                self.varNames.clear()
            else:
                exitErrorText = 'Non valid type for for loop first expression: ' + varType
                sys.exit(exitErrorText)
        
        #If variable was not found anywhere, store it
        elif not localVarFound and not varType:
            self.varType = 'float'
            # self.varNames.append() done automatically on "variable"
            self.quads.operand_push(self.varNames[0], self.varType)
            self.storeDeclaredVars()


    def p_while(self, p):
        '''while  :   whileKeyword LEFTPAREN expression endWhileExp body
        '''

        print("-----p_while------")
        print(*p)

        self.quads.endQuad_while()

    def p_whileKeyword(self, p):
        '''
            whileKeyword    :   WHILE
        '''
        print("-----p_whileKeyword------")
        print(*p)

        self.quads.startQuad_while()

    def p_endWhileExp(self, p):
        '''
            endWhileExp : RIGHTPAREN
        '''

        print("-----p_endWhileExp------")
        print(*p)

        self.quads.generateQuad_while()

    def p_expression(self, p):
        ''' expression  :   mili_exp expression2
            expression2 :   OR expression
                        |   empty
        '''
        print("-----p_expression------")
        print(*p)

    def p_mili_exp(self, p):
        ''' mili_exp    :   micro_exp mili_exp2
            mili_exp2   :   AND mili_exp
                        |   empty
        '''
        print("-----p_mili_exp------")
        print(*p)

    def p_micro_exp(self, p):
        ''' micro_exp   :   nano_exp
                        |   nano_exp GREATER nano_exp
                        |   nano_exp LESS nano_exp
                        |   nano_exp NOTEQUAL nano_exp
                        |   nano_exp EQUAL nano_exp 
        '''
        if len(p) >= 3:
            if p[2]:
                self.quads.operator_push(p[2])
        print("-----p_micro_exp------")
        print(*p)

    
    def p_nano_exp(self, p):
        ''' nano_exp    :   term
                        |   term PLUS term
                        |   term MINUS term
        '''
        if len(p) >= 3:
            if p[2]:
                self.quads.operator_push(p[2])
        print("-----p_nano_exp------")
        print(*p)
    
    def p_term(self,p):
        '''term :   factor
                |   factor TIMES factor
                |   factor DIVIDE factor   
        '''
        if len(p) >= 3:
            if p[2]:
                self.quads.operator_push(p[2])
        print("-----p_term------")
        print(*p)


    def p_factor(self,p):
        '''factor   :   LEFTPAREN expression RIGHTPAREN
                    |   factor_int
                    |   factor_float
                    |   factor_char
                    |   factor_bool
                    |   factor_variable
                    |   factor_call
        '''
        print("-----p_factor------")
        print(*p)

    def p_factor_int(self,p):
        '''
            factor_int   :   CTE_I
        '''

        self.quads.operand_push(p[1], 'int')
        print("-----p_factor_int------")
        print(*p)

    def p_factor_float(self,p):
        '''
            factor_float   :   CTE_F
        '''

        self.quads.operand_push(p[1], 'float')
        print("-----p_factor_float------")
        print(*p)

    def p_factor_char(self,p):
        '''
            factor_char   :   CTE_CH
        '''

        self.quads.operand_push(p[1], 'char')
        print("-----p_factor_char------")
        print(*p)

    def p_factor_bool(self,p):
        '''
            factor_bool     :   TRUE
                            |   FALSE
        '''

        self.quads.operand_push(p[1], 'bool')
        print("-----p_factor_bool------")
        print(*p)

    def p_factor_variable(self,p):
        '''
            factor_variable   :   variable
        '''
        
        #Check if variable to store exists locally in not yet saved function
        localVarFound = False
        for idx, varName in enumerate(self.declaredVars['name']):
            if varName == self.varNames[0]:
                self.quads.operand_push(self.declaredVars['name'][idx], self.declaredVars['type'][idx])
                self.varNames.clear()
                localVarFound = True
                break
        
        #If variable was not found locally, check if variable to store exists in VarsDirectory that belongs to a global var
        varType = None
        if not localVarFound:
            varType = self.dirTable.getVarType_Global(self.varNames[0])
        if not localVarFound and varType:
            self.quads.operand_push(self.varNames[0], varType)
            self.varNames.clear()
        
        #If variable was not found anywhere, throw an error and exit
        elif not localVarFound and not varType:
            noVarNameErrorText = " Error: variable “" + self.varNames[0] + '” does not exist in current scope or globally'
            sys.exit(noVarNameErrorText)

        print("-----p_factor_variable------")
        print(*p)

    def p_factor_call(self,p):
        '''
            factor_call   :   call
        '''
        print("-----p_factor_call------")
        print(*p)

    # Error rule for syntax errors
    def p_error(self,p):
        print("Syntax error in input! - {} ".format(p))


    def p_empty(self, p):
        '''empty :'''
        pass



#####DEBUGS:

# 1) Resolver lo de CTE_String y CTE_CH
# 2) Al haberlo resuelto, cambiar la gramática para que incluya comillas y se de a entender que eso es el string o char

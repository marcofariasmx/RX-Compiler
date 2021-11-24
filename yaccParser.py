from re import S
import ply.yacc as yacc
import sys
from lexer import MyLexer
#from FuncsDir_Vars_Table import FuncsDir_Vars_Table
from collections import defaultdict
from quadruples import quadruples
from copy import deepcopy

class MyParser(object):

    tokens = MyLexer.tokens

    def __init__(self):
    
        #Create quads object
        self.quads = quadruples()

        #Create DirFunc
        self.dirTable = self.quads.dirTable

        # Build the parser and lexer
        self.lexer = MyLexer()
        self.lexer.build()
        self.parser = yacc.yacc(module=self)

        #Create some helpers to store data
        self.varType = ''
        self.varNames = []
        self.varIsArray = []
        #self.declaredVars = {'name': [], 'type': [], 'isArray': [], 'memAddress': []}
        self.declaredVars = defaultdict(list)
        self.currScope = ''
        self.ownerFunc = ''
        self.varsSize = []
        self.varSizeNum = 0
        self.varDimensions = []
        self.varDimensionsHelper = []
        self.dimensionsSize = []
        self.dimensionSizeHelper = []

        #Quadruples
        self.operand1 = defaultdict(list)
        self.operand2 = defaultdict(list)
        self.operator = ''
        self.result = []

        #Temp factors list.
        self.factors = defaultdict(list)

        #Functions
        self.functionType = ''
        self.functionsInitDir = []
        self.functionName = ''
        self.paramType = []

        #Parameters
        #self.parameters = {'parameters' : {'paramType': [], 'paramIsArray':[], 'paramVarName': []}
        self.parameters = defaultdict(list)
        self.paramTypeList = []
        self.paramIsArrayList = []
        self.paramNameList = []
        self.paramNum = 0

        #Calls to functions
        self.callName = []
        self.callMemAddress = []
        #self.callType = []


    #Helper functions
    def storeDeclaredVars(self):
        
        for var in self.varNames:
            self.declaredVars['name'].append(var)
            self.declaredVars['type'].append(self.varType)
            self.declaredVars['isArray'].append(self.varIsArray.pop(0))

            if self.declaredVars['isArray'][-1]: #last appended item is array, then
                
                self.declaredVars['dimensions'].append(deepcopy(self.varDimensionsHelper))

                
                varsSize = 1


                for dim in self.varDimensionsHelper:

                    varsSize = varsSize * int(dim)
                
                self.declaredVars['size'].append(varsSize)
                
                self.declaredVars['dimensionsSize'].append(len(self.varDimensionsHelper))
            
                memBlocksSize = varsSize

                self.varDimensionsHelper.clear()
                self.varDimensions.clear()

            else:

                self.declaredVars['dimensions'].append(None)
                self.declaredVars['size'].append(1)
                self.declaredVars['dimensionsSize'].append(None)

                memBlocksSize = 1

            

            memAddress = self.quads.memory.allocateMem(self.currScope, self.varType, memBlocksSize)
            self.declaredVars['memAddress'].append(memAddress)

        self.varNames.clear()
        self.varType = ''

    def storeDeclaredParams(self):
        for idx, paramName in enumerate(self.paramNameList):
            self.declaredVars['name'].append(paramName)
            self.declaredVars['type'].append(self.paramTypeList[idx])
            self.declaredVars['isArray'].append(self.paramIsArrayList[idx])
            self.declaredVars['dimensions'].append(None)
            self.declaredVars['size'].append(1)
            self.declaredVars['dimensionsSize'].append(None)

            memAddress = self.quads.memory.allocateMem(self.currScope, self.paramTypeList[idx], 1)
            self.declaredVars['memAddress'].append(memAddress)

    def insertVars(self):
        for idx, varName in enumerate(self.declaredVars['name']):

            #Before insert earch for var id-name in current VarTable if found throw Error “multiple declaration”
            #if not, add var id-name and current-type to current VarTable
            for idx2, varInDir in enumerate(self.dirTable.VarsDirectory['name']):
                if varInDir == varName and self.dirTable.VarsDirectory['ownerFunc'][idx2] == self.ownerFunc:
                    exitErrorText = " Error: multiple declaration of variable: “" + varName + '” ' 'in scope of “' + self.ownerFunc + '”'
                    sys.exit(exitErrorText)

            self.dirTable.insertVariable(varName, self.declaredVars['type'][idx], self.ownerFunc, self.currScope, self.declaredVars['isArray'][idx], self.declaredVars['memAddress'][idx], self.declaredVars['size'][idx], self.declaredVars['dimensions'][idx], self.declaredVars['dimensionsSize'][idx])
        self.declaredVars.clear()
    
    def insert_FuncsAsGlobalVars(self, funcName, funcReturnType):
        #Before insert search for var id-name in current VarTable if found throw Error “Error: declaration of function: with the same name”
        #if not, add var id-name and current-type to current VarTable
        for idx, varInDir in enumerate(self.dirTable.VarsDirectory['name']):
            if varInDir == funcName and self.dirTable.VarsDirectory['scope'][idx] == 'global':
                exitErrorText = " Error: declaration of function: “" + funcName + '” ' 'with the same name as another global variable “' + varInDir + '”'
                sys.exit(exitErrorText)

        memAddress = self.quads.memory.allocateMem('global', funcReturnType, 1)
        
        self.dirTable.insertVariable(funcName, funcReturnType, None, 'global', False, memAddress, 1, None, None) #If ownerFunc is None it means that it is a function type in the variables

    # Grammar declaration

    def p_program(self, p):
        '''program      :  PROGRAM program_id SEMICOLON globalVars globalFuncs main_keyword LEFTPAREN RIGHTPAREN main_body
        '''


        p[0] = "COMPILED"

        self.ownerFunc = 'main'
        self.insertVars()


        # #prints for testing purposes
        # print("VARNAMES")
        # print(self.varNames)
        # print(self.varType)
        # print('factors: ', self.factors)

        # print("FuncsDirectory:")
        # print(self.dirTable.FuncsDirectory)
        # print("VarsDirectory:")
        # print(self.dirTable.VarsDirectory)

        # print("MEMORY: ")
        # print("Global: ")
        # print(self.quads.memory.globalMem)
        # print("Local: ")
        # print(self.quads.memory.localMem)
        # print("Temporal: ")
        # print(self.quads.memory.tempMem)
        # print("Constant: ")
        # print(self.quads.memory.constMem)

        # print("QUADRUPLES: ")
        # for idx, operator in enumerate(self.quads.quadruples['operator']):
        #     print(idx+1, ', ', operator, ', ', self.quads.quadruples['operand1'][idx], ', ', self.quads.quadruples['operand2'][idx], ', ', self.quads.quadruples['result'][idx])

        # After compilation is done, export obj containing the directory of functions & variables, quadruples and constants
        self.quads.exportOBJ()
        #self.quads.exportOBJ_HumanReadable()

    def p_main_keyword(self, p):
        '''
            main_keyword    : MAIN
        '''

        #Clear local and temp memory so that it starts fresh
        self.quads.memory.emptyMem()

        self.functionsInitDir.append(self.quads.counter)
        self.currScope = 'local'
    

    def p_main_body(self, p):
        '''
            main_body   :   body
        '''
        mainInitDir = self.functionsInitDir.pop()
        self.dirTable.insertFunction('main', 'void', mainInitDir, None, None)
        self.quads.quadruples['result'][0] = mainInitDir #Redirect for main quadruple


    def p_expression_program_id(self, p):
        '''
        program_id : ID
        '''

        self.ownerFunc = p[1]
        self.currScope = 'global'

        #Add id-name and type program a DirFunc
        self.dirTable.insertFunction(p[1], 'program', 1, None, None)


    def p_globalVars(self, p):
        '''
            globalVars  :  vars
                        |  empty 
        '''
        self.insertVars()


    def p_globaFuncs(self, p):
        '''
            globalFuncs :  functions
                        |  empty
        '''

        self.insertVars()

    def p_vars(self, p):
        ''' 
            vars    :   VARS vars_body
        '''


    def p_vars_body(self, p):
        ''' 
            vars_body   :   type_simple multiVar SEMICOLON vars_body
                        |   empty
        '''


    def p_multiVar(self, p):
        ''' 
            multiVar    :   singleVar COMMA multiVar
                        |   singleVar 
        '''


        self.storeDeclaredVars()

    def p_singleVar(self, p):
        ''' 
            singleVar  :  variable
        '''


    def p_functions(self, p):
        ''' functions    :   FUNC type_simple function_id LEFTPAREN params RIGHTPAREN body_return
                         |   FUNC VOID function_id LEFTPAREN RIGHTPAREN body
        '''

        self.quads.generate_endfunc_quad()

        #Add id-name and type program a DirFunc
        if p[2] and p[1]:
            self.dirTable.insertFunction(p[2], p[1], self.functionsInitDir.pop(), None, None)
            self.ownerFunc = p[2]
        elif p[1]:
            self.dirTable.insertFunction(self.functionName, self.functionType, self.functionsInitDir.pop(), None, deepcopy(self.parameters))
            self.ownerFunc = self.functionName
            self.insert_FuncsAsGlobalVars(self.functionName, self.functionType)

            self.paramNameList.clear()
            self.paramTypeList.clear()
            self.paramIsArrayList.clear()
        
        
    def p_function_id(self, p):
        '''
            function_id :   ID
        '''
        #Clear local and temp memory so that it starts fresh
        self.quads.memory.emptyMem()

        #Clear params in params list to store the correct ones
        self.paramType.clear()

        self.functionsInitDir.append(self.quads.counter)
        self.functionName = p[1]
        self.currScope = 'local'


    def p_type_simple(self, p):
        ''' type_simple :   INT
                        |   FLOAT
                        |   CHAR
                        |   BOOL
        '''

        self.varType = p[1]
        self.functionType = p[1]
        self.paramType.append(p[1])
        

    def p_variable(self, p):
        ''' variable    :   var_matrix
                        |   var_array
                        |   var_id
        '''
        
        #Append the variable dimensions
        self.varDimensions.append(self.varDimensionsHelper)
        

    def p_var_id(self, p):
        '''
            var_id  : ID
        '''

        self.varNames.append(p[1])
        self.varIsArray.append(False)


    def p_var_matrix(self, p):
        '''
            var_matrix  :   var_id var_dimension var_dimension
        '''
        self.varIsArray[-1] = True


    def p_var_array(self, p):
        '''
            var_array  :   var_id var_dimension
        '''
        self.varIsArray[-1] = True


    def p_var_dimension(self, p):
        '''
            var_dimension   :   LEFTSQBRACKET nano_exp RIGHTSQBRACKET
        '''

        #get the addrs dimension from operands
        operand, type = self.quads.operand_pop()
        #convert that addrs to a dim number
        if str(operand)[0] != '+': #if it is not pointer type, then append, otherwise append None, unkwown
            dimNumber = self.quads.memory.getValFromMemory(operand)
        else: # it is pointer, append back to operands to use it
            self.quads.operand_push(operand, type)
            dimNumber = None

        self.varDimensionsHelper.append(dimNumber)
    
    def p_params(self, p):
        '''
            params  :   params_body
        '''
        self.parameters['paramType'].append(self.paramTypeList)
        self.parameters['paramIsArray'].append(self.paramIsArrayList)
        self.parameters['paramVarName'].append(self.paramNameList)

        self.storeDeclaredParams()

    def p_params_body(self, p):
        ''' params_body :   type_simple variable COMMA params_body
                        |   type_simple variable
        '''
        #self.paramType is pushed in type_simple

        self.paramTypeList.append(self.paramType.pop(0))
        self.paramIsArrayList.append(self.varIsArray.pop(0))
        self.paramNameList.append(self.varNames.pop(0))
        

    def p_body(self, p):
        ''' 
            body    :   LEFTBRACKET bodyContent RIGHTBRACKET
        '''


    def p_bodyContent(self, p):
        ''' bodyContent :   statute bodyContent
                        |   empty
        '''


    def p_body_return(self, p):
        ''' 
            body_return :   LEFTBRACKET bodyContent_return RIGHTBRACKET
        '''


    def p_bodyContent_return(self, p):
        ''' 
            bodyContent_return  :   statute bodyContent_return
                                |   empty
        '''


    def p_call(self, p):
        ''' 
            call    :   call_id LEFTPAREN call_params RIGHTPAREN
        '''

        self.paramNum = 0
        callName = self.callName.pop()
        callMemAddress = self.callMemAddress.pop()
        #Get call type
        callFound = False
        for idx, varName in enumerate(self.dirTable.VarsDirectory['name']):
            if varName == callName and self.dirTable.VarsDirectory['ownerFunc'][idx] == None:
                callType = self.dirTable.VarsDirectory['type'][idx]
                callFound = True
                break

        #For recursivity cases
        if self.functionName == callName:
            callFound = True
            callType = self.functionType
        
        if not callFound:
            exitErrorText = 'No function with the name: ' + callName + ' found.'
            sys.exit(exitErrorText)
        if callFound:
            self.quads.operand_push(callMemAddress, callType)
        

    def p_call_id(self, p):
        '''
            call_id : ID
        '''
        #Generate ERA in quads for call

        for idx, varName in enumerate(self.dirTable.VarsDirectory['name']):
            if varName == p[1] and self.dirTable.VarsDirectory['ownerFunc'][idx] == None:
                callType = self.dirTable.VarsDirectory['type'][idx]
                callFound = True
                break

        if self.functionName == p[1]:
            callFound = True
            callType = self.functionType

        memAddress = self.quads.memory.allocateMem('global', callType, 1)

        self.quads.generate_era_quad(p[1])
        self.callName.append(p[1])
        self.callMemAddress.append(memAddress)


    def p_call_params(self, p):
        '''
            call_params :   multi_param
                        |   empty
        '''

        self.quads.generate_GOSUB_quad(self.callMemAddress[-1])

    def p_multi_param(self, p):
        '''
            multi_param :   single_param COMMA multi_param
                        |   single_param   
        '''

    def p_single_param(self, p):
        '''
            single_param    :   expression
        '''

        self.paramNum += 1
        self.quads.generate_params_quads(self.paramNum)

    def p_statute(self, p):
        '''statute  :   vars
                    |   assignment
                    |   write
                    |   read
                    |   if
                    |   for
                    |   while
                    |   call SEMICOLON
                    |   returnTrigger
        '''


    def p_returnTrigger(self, p):
        '''
            returnTrigger   :   RETURN factor SEMICOLON
        '''
        self.quads.generate_return_quad()


    def p_assignment(self, p):
        '''
            assignment  :   factor_variable ASSIGNMENT expression SEMICOLON
        '''
        #Consulting ID type and pushing the operand is done through "factor_variable"

        #Push the operator assignment
        if p[2]:
            self.quads.operator_push(p[2])


    def p_write(self, p):
        '''
            write   :   PRINT LEFTPAREN write_body RIGHTPAREN SEMICOLON
        '''


    def p_write_body(self, p):
        '''
            write_body  :   write_single COMMA write_body
                        |   write_single
        '''

    def p_write_single(self, p):
        '''
            write_single    :   expression
        '''
        varAddress, type = self.quads.operand_pop()
        try: #means it is a composite type pointer, try to pop again
            varAddress, type = self.quads.operand_pop()
        except:
            pass

        self.quads.generate_print_quad(varAddress)

    def p_read(self, p):
        ''' read    :   READ LEFTPAREN read1 RIGHTPAREN SEMICOLON
            read1   :   variable 
                    |   variable read2
            read2   :   COMMA read1 
        '''


    def p_if(self, p):
        ''' if          :   IF LEFTPAREN expression_if RIGHTPAREN body_if else_case body_else
        '''

        if p[1]:
            self.quads.endQuad()

    def p_else_case(self, p):
        '''
            else_case   :   ELSE
                        |   empty
        '''

        if p[1]:
            self.quads.generateQuad_else()
            self.quads.endQuadElse()


    def p_expression_if(self, p):
        '''
            expression_if   :   expression
        '''

        self.quads.generateQuad_if()


    def p_body_if(self, p):
        '''
            body_if : body
        '''


    def p_body_else(self, p):
        '''
            body_else   :   body
                        |   empty
                        
        '''


    def p_for(self, p):
        '''for  :   FOR for_id_exists ASSIGNMENT for_expression1 TO for_expression2 by_optional DO body
        '''

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
                    self.quads.operand_push(self.declaredVars['memAddress'][idx], self.declaredVars['type'][idx])
                    self.varNames.clear()
                    localVarFound = True
                else:
                    exitErrorText = 'Non valid type for for loop first expression: ' + self.declaredVars['type'][idx]
                    sys.exit(exitErrorText)
                break
        
        #If variable was not found locally, check if variable to store exists in VarsDirectory that belongs to a global var
        varType = None
        if not localVarFound:
            varType, memAddress, isArray, dimensions = self.dirTable.getVarTypeAndAddress_Global(self.varNames[0])
        if not localVarFound and varType:
            #Before pushing to operands stack, validate type is numeric
            if varType == 'int' or varType == 'float':
                self.quads.operand_push(memAddress, varType) #POTENTIAL ERROR HERE SINCE IT IS PUSHING the name varType[1], analize, also for if
                self.varNames.clear()
            else:
                exitErrorText = 'Non valid type for for loop first expression: ' + self.varNames[0] + ' of type ' + varType
                sys.exit(exitErrorText)
        
        #If variable was not found anywhere, store it
        elif not localVarFound and not varType:
            self.varType = 'float'
            # self.varNames.append() done automatically on "variable"

            memAddress = self.quads.memory.allocateMem('local', self.varType, 1)
            self.quads.operand_push(memAddress, self.varType)
            
            self.declaredVars['name'].append(self.varNames.pop())
            self.declaredVars['type'].append(self.varType)
            self.declaredVars['isArray'].append(self.varIsArray.pop())
            self.declaredVars['memAddress'].append(memAddress)
            self.declaredVars['dimensions'].append(None)
            self.declaredVars['size'].append(1)
            self.declaredVars['dimensionsSize'].append(None)

            #self.varNames.clear()
            self.varType = ''


    def p_while(self, p):
        '''while  :   whileKeyword LEFTPAREN expression endWhileExp body
        '''

        self.quads.endQuad_while()

    def p_whileKeyword(self, p):
        '''
            whileKeyword    :   WHILE
        '''

        self.quads.startQuad_while()


    def p_endWhileExp(self, p):
        '''
            endWhileExp : RIGHTPAREN
        '''

        self.quads.generateQuad_while()

    def p_expression(self, p):
        ''' expression  :   mili_exp expression2
            expression2 :   OR expression
                        |   empty
        '''

    def p_mili_exp(self, p):
        ''' mili_exp    :   micro_exp mili_exp2
            mili_exp2   :   AND mili_exp
                        |   empty
        '''

    def p_micro_exp(self, p):
        ''' micro_exp   :   nano_exp
                        |   nano_exp GREATER nano_exp
                        |   nano_exp LESS nano_exp
                        |   nano_exp NOTEQUAL nano_exp
                        |   nano_exp EQUAL nano_exp
                        |   nano_exp GREATEROREQUAL nano_exp
                        |   nano_exp LESSOREQUAL nano_exp
        '''
        if len(p) >= 3:
            if p[2]:
                self.quads.operator_push(p[2])

    
    def p_nano_exp(self, p):
        ''' nano_exp    :   term
                        |   term PLUS term
                        |   term MINUS term
        '''
        if len(p) >= 3:
            if p[2]:
                self.quads.operator_push(p[2])

    
    def p_term(self,p):
        '''term :   factor
                |   factor TIMES factor
                |   factor DIVIDE factor   
        '''
        if len(p) >= 3:
            if p[2]:
                self.quads.operator_push(p[2])


    def p_factor(self,p):
        '''factor   :   LEFTPAREN expression RIGHTPAREN
                    |   factor_int
                    |   factor_float
                    |   factor_char
                    |   factor_bool
                    |   factor_variable
                    |   factor_call
        '''


    def p_factor_int(self,p):
        '''
            factor_int   :   CTE_I
        '''
        
        #Check first if constant already exists in constants table
        memAddress = self.quads.memory.searchConstant('int', p[1])
        #If it doesnt exists, create it and insert into it
        if not memAddress:
            memAddress = self.quads.memory.allocateMem('constant', 'int', 1)
            self.quads.memory.insertIntoMem(memAddress, p[1])
        
        self.quads.operand_push(memAddress, 'int')


    def p_factor_float(self,p):
        '''
            factor_float   :   CTE_F
        '''

        #Check first if constant already exists in constants table
        memAddress = self.quads.memory.searchConstant('float', p[1])
        #If it doesnt exists, create it and insert into it
        if not memAddress:
            memAddress = self.quads.memory.allocateMem('constant', 'float', 1)
            self.quads.memory.insertIntoMem(memAddress, p[1])

        self.quads.operand_push(memAddress, 'float')


    def p_factor_char(self,p):
        '''
            factor_char   :   CTE_CH
        '''

        #Check first if constant already exists in constants table
        memAddress = self.quads.memory.searchConstant('char', p[1])
        #If it doesnt exists, create it and insert into it
        if not memAddress:
            memAddress = self.quads.memory.allocateMem('constant', 'char', 1)
            self.quads.memory.insertIntoMem(memAddress, p[1])

        self.quads.operand_push(memAddress, 'char')


    def p_factor_bool(self,p):
        '''
            factor_bool     :   TRUE
                            |   FALSE
        '''

        self.quads.operand_push(p[1], 'bool')


    def p_factor_variable(self,p):
        '''
            factor_variable   :   variable
        '''
        
        #Check if variable to store exists locally in not yet saved function
        localVarFound = False
        for idx, varName in enumerate(self.declaredVars['name']):
            if varName == self.varNames[0]:

                #varType, memAddress, isArray, dimensions
                dimensions = self.declaredVars['dimensions'][idx]
                varType = self.declaredVars['type'][idx]
                memAddress = self.declaredVars['memAddress'][idx]
                
                normalPushType = True
                if self.declaredVars['isArray'][idx]:
                    #Calculate offset
                    
                    #if is matrix 
                    if len(dimensions) > 1:
                        #First Ensure it is within limits
                        if self.varDimensionsHelper[0] > dimensions[0] or self.varDimensionsHelper[0] > dimensions[0]:
                            exitErrorText = " Error: out of bounds access for: “" + self.varNames[0] + '”'
                            sys.exit(exitErrorText)

                        # M[s1][s2] = DirBase(M) + (s1 * d2) + s2 - d2 - 1
                        offset = (self.varDimensionsHelper[0] * dimensions[1]) + self.varDimensionsHelper[1] - dimensions[1] - 1
                    
                    #it is array
                    else:
                        #First Ensure it is within limits (Comprobar las dimensiones que se están pasando)
                        if len(self.varDimensionsHelper) > 0:
                            if self.varDimensionsHelper[0] > dimensions[0]:
                                exitErrorText = " Error: out of bounds access for: “" + self.varNames[0] + '”'
                                sys.exit(exitErrorText)
                            
                            # A[s1] = DirBase(A) + s1 - 1
                            offset = self.varDimensionsHelper[0] - 1
                        else: #Si no tiene dimensiones ints, entonces se está pasando la direción de una variable, recalcularla como un int
                            varType, varMemAddress, isArray, dimensions = self.dirTable.getVarTypeAndAddress_Global(self.varNames[-1])
                            pointerAddress = '+' + str(memAddress) + str(varMemAddress)
                            normalPushType = False
                            #value = self.quads.memory.getValFromMemory(varMemAddress)
                            offset = 0
                else:
                    #Default offset is always 1
                    offset = 0
                
                if normalPushType:
                    self.quads.operand_push(int(memAddress) + offset , varType)
                else:
                    self.quads.operand_push(pointerAddress, varType) 
        
                self.varNames.pop(0)
                self.varDimensionsHelper.clear()
                localVarFound = True
                break
        
        #If variable was not found locally, check if variable to store exists in VarsDirectory that belongs to a global var
        varType = None
        if not localVarFound:
            varType, memAddress, isArray, dimensions = self.dirTable.getVarTypeAndAddress_Global(self.varNames[0])
        if not localVarFound and varType:
            normalPushType = True
            if isArray:
                #Calculate offset
                
                #if is matrix
                if len(dimensions) > 1:
                    #First Ensure it is within limits
                    if self.varDimensionsHelper[0] > dimensions[0] or self.varDimensionsHelper[0] > dimensions[0]:
                        exitErrorText = " Error: out of bounds access for: “" + self.varNames[0] + '”'
                        sys.exit(exitErrorText)

                    # M[s1][s2] = DirBase(M) + (s1 * d2) + s2 - d2 - 1
                    offset = (self.varDimensionsHelper[0] * dimensions[1]) + self.varDimensionsHelper[1] - dimensions[1] - 1
                
                #it is array
                else:
                    #First Ensure it is within limits (Comprobar las dimensiones que se están pasando)
                    if len(self.varDimensionsHelper) > 0:
                        if self.varDimensionsHelper[0] > dimensions[0]:
                            exitErrorText = " Error: out of bounds access for: “" + self.varNames[0] + '”'
                            sys.exit(exitErrorText)
                        
                        # A[s1] = DirBase(A) + s1 - 1
                        offset = self.varDimensionsHelper[0] - 1
                    else: #Si no tiene dimensiones ints, entonces se está pasando la direción de una variable, recalcularla como un int
                        varType, varMemAddress, isArray, dimensions = self.dirTable.getVarTypeAndAddress_Global(self.varNames[-1])
                        pointerAddress = '+' + str(memAddress) + str(varMemAddress)
                        normalPushType = False
                        #value = self.quads.memory.getValFromMemory(varMemAddress)
                        offset = 0
            else:
                #Default offset is always 1
                offset = 0
            
            if normalPushType:
                self.quads.operand_push(int(memAddress) + offset , varType)
            else:
                self.quads.operand_push(pointerAddress, varType)  
            #self.varNames.clear()
            self.varNames.pop(0)
            self.varDimensionsHelper.clear()
        
        #If variable was not found anywhere, throw an error and exit
        elif not localVarFound and not varType:
            noVarNameErrorText = " Error: variable “" + self.varNames[0] + '” does not exist in current scope or globally'
            sys.exit(noVarNameErrorText)


    def p_factor_call(self,p):
        '''
            factor_call   :   call
        '''


    # Error rule for syntax errors
    def p_error(self,p):
        print("Syntax error in input! - {} ".format(p))


    def p_empty(self, p):
        '''empty :'''
        pass


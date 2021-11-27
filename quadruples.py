from semantics import Semantic
from memory import memory
from FuncsDir_Vars_Table import FuncsDir_Vars_Table
import sys
import pickle as pickle


class quadruples():

    def __init__(self):

        #Create DirFunc
        self.dirTable = FuncsDir_Vars_Table()

        #Initialize memory
        self.memory = memory()

        self.semantic = Semantic()
        
        self.quadruples = {'operator': [], 'operand1': [], 'operand2': [], 'result': []}
        self.jumpStack = [] #to momentarily store jumps related to pending gotos

        self.counter = 1

        self.operatorsStack = [] # +, -, *, /, >, <, etc
        self.operandsStack = {'operand': [], 'type': []} #operands: a, b, c.. types: int, char, bool...

        self.forLoopControlVars = []
        self.forLoopBySteps = []

        self.pointerStack = []
        
        self.result = 0

        ###Insert a 1 as a global constant to use for default by steps in for loop and in offsets
        self.memAddres_const1 = self.memory.allocateMem('constant', 'int', 1)
        self.memory.insertIntoMem(self.memAddres_const1, 1)

        self.quadruples['operator'].append('GOTO')
        self.quadruples['operand1'].append(None)
        self.quadruples['operand2'].append(None)
        self.quadruples['result'].append('main')

        self.counter += 1

    def operand_push(self, operand, type):
        self.operandsStack['operand'].append(operand)
        self.operandsStack['type'].append(type)

        #print("Operands Stack: ")
        #print(self.operandsStack)

    def operand_pop(self):
        operand = self.operandsStack['operand'].pop()
        type = self.operandsStack['type'].pop()

        return operand, type

    #When an operator is pushed, it triggers an action to generate a quadruple based on the previously pushed operands.
    def operator_push(self, operator):
        self.operatorsStack.append(operator)
        self.generateQuad(operator)

        #print("Operators Stack: ")
        #print(self.operatorsStack)

    def generateQuad(self, operatorType):
        rightOperand = self.operandsStack['operand'].pop()
        rightType = self.operandsStack['type'].pop()
        leftOperand = self.operandsStack['operand'].pop()
        leftType = self.operandsStack['type'].pop()

        #If one more pop() is available AND it is pointer type, pop it and replace it
        try:
            if self.operandsStack['operand'][-1][0] == '+':
                leftOperand = self.operandsStack['operand'].pop()
                leftType = self.operandsStack['type'].pop()
        except:
            pass
        
        operator = self.operatorsStack.pop(0)

        try:
            result_Type = self.semantic.semantic_cube[leftType][operator][rightType]
        except:
            exitErrorText = " Error: Type mismatch in “" + leftOperand + ' ' + operator + ' ' + rightOperand  + '” -> “' + leftType + '” ' + operator + ' “' + rightType + '”'
            sys.exit(exitErrorText)

        if operatorType == '=':

            #memAddress = self.memory.allocateMem('scope', result_Type, 1)

            self.quadruples['operator'].append(operator)
            self.quadruples['operand1'].append(rightOperand)
            self.quadruples['operand2'].append(None)
            self.quadruples['result'].append(leftOperand)

        else: # + - * / > < >= <= == !=
            
            self.result += 1
            #maskedResult = 'T' + str(self.result)
            tempMemAddress = self.memory.allocateMem('temporal', result_Type, 1)

            self.quadruples['operator'].append(operator)
            self.quadruples['operand1'].append(leftOperand)
            self.quadruples['operand2'].append(rightOperand)
            self.quadruples['result'].append(tempMemAddress)

            self.operandsStack['operand'].append(tempMemAddress)
            self.operandsStack['type'].append(result_Type)

            #print("self.quadruples")
            #print(self.quadruples)
        
        self.counter += 1;

    def generateQuad_if(self):
        exp_type = self.operandsStack['type'].pop()
        result = self.operandsStack['operand'].pop()

        if exp_type != 'bool':

            exitErrorText = " Error: Type mismatch in " + exp_type + ' ' + result
            sys.exit(exitErrorText)
        
        else:
            
            
            self.quadruples['operator'].append('GotoF')
            self.quadruples['operand1'].append(result)
            self.quadruples['operand2'].append(None)
            self.quadruples['result'].append('__')

            self.jumpStack.append(self.counter)

        self.counter +=1;

    def fillQuad(self, quadNum, result):
        self.quadruples['result'][quadNum-1] = result

    def endQuad(self):
        end = self.jumpStack.pop()
        self.fillQuad(end, self.counter)

    def endQuadElse(self):
        end = self.jumpStack.pop(-2) #pops the penultimate element from jumpstack
        self.fillQuad(end, self.counter)


    def generateQuad_else(self):
        self.quadruples['operator'].append('GOTO')
        self.quadruples['operand1'].append(None)
        self.quadruples['operand2'].append(None)
        self.quadruples['result'].append('__')

        self.jumpStack.append(self.counter)
        self.counter +=1;
        
    def startQuad_while(self):
        self.jumpStack.append(self.counter)

    def generateQuad_while(self):
        exp_type = self.operandsStack['type'].pop()
        result = self.operandsStack['operand'].pop()

        if exp_type != 'bool':

            exitErrorText = " Error: Type mismatch in " + exp_type + ' ' + result
            sys.exit(exitErrorText)
        
        else:
            
            self.quadruples['operator'].append('GotoF')
            self.quadruples['operand1'].append(result)
            self.quadruples['operand2'].append(None)
            self.quadruples['result'].append('__')

            self.jumpStack.append(self.counter)

        self.counter +=1;

    def endQuad_while(self):
        end = self.jumpStack.pop()
        retrn = self.jumpStack.pop()

        self.quadruples['operator'].append('GOTO')
        self.quadruples['operand1'].append(None)
        self.quadruples['operand2'].append(None)
        self.quadruples['result'].append(retrn)

        self.counter +=1;

        self.fillQuad(end, self.counter)

    
    def forLoop_VC(self):

        self.forLoopControlVars.append(self.quadruples['result'][-1])

    def forLoop_BySteps(self):
        operand = self.operandsStack['operand'].pop()
        operandType = self.operandsStack['type'].pop()

        if operandType == 'float' or operandType == 'int':
            #valid
            pass
        else:
            exitErrorText = 'Non valid type for for loop third expression: ' + operandType
            sys.exit(exitErrorText)

        self.forLoopBySteps.append(operand)
        

    def forLoop_end(self):

        if not self.forLoopBySteps: #if custom steps not declared, add default 1
            
            ###Insert a 1 as a global constant to use for default by steps in for loop
            self.memory.insertIntoMem(self.memAddres_const1, 1)
            self.forLoopBySteps.append(self.memAddres_const1)

        controlVar = self.forLoopControlVars.pop()

        self.result += 1

        self.quadruples['operator'].append('+')
        self.quadruples['operand1'].append(controlVar)
        self.quadruples['operand2'].append(self.forLoopBySteps.pop())

        if str(self.quadruples['operand1'][-1])[1] == 2 or str(self.quadruples['operand2'][-1])[1] == 2:
            memType = 'float'
        else:
            memType = 'int'
        
        tempMemAddress = self.memory.allocateMem('temporal', memType, 1)

        self.quadruples['result'].append(tempMemAddress)

        self.counter +=1;

        self.quadruples['operator'].append('=')
        self.quadruples['operand1'].append(tempMemAddress)
        self.quadruples['operand2'].append(None)
        self.quadruples['result'].append(controlVar)

        self.counter +=1;

        retrn = self.jumpStack.pop()

        self.quadruples['operator'].append('GOTO')
        self.quadruples['operand1'].append(None)
        self.quadruples['operand2'].append(None)
        self.quadruples['result'].append(retrn-1)

        self.counter +=1;

        self.fillQuad(retrn, self.counter)


    def forLoop_VF(self):

        operand = self.operandsStack['operand'].pop()
        operandType = self.operandsStack['type'].pop()

        if operandType == 'float' or operandType == 'int':
            #valid
            pass
        else:
            exitErrorText = 'Non valid type for for loop second expression: ' + operandType
            sys.exit(exitErrorText)

        self.result += 1
        #maskedResult = 'T' + str(self.result)

        self.quadruples['operator'].append('<')
        self.quadruples['operand1'].append(self.forLoopControlVars[-1])
        self.quadruples['operand2'].append(operand)
        tempMemAddress = self.memory.allocateMem('temporal', 'bool', 1)

        self.quadruples['result'].append(tempMemAddress)

        self.counter +=1;

        #self.result += 1
        #maskedResult = 'T' + str(self.result)
        #tempMemAddress = self.memory.allocateMem('temporal', 'float', 1)

        self.quadruples['operator'].append('GotoF')
        self.quadruples['operand1'].append(tempMemAddress)
        self.quadruples['operand2'].append(None)
        self.quadruples['result'].append('__')

        self.jumpStack.append(self.counter)

        self.counter +=1;
    
    def generate_era_quad(self, id):
        self.quadruples['operator'].append('ERA')
        self.quadruples['operand1'].append(None)
        self.quadruples['operand2'].append(None)
        self.quadruples['result'].append(id)

        self.counter +=1;

    def generate_params_quads(self, paramNum):
            #if self.operandsStack['operand']:
            self.quadruples['operator'].append('param')
            self.quadruples['operand1'].append(self.operandsStack['operand'].pop())
            self.quadruples['operand2'].append(None)
            self.quadruples['result'].append('par'+str(paramNum))

            self.counter +=1;

            #self.operandsStack['operand'].pop(0)
            self.operandsStack['type'].pop(0)

    def generate_endfunc_quad(self):
        self.quadruples['operator'].append('ENDFUNC')
        self.quadruples['operand1'].append(None)
        self.quadruples['operand2'].append(None)
        self.quadruples['result'].append(None)

        self.counter +=1;

    def generate_GOSUB_quad(self, funcID):
        self.quadruples['operator'].append('GOSUB')
        self.quadruples['operand1'].append(None)
        self.quadruples['operand2'].append(None)
        self.quadruples['result'].append(funcID)

        self.counter +=1;

    def generate_print_quad(self, varAddress):
        self.quadruples['operator'].append('print')
        self.quadruples['operand1'].append(None)
        self.quadruples['operand2'].append(None)
        self.quadruples['result'].append(varAddress)

        self.counter +=1;

    def generate_return_quad(self):

        operand, type = self.operand_pop()

        self.quadruples['operator'].append('RETURN')
        self.quadruples['operand1'].append(None)
        self.quadruples['operand2'].append(None)
        self.quadruples['result'].append(operand)

        self.counter +=1;

    def verifyQuad_Arrays(self, upperLimit):

        print("SE VA A VERIFICAR-----------")

        #Generate verify quad
        print("BEFORE POP: ", self.operandsStack)
        #operand, type = self.operand_pop()
        operand = self.operandsStack['operand'].pop(-2)
        self.operandsStack['type'].pop(-2)

        self.quadruples['operator'].append('Verif')
        self.quadruples['operand1'].append(operand)
        self.quadruples['operand2'].append(1)
        self.quadruples['result'].append(upperLimit)

        self.counter +=1;

        #Generate offset quad

        self.quadruples['operator'].append('-')
        self.quadruples['operand1'].append(operand)
        self.quadruples['operand2'].append(self.memAddres_const1)

        tempMemAddress = self.memory.allocateMem('temporal', 'int', 1)
        self.quadruples['result'].append(tempMemAddress)

        self.counter +=1;

        #Generate pointer quad
        operand, type = self.operand_pop()

        self.quadruples['operator'].append('+')
        self.quadruples['operand1'].append(tempMemAddress)
        self.quadruples['operand2'].append('!' + str(operand))

        tempMemAddress = self.memory.allocateMem('temporal', 'pointer', 1)
        self.quadruples['result'].append(tempMemAddress)

        self.operandsStack['operand'].append(tempMemAddress)
        self.operandsStack['type'].append('int')

        self.counter +=1;

    def exportOBJ(self):

        #file = open("OBJ.pkl", "wb")

        #1 Global mem
        #2 Constant mem
        #3 Funcs Dir
        #4 Quads 
        Dictionaries = [self.memory.globalMem, self.memory.constMem, self.dirTable.FuncsDirectory, self.dirTable.VarsDirectory, self.quadruples]

        pickle.dump( Dictionaries, open( "OBJ.pkl", "wb" ) )

        

    def exportOBJ_HumanReadable(self):

        def converter(memAddress):
            newQuad = ''

            if memAddress == None:
                return 'None'
            elif memAddress < 1000:
                return str(memAddress)

            if int(str(memAddress)[1]) == 1: # int type
                type = 'int'
            elif int(str(memAddress)[1]) == 2: # float type
                type = 'float'
            elif int(str(memAddress)[1]) == 3: # char type
                type = 'char'
            elif int(str(memAddress)[1]) == 4: # bool type
                type = 'bool'
            elif int(str(memAddress)[1]) == 5: # pointer type
                type = 'pointer'

            if int(str(memAddress)[0]) == 1: #global type
                newQuad = 'G-' + type + '-' + str(int(str(memAddress)[2:]))
                return newQuad
            elif int(str(memAddress)[0]) == 2: #local type
                newQuad = 'L-' + type + '-' + str(int(str(memAddress)[2:]))
                return newQuad
            elif int(str(memAddress)[0]) == 3: #temp type
                newQuad = 'T-' + type + '-' + str(int(str(memAddress)[2:]))
                return newQuad
            elif int(str(memAddress)[0]) == 4: #Constant type
                newQuad = 'C-' + type + '-' + str(int(str(memAddress)[2:]))
                return newQuad


        file = open("OBJ-HumanReadable.txt", "w")

        #Export memory
        file.write('MEMORY-DUMP:\n')
        for type in self.memory.constMem:
            for idx, value in enumerate(self.memory.constMem[type]['value']):
                line = converter(self.memory.constMem[type]['memIndex'][idx]) + ' ' + str(value) + '\n'
                file.write(line)

        #Export quads
        file.write('QUADS-DUMP:\n')
        for idx, operator in enumerate(self.quadruples['operator']):
            line = str(operator) + ' ' +converter(self.quadruples['operand1'][idx]) + ' ' + converter(self.quadruples['operand2'][idx]) + ' ' + converter(self.quadruples['result'][idx]) + '\n'
            file.write(line)

        file.close()
        



        





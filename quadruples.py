from semantics import Semantic
import sys

class quadruples():

    def __init__(self) -> None:

        self.semantic = Semantic()
        
        self.quadruples = {'operator': [], 'operand1': [], 'operand2': [], 'result': []}
        self.jumpStack = [] #to momentarily store jumps related to pending gotos

        self.counter = 1

        self.operatorsStack = [] # +, -, *, /, >, <, etc
        self.operandsStack = {'operand': [], 'type': []} #operands: a, b, c.. types: int, char, bool...

        self.result = 0

    def operand_push(self, operand, type):
        self.operandsStack['operand'].append(operand)
        self.operandsStack['type'].append(type)

        print("Operands Stack: ")
        print(self.operandsStack)

    #When an operator is pushed, it triggers an action to generate a quadruple based on the previously pushed operands.
    def operator_push(self, operator):
        self.operatorsStack.append(operator)
        self.generateQuad(operator)

        print("Operators Stack: ")
        print(self.operatorsStack)

    def generateQuad(self, operatorType):
        rightOperand = self.operandsStack['operand'].pop()
        rightType = self.operandsStack['type'].pop()
        leftOperand = self.operandsStack['operand'].pop()
        leftType = self.operandsStack['type'].pop()
        
        
        operator = self.operatorsStack.pop(0)

        try:
            result_Type = self.semantic.semantic_cube[leftType][operator][rightType]
        except:
            exitErrorText = " Error: Type mismatch in “" + leftOperand + ' ' + operator + ' ' + rightOperand  + '” -> “' + leftType + '” ' + operator + ' “' + rightType + '”'
            sys.exit(exitErrorText)

        if operatorType == '=':
            self.quadruples['operator'].append(operator)
            self.quadruples['operand1'].append(rightOperand)
            self.quadruples['operand2'].append(None)
            self.quadruples['result'].append(leftOperand)

        else: # + - * / > < >= <= == !=
            
            self.result += 1
            maskedResult = 'T' + str(self.result)

            self.quadruples['operator'].append(operator)
            self.quadruples['operand1'].append(leftOperand)
            self.quadruples['operand2'].append(rightOperand)
            self.quadruples['result'].append(maskedResult)

            self.operandsStack['operand'].append(maskedResult)
            self.operandsStack['type'].append(result_Type)

            #print("self.quadruples")
            #print(self.quadruples)
        
        self.counter += 1;

    def generateQuad_if(self):
        print("********** generateQuad_if")
        exp_type = self.operandsStack['type'].pop()
        result = self.operandsStack['operand'].pop()

        if exp_type != 'bool':

            exitErrorText = " Error: Type mismatch in " + exp_type + ' ' + result
            print(self.quadruples)
            print()
            sys.exit(exitErrorText)
        
        else:
            
            
            self.quadruples['operator'].append('GotoF')
            self.quadruples['operand1'].append(result)
            self.quadruples['operand2'].append(None)
            self.quadruples['result'].append('__')

            self.jumpStack.append(self.counter)

        self.counter +=1;

    def fillQuad(self, quadNum, result):
        print("self.quadruples")
        print(self.quadruples)
        print("quadNum: ", quadNum)
        print("result: ", result)
        self.quadruples['result'][quadNum-1] = result
        print(self.quadruples)

    def endQuad(self):
        print("********** endQuad")
        end = self.jumpStack.pop(0)
        self.fillQuad(end, self.counter)


    def generateQuad_else(self):
        print("********** generateQuad_else")
        self.quadruples['operator'].append('GOTO')
        self.quadruples['operand1'].append(None)
        self.quadruples['operand2'].append(None)
        self.quadruples['result'].append('__')

        self.jumpStack.append(self.counter)
        self.counter +=1;
        






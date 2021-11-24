from memory import memory
import pickle as pickle
import sys

class VirtualMachine():
    
    def __init__(self):

        #Initialize memory
        #self.memory = memory()
        self.MemStack = []
        self.MemStack.append(memory())

        #Create quadruples structure
        #self.quadruples = {'operator': [], 'operand1': [], 'operand2': [], 'result': []}

        #Load OBJ file to memory an quads
        self.loadOBJ()

        #Load to global & constant mem
        #scope, type, nodeIndex = self.memTranslator(memAddress)
        self.MemStack[0].globalMem = self.globalMemDict
        self.MemStack[0].constMem = self.constantMemDict
        #self.memory.allocateMem(scope, type, 1)
        #self.memory.insertIntoMem(memAddress, value)
        

        #self.memory.globalMem = self.globalMemDict
        #self.memory.constMem = self.constantMemDict


        #Load quadruples from dict (OBJ file)
        self.quadruples = self.quadsDict

        #ERA
        self.ERAstack = []

        #Params stack
        self.paramAddrStack = []
        self.paramValueStack = []
        self.paramTypeStack = []
        self.paramCounter = 0

        #GOSUB
        #Next quad counter stack
        self.nextQuadCounter = []
        self.GOSUBaddrStack = []
        self.funcInitQuadNum = 0

        #Process quadruples
        self.processQuads()

        # #Print quads for testing purposes
        # self.printQuads()

        # #Print memorys
        # print('GlobalMem')
        # print(self.MemStack[-1].globalMem)
        # print('localMem')
        # print(self.MemStack[-1].localMem)
        # print('tempMem')
        # print(self.MemStack[-1].tempMem)
        # print('constMem')
        # print(self.MemStack[-1].constMem)


    def memTranslator(self, memAddress):

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

        if int(str(memAddress)[0]) == 1: #global scope
            scope = 'global'
            nodeIndex = int(str(memAddress)[2:])
        elif int(str(memAddress)[0]) == 2: #local scope
            scope = 'local'
            nodeIndex = int(str(memAddress)[2:])
        elif int(str(memAddress)[0]) == 3: #temp scope
            scope = 'temporal'
            nodeIndex = int(str(memAddress)[2:])
        elif int(str(memAddress)[0]) == 4: #Constant scope
            scope = 'constant'
            nodeIndex = int(str(memAddress)[2:])

        return scope, type, nodeIndex
    
    def loadOBJ(self):

        Dicts = pickle.load( open ("OBJ.pkl", "rb") )
        #1 Global mem
        #2 Constant mem
        #3 Funcs Dir
        #4 Quads 
        self.globalMemDict = Dicts[0]
        self.constantMemDict = Dicts[1]
        self.funcsDict = Dicts[2]
        self.varsDict = Dicts[3]
        self.quadsDict = Dicts[4]

    def accessMemVal(self, scope, type, index):
        if scope == 'global':
            return self.MemStack[-1].globalMem[type]['value'][index]
        elif scope == 'local':
            return self.MemStack[-1].localMem[type]['value'][index]
        elif scope == 'temporal':
            return self.MemStack[-1].tempMem[type]['value'][index]
        elif scope == 'constant':
            return self.MemStack[-1].constMem[type]['value'][index]
    
    def createMemBlock_IfNotExists(self, result):
        scope, type, nodeIndex = self.memTranslator(result)
        try:
            self.accessMemVal(scope, type, nodeIndex)
        except:
            memAddress = self.MemStack[-1].allocateMem(scope, type, 1)
            #print('NEW MEM ADDRESS: ', memAddress)
    
    def ptrProcess(self, pointer):

        if pointer == None:
            return pointer

        ptr = str(pointer)
        if ptr[0] == '+':
            ptr = ptr[1:] #eliminate plus sign
            ptr1, ptr2 = ptr[:len(ptr)//2], ptr[len(ptr)//2:] #split in half

            #calculate new address
            ptr2 = self.MemStack[-1].getValFromMemory(int(ptr2))
            return int(ptr1) + int(ptr2) - 1 # offset
        else:
            return pointer
    
    def processQuads(self):

        def num(s):
            s = str(s)
            try:
                return int(s)
            except ValueError:
                return float(s)

        numOfQuads = len(self.quadruples['operator'])
        mainQuad = int(self.quadruples['result'][0])
        quadIdx = mainQuad

        while quadIdx <= numOfQuads:
            operator = self.quadruples['operator'][quadIdx-1]
            operand1 = self.ptrProcess(self.quadruples['operand1'][quadIdx-1])
            operand2 = self.ptrProcess(self.quadruples['operand2'][quadIdx-1])
            result = self.ptrProcess(self.quadruples['result'][quadIdx-1])

            if operator == '=':
                #if result memBlock doesnt exist, create it first
                self.createMemBlock_IfNotExists(result)

                #Then assign the value
                valToAssign = self.MemStack[-1].getValFromMemory(operand1)
                self.MemStack[-1].insertIntoMem(result, valToAssign)
                # print(result, valToAssign)
                # print('localMem')
                # print(self.MemStack[-1].localMem)

            elif operator == '+':
                #if result memBlock doesnt exist, create it first
                self.createMemBlock_IfNotExists(result)

                #Do the summ and store it in new temp val
                val1 = self.MemStack[-1].getValFromMemory(operand1)
                val2 = self.MemStack[-1].getValFromMemory(operand2)
                resultVal = num(val1) + num(val2)

                self.MemStack[-1].insertIntoMem(result, resultVal)
            
            elif operator == '-':
                #if result memBlock doesnt exist, create it first
                self.createMemBlock_IfNotExists(result)

                #Do the subtraction and store it in new temp val
                val1 = self.MemStack[-1].getValFromMemory(operand1)
                val2 = self.MemStack[-1].getValFromMemory(operand2)
                resultVal = num(val1) - num(val2)

                self.MemStack[-1].insertIntoMem(result, resultVal)
            
            elif operator == '*':
                #if result memBlock doesnt exist, create it first
                self.createMemBlock_IfNotExists(result)

                #Do the multiplication and store it in new temp val
                val1 = self.MemStack[-1].getValFromMemory(operand1)
                val2 = self.MemStack[-1].getValFromMemory(operand2)
                resultVal = num(val1) * num(val2)

                self.MemStack[-1].insertIntoMem(result, resultVal)
            
            elif operator == '/':
                #if result memBlock doesnt exist, create it first
                self.createMemBlock_IfNotExists(result)

                #Do the division and store it in new temp val
                val1 = self.MemStack[-1].getValFromMemory(operand1)
                val2 = self.MemStack[-1].getValFromMemory(operand2)
                resultVal = num(val1) / num(val2)

                self.MemStack[-1].insertIntoMem(result, resultVal)

            elif operator == '>':
                #if result memBlock doesnt exist, create it first
                self.createMemBlock_IfNotExists(result)

                #Do the biggerThan comparison and store it in new temp val
                val1 = self.MemStack[-1].getValFromMemory(operand1)
                val2 = self.MemStack[-1].getValFromMemory(operand2)
                resultVal = num(val1) > num(val2)
                self.MemStack[-1].insertIntoMem(result, resultVal)

            elif operator == '<':
                #if result memBlock doesnt exist, create it first
                self.createMemBlock_IfNotExists(result)

                #Do the lessThan comparison and store it in new temp val
                val1 = self.MemStack[-1].getValFromMemory(operand1)
                val2 = self.MemStack[-1].getValFromMemory(operand2)
                resultVal = num(val1) < num(val2)
                self.MemStack[-1].insertIntoMem(result, resultVal)

            elif operator == '<=':
                #if result memBlock doesnt exist, create it first
                self.createMemBlock_IfNotExists(result)

                #Do the lessThanOrEqual comparison and store it in new temp val
                val1 = self.MemStack[-1].getValFromMemory(operand1)
                val2 = self.MemStack[-1].getValFromMemory(operand2)
                resultVal = num(val1) <= num(val2)
                self.MemStack[-1].insertIntoMem(result, resultVal)

            elif operator == '>=':
                #if result memBlock doesnt exist, create it first
                self.createMemBlock_IfNotExists(result)

                #Do the biggerThanOrEqual comparison and store it in new temp val
                val1 = self.MemStack[-1].getValFromMemory(operand1)
                val2 = self.MemStack[-1].getValFromMemory(operand2)
                resultVal = num(val1) >= num(val2)
                self.MemStack[-1].insertIntoMem(result, resultVal)

            elif operator == '==':
                #if result memBlock doesnt exist, create it first
                self.createMemBlock_IfNotExists(result)

                #Do the lessThan comparison and store it in new temp val
                val1 = self.MemStack[-1].getValFromMemory(operand1)
                val2 = self.MemStack[-1].getValFromMemory(operand2)
                resultVal = num(val1) == num(val2)
                self.MemStack[-1].insertIntoMem(result, resultVal)

            elif operator == 'GotoF':
                #goto quad numb
                goto = int(result)

                boolVal = self.MemStack[-1].getValFromMemory(operand1)
                if not boolVal: #if it is indeed false
                    quadIdx = goto-1

            elif operator == 'GOTO':
                #goto quad numb
                goto = int(result)

                quadIdx = goto-1

            elif operator == 'ERA':
                #store ERA func name
                self.ERAstack.append(result)

            elif operator == 'RETURN':
                #1 temporarily store return address val
                self.returnAddressVal = self.MemStack[-1].getValFromMemory(result)

                #2 eliminate last memory object
                self.MemStack.pop()

                #3 Store returnAddressVal into GOSUB address
                #3.1 allocate memory first for that particular GOSUB address
                memAddress = self.GOSUBaddrStack.pop()
                self.createMemBlock_IfNotExists(memAddress)
                self.MemStack[-1].insertIntoMem(memAddress, self.returnAddressVal)

                #4 restore flow of quad counter quadIdx
                quadIdx = self.nextQuadCounter.pop()

            elif operator == 'ENDFUNC':
                #1 eliminate last memory object
                self.MemStack.pop()

                #2 restore flow of quad counter quadIdx
                quadIdx = self.nextQuadCounter.pop()

            elif operator == 'param':
                #store param addres and value
                self.paramAddrStack.append(operand1)
                paramVal = self.MemStack[-1].getValFromMemory(operand1)
                self.paramValueStack.append(paramVal)
                self.paramCounter += 1

                scope, type, nodeIndex = self.memTranslator(operand1)
                self.paramTypeStack.append(type)
            
            elif operator == 'GOSUB':
                #store next quad counter
                self.nextQuadCounter.append(quadIdx)

                #store GOSUB address
                self.GOSUBaddrStack.append(result)

                #search for function name that matches name, params and params type
                funcName = self.ERAstack.pop()

                #get the last parameters that correspond to the function inserted in stack
                tempParamsType = []
                # print("entrogosub")
                # print(self.paramTypeStack)
                # print(self.paramCounter)
                for x in range(self.paramCounter):
                    tempParamsType.insert(0, self.paramTypeStack.pop())

                functionFound = False
                paramTypeMatch = True
                exactMatch = False

                self.funcInitQuadNum = 0

                for idx, dictFuncName in enumerate(self.funcsDict['name']):
                    if funcName == dictFuncName: #if name matches
                        functionFound = True
                        #Count the number of params and check if matches
                        #print(self.funcsDict['parameters']['paramType'][idx])
                        if len(self.funcsDict['parameters']['paramType'][idx]) == self.paramCounter:
                            #Verify param type match
                            for idx2, dictParamType in enumerate(self.funcsDict['parameters']['paramType'][idx]):
                                if dictParamType != tempParamsType[idx2]:
                                    paramTypeMatch = False
                                    break
                            #If after param type match val is true, mark exact match as true and store function initDirection to point quad counter there
                            if paramTypeMatch:
                                exactMatch = True
                                self.funcInitQuadNum = self.funcsDict['initDirection'][idx]

                if not exactMatch:
                    if not functionFound:
                        exitErrorText = " Error: Function with name “" + funcName + '” not found.'
                        sys.exit(exitErrorText)
                    else:
                        exitErrorText = " Error: Function with name “" + funcName + '” found, but parameters given are the incorrect type:'
                        for paramType in tempParamsType:
                            exitErrorText = exitErrorText + str(paramType) + ' ' 
                        sys.exit(exitErrorText)

                #Point quads to the found function's execution code
                quadIdx = self.funcInitQuadNum - 1
                self.funcInitQuadNum = 0

                #Create new memory object
                self.MemStack.append(memory())

                #Point all constants and globals to new memory
                self.MemStack[-1].globalMem = self.MemStack[0].globalMem
                self.MemStack[-1].constMem = self.MemStack[0].constMem

                #Allocate and insert params values:
                #get the last parameter values that correspond to the function inserted in stack
                tempVals = []
                for x in range(self.paramCounter):
                    tempVals.insert(0, self.paramValueStack.pop())

                for idx, paramType in enumerate(tempParamsType):
                    memAddress = self.MemStack[-1].allocateMem('local', paramType, 1)
                    self.MemStack[-1].insertIntoMem(memAddress, tempVals[idx])
                    #print(self.MemStack[-1].localMem)

                #reset paramCounter to 0
                self.paramCounter = 0

                #Continue execution in quads loop
            
            elif operator == 'print':
                printText = str(self.MemStack[-1].getValFromMemory(result))
                #Remove quotations
                if printText[0] == '"':
                    printText = printText[1:]
                if printText[-1] == '"':
                    printText = printText[:-1]

                #newline
                if printText == '_nl':
                    print('\n', end='')
                else:
                    print(printText, end='')

            #Quadruples index
            quadIdx += 1

    def printQuads(self):
        print("QUADRUPLES: ")
        for idx, operator in enumerate(self.quadruples['operator']):
            print(idx+1, ', ', operator, ', ', self.quadruples['operand1'][idx], ', ', self.quadruples['operand2'][idx], ', ', self.quadruples['result'][idx])

#Initialize VM
VM = VirtualMachine()
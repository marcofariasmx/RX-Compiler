from memory import memory

class VirtualMachine():
    
    def __init__(self):

        #Initialize memory
        self.memory = memory()

        #Create quadruples structure
        self.quadruples = {'operator': [], 'operand1': [], 'operand2': [], 'result': []}

        #Load OBJ file to memory an quads
        self.loadOBJ()

        #Process quadruples
        self.processQuads()

        # #TEST ZONE
        # print('-----------------TEST ZONE-----------------')

        # #Test print quads
        # print("QUADRUPLES: ")
        # for idx, operator in enumerate(self.quadruples['operator']):
        #    print(idx+1, ', ', operator, ', ', self.quadruples['operand1'][idx], ', ', self.quadruples['operand2'][idx], ', ', self.quadruples['result'][idx])

        # #Test print mems
        # print("MEMORY: ")
        # print("Global: ")
        # print(self.memory.globalMem)
        # print("Local: ")
        # print(self.memory.localMem)
        # print("Temporal: ")
        # print(self.memory.tempMem)
        # print("Constant: ")
        # print(self.memory.constMem)

        #Test exists
        # idx = 1
        # type = 'int'
        # try:
        #     self.memory.constMem[type]['memIndex'][idx]
        #     print('Value: ', self.memory.constMem[type]['value'][idx], ' exists!')
        # except:
        #     print('Mem block doesnt exist')

        # try:
        #     val = self.accessMemVal('constant', type, 2)
        #     print('Val: ', val, ' exists!')
        # except:
        #     print('Mem block doesnt exist')

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
        # Using readlines()
        OBJfile = open('OBJ.txt', 'r')
        Lines = OBJfile.readlines()
        
        # .strip() strips the newline character
        lineType = ''
        for line in Lines:
            #count += 1
            if line.strip() == 'MEMORY-DUMP:':
                lineType = 'memory'
                #skip the line
                continue
            elif line.strip() == 'QUADS-DUMP:':
                lineType = 'quads'
                #skip the line
                continue
            if lineType == 'memory':
                #Allocate Mem and store values
                memTokens = line.strip().split(' ')
                memAddress = memTokens[0]
                value = memTokens[1]

                scope, type, nodeIndex = self.memTranslator(memAddress)
                self.memory.allocateMem(scope, type, 1)
                self.memory.insertIntoMem(memAddress, value)

            elif lineType == 'quads':
                quadTokens = line.strip().split(' ')
                self.quadruples['operator'].append(quadTokens[0])
                self.quadruples['operand1'].append(quadTokens[1])
                self.quadruples['operand2'].append(quadTokens[2])
                self.quadruples['result'].append(quadTokens[3])

    def accessMemVal(self, scope, type, index):
        if scope == 'global':
            return self.memory.globalMem[type]['value'][index]
        elif scope == 'local':
            return self.memory.localMem[type]['value'][index]
        elif scope == 'temporal':
            return self.memory.tempMem[type]['value'][index]
        elif scope == 'constant':
            return self.memory.constMem[type]['value'][index]
    
    def createMemBlock_IfNotExists(self, result):
        scope, type, nodeIndex = self.memTranslator(result)
        try:
            self.accessMemVal(scope, type, nodeIndex)
        except:
            memAddress = self.memory.allocateMem(scope, type, 1)
            #print('NEW MEM ADDRESS: ', memAddress)
    
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
            operand1 = self.quadruples['operand1'][quadIdx-1]
            operand2 = self.quadruples['operand2'][quadIdx-1]
            result = self.quadruples['result'][quadIdx-1]

            if operator == '=':
                #if result memBlock doesnt exist, create it first
                self.createMemBlock_IfNotExists(result)

                #Then assign the value
                valToAssign = self.memory.getValFromMemory(operand1)
                self.memory.insertIntoMem(result, valToAssign)

            elif operator == '+':
                #if result memBlock doesnt exist, create it first
                self.createMemBlock_IfNotExists(result)

                #Do the summ and store it in new temp val
                val1 = self.memory.getValFromMemory(operand1)
                val2 = self.memory.getValFromMemory(operand2)
                resultVal = num(val1) + num(val2)

                self.memory.insertIntoMem(result, resultVal)
            
            elif operator == '-':
                #if result memBlock doesnt exist, create it first
                self.createMemBlock_IfNotExists(result)

                #Do the subtraction and store it in new temp val
                val1 = self.memory.getValFromMemory(operand1)
                val2 = self.memory.getValFromMemory(operand2)
                resultVal = num(val1) - num(val2)

                self.memory.insertIntoMem(result, resultVal)
            
            elif operator == '*':
                #if result memBlock doesnt exist, create it first
                self.createMemBlock_IfNotExists(result)

                #Do the multiplication and store it in new temp val
                val1 = self.memory.getValFromMemory(operand1)
                val2 = self.memory.getValFromMemory(operand2)
                resultVal = num(val1) * num(val2)

                self.memory.insertIntoMem(result, resultVal)
            
            elif operator == '/':
                #if result memBlock doesnt exist, create it first
                self.createMemBlock_IfNotExists(result)

                #Do the division and store it in new temp val
                val1 = self.memory.getValFromMemory(operand1)
                val2 = self.memory.getValFromMemory(operand2)
                resultVal = num(val1) / num(val2)

                self.memory.insertIntoMem(result, resultVal)

            elif operator == '>':
                #if result memBlock doesnt exist, create it first
                self.createMemBlock_IfNotExists(result)

                #Do the biggerThan comparison and store it in new temp val
                val1 = self.memory.getValFromMemory(operand1)
                val2 = self.memory.getValFromMemory(operand2)
                resultVal = num(val1) > num(val2)
                self.memory.insertIntoMem(result, resultVal)

            elif operator == '<':
                #if result memBlock doesnt exist, create it first
                self.createMemBlock_IfNotExists(result)

                #Do the lessThan comparison and store it in new temp val
                val1 = self.memory.getValFromMemory(operand1)
                val2 = self.memory.getValFromMemory(operand2)
                resultVal = num(val1) < num(val2)
                self.memory.insertIntoMem(result, resultVal)

            elif operator == 'GotoF':
                #goto quad numb
                goto = int(result)

                boolVal = self.memory.getValFromMemory(operand1)
                if not boolVal: #if it is indeed false
                    quadIdx = goto-1

            elif operator == 'GOTO':
                #goto quad numb
                goto = int(result)

                quadIdx = goto-1
            
            elif operator == 'print':
                print(self.memory.getValFromMemory(result))

            #Quadruples index
            quadIdx += 1

#Initialize VM
VM = VirtualMachine()
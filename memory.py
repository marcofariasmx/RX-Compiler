class memory():

    def __init__(self):

        #with current configuration, it is possible to store up to
        #1000 variables (0 -> 999) for each type for each scope

        self.int_MemBaseDir = 1000
        self.float_MemBaseDir = 2000
        self.char_MemBaseDir = 3000
        self.bool_MemBaseDir = 4000
        self.pointer_MemBaseDir = 5000

        self.globalMem_BaseDir = 10000
        self.localMem_BaseDir = 20000
        self.tempMem_BaseDir = 30000
        self.constMem_BaseDir = 40000
        
        self.globalMem = {'int': {'memIndex': [], 'value': []}, 'float': {'memIndex': [], 'value': []}, 'char': {'memIndex': [], 'value': []}, 'bool': {'memIndex': [], 'value': []}, 'pointer': {'memIndex': [], 'value': []}}
        self.localMem = localMem().localMem
        #self.localMem = {'int': {'memIndex': [], 'value': []}, 'float': {'memIndex': [], 'value': []}, 'char': {'memIndex': [], 'value': []}, 'bool': {'memIndex': [], 'value': []}, 'pointer': {'memIndex': [], 'value': []}}
        self.tempMem = tempMem().tempMem
        #self.tempMem = {'int': {'memIndex': [], 'value': []}, 'float': {'memIndex': [], 'value': []}, 'char': {'memIndex': [], 'value': []}, 'bool': {'memIndex': [], 'value': []}, 'pointer': {'memIndex': [], 'value': []}}
        self.constMem = {'int': {'memIndex': [], 'value': []}, 'float': {'memIndex': [], 'value': []}, 'char': {'memIndex': [], 'value': []}, 'bool': {'memIndex': [], 'value': []}, 'pointer': {'memIndex': [], 'value': []}}
        #self.localMemStack = []
        #self.tempMemStack = []
        #self.localMemStack.append(localMem().localMem)
        #self.tempMemStack.append(tempMem().tempMem)
    
    def emptyMem(self):
        self.localMem.clear()
        self.tempMem.clear()
        self.localMem = localMem().localMem
        self.tempMem = tempMem().tempMem

    # def popMem(self):
    #     self.localMemStack.pop()
    #     self.tempMemStack.pop()

    # def newMem(self):
    #     self.localMemStack.append(localMem().localMem)
    #     self.tempMemStack.append(tempMem().tempMem)
    
    def allocateMem(self, scope, type, memBlocksSize):

        baseAddress = 0

        if type == 'int':
            memBaseDir = self.int_MemBaseDir
        elif type == 'float':
            memBaseDir = self.float_MemBaseDir
        elif type == 'char':
            memBaseDir = self.char_MemBaseDir
        elif type == 'bool':
            memBaseDir = self.bool_MemBaseDir
        elif type == 'pointer':
            memBaseDir = self.pointer_MemBaseDir

        if scope == 'global':
            if self.globalMem[type]['memIndex']: #If not empty, append
                baseAddress = self.globalMem[type]['memIndex'][-1] + 1
                for x in range(memBlocksSize):
                    self.globalMem[type]['memIndex'].append(self.globalMem[type]['memIndex'][-1] + 1)
                    self.globalMem[type]['value'].append(None)
            else: #it is empty, start in memBaseDir
                baseAddress = memBaseDir + self.globalMem_BaseDir
                self.globalMem[type]['memIndex'].append(memBaseDir + self.globalMem_BaseDir)
                self.globalMem[type]['value'].append(None)
                for x in range(memBlocksSize-1):
                    self.globalMem[type]['memIndex'].append(self.globalMem[type]['memIndex'][-1] + 1)
                    self.globalMem[type]['value'].append(None)

        elif scope == 'local':
            if self.localMem[type]['memIndex']: #If not empty, append
                baseAddress = self.localMem[type]['memIndex'][-1] + 1
                for x in range(memBlocksSize):
                    self.localMem[type]['memIndex'].append(self.localMem[type]['memIndex'][-1] + 1)
                    self.localMem[type]['value'].append(None)
            else: #it is empty, start in memBaseDir
                baseAddress = memBaseDir + self.localMem_BaseDir
                self.localMem[type]['memIndex'].append(memBaseDir + self.localMem_BaseDir)
                self.localMem[type]['value'].append(None)
                for x in range(memBlocksSize-1):
                    self.localMem[type]['memIndex'].append(self.localMem[type]['memIndex'][-1] + 1)
                    self.localMem[type]['value'].append(None)

        elif scope == 'temporal':
            if self.tempMem[type]['memIndex']: #If not empty, append
                baseAddress = self.tempMem[type]['memIndex'][-1] + 1
                for x in range(memBlocksSize):
                    self.tempMem[type]['memIndex'].append(self.tempMem[type]['memIndex'][-1] + 1)
                    self.tempMem[type]['value'].append(None)
            else: #it is empty, start in memBaseDir
                baseAddress = memBaseDir + self.tempMem_BaseDir
                self.tempMem[type]['memIndex'].append(memBaseDir + self.tempMem_BaseDir)
                self.tempMem[type]['value'].append(None)
                for x in range(memBlocksSize-1):
                    self.tempMem[type]['memIndex'].append(self.tempMem[type]['memIndex'][-1] + 1)
                    self.tempMem[type]['value'].append(None)

        elif scope == 'constant':
            if self.constMem[type]['memIndex']: #If not empty, append
                baseAddress = self.constMem[type]['memIndex'][-1] + 1
                for x in range(memBlocksSize):
                    self.constMem[type]['memIndex'].append(self.constMem[type]['memIndex'][-1] + 1)
                    self.constMem[type]['value'].append(None)
            else: #it is empty, start in memBaseDir
                baseAddress = memBaseDir + self.constMem_BaseDir
                self.constMem[type]['memIndex'].append(memBaseDir + self.constMem_BaseDir)
                self.constMem[type]['value'].append(None)
                for x in range(memBlocksSize-1):
                    self.constMem[type]['memIndex'].append(self.constMem[type]['memIndex'][-1] + 1)
                    self.constMem[type]['value'].append(None)

        return baseAddress

    def insertIntoMem(self, memAddress, value):

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
            self.globalMem[type]['value'][int(str(memAddress)[2:])] = value
        elif int(str(memAddress)[0]) == 2: #local type
            self.localMem[type]['value'][int(str(memAddress)[2:])] = value
        elif int(str(memAddress)[0]) == 3: #temp type
            self.tempMem[type]['value'][int(str(memAddress)[2:])] = value
        elif int(str(memAddress)[0]) == 4: #const type
            self.constMem[type]['value'][int(str(memAddress)[2:])] = value

    
    def getValFromMemory(self, memAddress):

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
            return self.globalMem[type]['value'][int(str(memAddress)[2:])]
        elif int(str(memAddress)[0]) == 2: #local type
            return  self.localMem[type]['value'][int(str(memAddress)[2:])]
        elif int(str(memAddress)[0]) == 3: #temp type
            return  self.tempMem[type]['value'][int(str(memAddress)[2:])]
        elif int(str(memAddress)[0]) == 4: #const type
            return  self.constMem[type]['value'][int(str(memAddress)[2:])]
            
    def searchConstant(self, type, valueToSearch):
        for idx, value in enumerate(self.constMem[type]['value']):
            if valueToSearch == value:
                return  self.constMem[type]['memIndex'][idx]
            else:
                return None

    def test(self):
        #allocate
        print('baseAddress: ', self.allocateMem('global', 'int', 1))
        print('baseAddress: ', self.allocateMem('global', 'int', 5))
        print('baseAddress: ', self.allocateMem('global', 'int', 1))
        

        #print
        print('GlobalMem:')
        print(self.globalMem)
        
        #insertIntoMem
        self.insertIntoMem(11001, 53)
        self.insertIntoMem(11006, 10)


        charAddress = self.allocateMem('global', 'char', 1)
        print('charAddress: ', charAddress)
        self.insertIntoMem(charAddress, 'A')

        charAddress = self.allocateMem('global', 'char', 1)
        print('charAddress: ', charAddress)
        self.insertIntoMem(charAddress, 'B')

        num1 = self.getValFromMemory(11001)
        num2 = self.getValFromMemory(11006)
        print('Result: ', num1+num2 )

        #print
        print('GlobalMem:')
        print(self.globalMem)

class localMem():
    def __init__(self):
        self.localMem = {'int': {'memIndex': [], 'value': []}, 'float': {'memIndex': [], 'value': []}, 'char': {'memIndex': [], 'value': []}, 'bool': {'memIndex': [], 'value': []}, 'pointer': {'memIndex': [], 'value': []}}

class tempMem():
    def __init__(self):
        self.tempMem = {'int': {'memIndex': [], 'value': []}, 'float': {'memIndex': [], 'value': []}, 'char': {'memIndex': [], 'value': []}, 'bool': {'memIndex': [], 'value': []}, 'pointer': {'memIndex': [], 'value': []}}
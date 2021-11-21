class FuncsDir_Vars_Table():

    def __init__(self) -> None:
        self.FuncsDirectory = {'name': [], 'type': [], 'initDirection': [], 'size': [], 'parameters' : {'paramType': [], 'paramIsArray': [], 'paramVarName': []}}

        self.VarsDirectory = {'name': [], 'type': [], 'ownerFunc': [], 'scope': [], 'isArray': [], 'memAddress': []}

    def insertFunction(self, funcName, funcType, initDirection, size, parameters):
        self.FuncsDirectory['name'].append(funcName)
        self.FuncsDirectory['type'].append(funcType)
        self.FuncsDirectory['initDirection'].append(initDirection)
        self.FuncsDirectory['size'].append(size)

        if parameters:
            for idx, paramType in enumerate(parameters['paramType']):
                self.FuncsDirectory['parameters']['paramType'].append(paramType)
                self.FuncsDirectory['parameters']['paramIsArray'].append(parameters['paramIsArray'][idx])
                self.FuncsDirectory['parameters']['paramVarName'].append(parameters['paramVarName'][idx])
        else:
            self.FuncsDirectory['parameters']['paramType'].append(None)
            self.FuncsDirectory['parameters']['paramIsArray'].append(None)
            self.FuncsDirectory['parameters']['paramVarName'].append(None)

        print(self.FuncsDirectory)
    
    def insertVariable(self, varName, varType, ownerFunc, scope, isArray, memAddress):
        self.VarsDirectory['name'].append(varName)
        self.VarsDirectory['type'].append(varType)
        self.VarsDirectory['ownerFunc'].append(ownerFunc)
        self.VarsDirectory['scope'].append(scope)
        self.VarsDirectory['isArray'].append(isArray)
        self.VarsDirectory['memAddress'].append(memAddress)

        print(self.VarsDirectory)

    def getVarTypeAndAddress_Global(self, varName):
        typeAndAddress = []
        for idx, varInDir in enumerate(self.VarsDirectory['name']):
            if varInDir == varName:
                if self.VarsDirectory['scope'][idx] == 'global':
                    typeAndAddress.append(self.VarsDirectory['type'][idx])
                    typeAndAddress.append(self.VarsDirectory['memAddress'][idx])
                    return typeAndAddress
        
        return None


    def action(self):
        return None

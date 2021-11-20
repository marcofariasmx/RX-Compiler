class FuncsDir_Vars_Table():

    def __init__(self) -> None:
        self.FuncsDirectory = {'name': [], 'type': [], 'initDirection': [], 'size': [], 'parameters' : {'paramType': [], 'paramIsArray': [], 'paramVarName': []}}

        self.VarsDirectory = {'name': [], 'type': [], 'ownerFunc': [], 'scope': [], 'isArray': []}

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
    
    def insertVariable(self, varName, varType, ownerFunc, scope, isArray):
        self.VarsDirectory['name'].append(varName)
        self.VarsDirectory['type'].append(varType)
        self.VarsDirectory['ownerFunc'].append(ownerFunc)
        self.VarsDirectory['scope'].append(scope)
        self.VarsDirectory['isArray'].append(isArray)

        print(self.VarsDirectory)

    def getVarType_Global(self, varName):
        for idx, varInDir in enumerate(self.VarsDirectory['name']):
            if varInDir == varName:
                if self.VarsDirectory['scope'][idx] == 'global':
                    #print("PRUEBAAAAAAAAAAAAA")
                    #print(self.VarsDirectory['name'][idx])
                    #print(self.VarsDirectory['ownerFunc'][idx])
                    #print(self.VarsDirectory['scope'][idx])
                    return self.VarsDirectory['type'][idx]
        
        return None


    def action(self):
        return None

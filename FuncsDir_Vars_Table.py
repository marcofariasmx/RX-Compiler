class FuncsDir_Vars_Table():

    def __init__(self) -> None:
        self.FuncsDirectory = {'name': [], 'type': [], 'initDirection': [], 'size': [], 'parameters' : {'paramType': [], 'paramVarName': []}}

        self.VarsDirectory = {'name': [], 'type': [], 'ownerFunc': [], 'scope': []}

    def insertFunction(self, funcName, funcType, initDirection, size, parameters):
        self.FuncsDirectory['name'].append(funcName)
        self.FuncsDirectory['type'].append(funcType)
        self.FuncsDirectory['initDirection'].append(initDirection)
        self.FuncsDirectory['size'].append(size)

        if parameters:
            for param in parameters:
                self.FuncsDirectory['parameters']['paramType'].append(param['paramType'])
                self.FuncsDirectory['parameters']['paramVarName'].append(param['paramVarName'])
        else:
            self.FuncsDirectory['parameters']['paramType'].append(None)
            self.FuncsDirectory['parameters']['paramVarName'].append(None)

        print(self.FuncsDirectory)
    
    def insertVariable(self, varName, varType, ownerFunc, scope):
        self.VarsDirectory['name'].append(varName)
        self.VarsDirectory['type'].append(varType)
        self.VarsDirectory['ownerFunc'].append(ownerFunc)
        self.VarsDirectory['scope'].append(scope)

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

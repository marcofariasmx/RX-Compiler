from memory import memory
import pickle as pickle

#memory = memory()

#memory.test()

myDicts = pickle.load( open ("OBJ.pkl", "rb") )

#1 Global mem
#2 Constant mem
#3 Funcs Dir
#4 Quads 
for idx, dict in enumerate(myDicts):
    print("DICT ", idx+1)
    print(dict)

print("QUADRUPLES: ")
for idx, operator in enumerate(myDicts[3]['operator']):
    print(idx+1, ', ', operator, ', ', myDicts[3]['operand1'][idx], ', ', myDicts[3]['operand2'][idx], ', ', myDicts[3]['result'][idx])
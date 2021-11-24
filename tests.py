from memory import memory
import pickle as pickle

myDicts = pickle.load( open ("OBJ.pkl", "rb") )

#1 Global mem
#2 Constant mem
#3 Funcs Dir
#4 Quads 
dictName = ['Global mem', 'Constant mem', 'Funcs Dir', 'Vars Directory', 'Quads']
for idx, dict in enumerate(myDicts):
    print("DICT ", idx+1, ': ', dictName[idx])
    print(dict)

print("QUADRUPLES: ")
for idx, operator in enumerate(myDicts[4]['operator']):
    print(idx+1, ', ', operator, ', ', myDicts[4]['operand1'][idx], ', ', myDicts[4]['operand2'][idx], ', ', myDicts[4]['result'][idx])
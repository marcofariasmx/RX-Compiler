import sys
from yaccParser import MyParser

if __name__ == '__main__':

    parser = MyParser()
    lexer =  parser.lexer

    if len(sys.argv) > 1:
        file = sys.argv[1]
        try:
            f = open(file, 'r')
            data = f.read()
            f.close()
            result = parser.parser.parse(data)
            if result == "COMPILED":
                parser.lexer.test(data)
                print("Valid input")
                print(result)
        except EOFError:
            print(EOFError)
    else:
        print("No file to compile found")
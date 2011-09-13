#! /usr/bin/env python
import sys
import re, fileinput
import pyPEG
from pyPEG import parse
from pyPEG import keyword, _and, _not, ignore
#from xmlast import pyAST2XML

# pyPEG:
#                    0: following element is optional
#                   -1: following element can be omitted or repeated endless
#                   -2: following element is required and can be repeated endless

def comment():          return [re.compile(r"//.*"), re.compile("/\*.*?\*/", re.S)]
def module():           return re.compile(r"module")
def rawstring():        return [re.compile(r"\".*?\"")]
def literal():          return re.compile(r'\d*\.\d*|\d+|".*?"')
def symbol():           return re.compile(r"\w+")
def typedec():          return re.compile(r"var|func|pred")
def dot():              return re.compile(r"\.")

def TFI(): return "<+"
def IFT(): return "+>"
def IFF(): return "->"
def FFI(): return "<-"
def DUB(): return "<>"
def LS(): return "<<"
def RS(): return ">>"
def FWD(): return ">"
def BAK(): return "<"
def PTFI(): return "|<+"
def PIFT(): return "|+>"
def PIFF(): return "|->"
def PFFI(): return "|<-"
def PDUB(): return "|<>"
def PLS(): return "|<<"
def PRS(): return "|>>"
def PFWD(): return "|>"
def PBAK(): return "|<"
def SPACE(): return ""

arrow = [ TFI, IFT, IFF, FFI, DUB, LS, RS, FWD, BAK,
          PTFI, PIFT, PIFF, PFFI, PDUB, PLS, PRS, PFWD, PBAK, SPACE]

#def pipeq():            return re.compile(r"\|=")
def pipeq():            return "|="

def arr():              return arrow
def ident():            return symbol, -1, (dot, symbol)
def assign():           return pipeq, ident
def place():            return [assign, ident, parameterlist]

#def expression():       return [(place, -1, (arr, place)),
#                                (place, expression)]

def expression():       return place, -1, (arr, place)
def declaration():      return typedec, symbol, "=", ident
def statement():        return [declaration, expression, comment, rawstring], ";"
def block():            return "{", -1, [rawstring, statement], "}"
def parameterlist():    return "(", 0, (symbol, -1, (",", symbol)), ")"
def function():         return keyword("def"), symbol, parameterlist, block
def mod():              return "module", symbol, "{", -1, [function, rawstring], "}"

# simpleLanguage <- function;
def simpleLanguage():   return -1, mod

pyPEG.print_trace = False

files = fileinput.input()
result = parse( simpleLanguage(), 
                files,
                True,
                comment,
                lineCount = True,
                )

'''
def out(s): sys.stdout.write(s)

def pretty_print(prsr, depth=0, inlist=False):    
    if type(prsr) == list:
        for p in prsr:
            pretty_print(p, depth+1)

    if prsr.__class__.__name__ == 'Symbol':
        out("\n")
        out(" " * depth)   
        out('<%s line="%s"' % (str(prsr[0]), prsr.__name__.line))
        if type(prsr[1]) == list:
            out(">")
            pretty_print(prsr[1], depth+1, True)            
            #out("{{%s}}" % prsr)
        else: 
            out(' val="%s">' % str(prsr[1]))

        out('</%s>' % (str(prsr[0])))

#pretty_print(result)


def pretty_print(prsr, depth=0, inlist=False):    
    if type(prsr) == list:
        for p in prsr:
            pretty_print(p, depth+1)
        out(")")

    if prsr.__class__.__name__ == 'Symbol':
        out("\n")
        out(" " * depth)
        out('(%s "%s"' % (str(prsr[0]), prsr.__name__.line))
        if type(prsr[1]) == list:
            pretty_print(prsr[1], depth+1, True)            
        else: 
            out(' "%s")' % str(prsr[1]))
'''



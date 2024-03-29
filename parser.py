#! /usr/bin/env python
import sys
import re, fileinput
import pyPEG
from pyPEG import parse
from pyPEG import keyword, _and, _not, ignore

# pyPEG:
#                    0: following element is optional
#                   -1: following element can be omitted or repeated endless
#                   -2: following element is required and can be repeated endless

def comment():          return [re.compile(r"//.*"), re.compile("/\*.*?\*/", re.S)]
def module():           return re.compile(r"module")
def rawstring():        return [re.compile(r"\".*?\"")]
def literal():          return re.compile(r'\d*\.\d*|\d+|".*?"')
#def symbol():           return re.compile(r"\w+")
def symbol():           return re.compile(r"[A-z]+[A-z|0-9|_]*")
def typedec():          return re.compile(r"var|func|pred|ctrl")
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
def ID(): return "=>"
def DI(): return "<="
def SPACE(): return ""

arrow = [ TFI, IFT, IFF, FFI, DUB, LS, RS, FWD, BAK,
          PTFI, PIFT, PIFF, PFFI, PDUB, PLS, PRS, PFWD, PBAK, SPACE]

#def pipeq():            return re.compile(r"\|=")
def pipeq():            return "|="

def arr():              return arrow
def ident():            return symbol, -1, (dot, symbol)
def assign():           return pipeq, [ident, tupe]
def place():            return [assign, ident, tupe]
def expression():       return place, -1, (arr, place)
def declaration():      return typedec, symbol, "=", [ident, literal]
def statement():        return [declaration, expression, comment, rawstring], -2, ";"
def block():            return "{", -1, [rawstring, statement], "}"
def tupe():             return "(", 0, ([literal, ident], -1, (",", [literal, ident])), ")"
def parameterlist():    return "(", 0, (typedec, symbol, -1, (",", typedec, symbol)), ")"
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

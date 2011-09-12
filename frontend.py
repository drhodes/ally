#! /usr/bin/env python
from parser import *
import sys

def out(s): sys.stdout.write(s)

def levelout(s, n): 
    out(n*"  ")
    out(s)

def newline(): out("\n")

def pretty(pt, depth=0):
    if type(pt) == list:        
        for node in pt:
            pretty(node, depth+1)        
        return            
    if type(pt) == unicode:
        levelout(pt, depth+1)        
        newline()
    else:
        levelout(pt.__name__, depth)
        out(": ")
        out(pt.__name__.line)
        newline()
        pretty(pt.what, depth+1)

tree = result[0] 
print pretty(tree)


def tbl(n):
    d = {
        "comment":comment,
        "module":module,
        "rawstring":rawstring,
        "literal":literal,
        "symbol":symbol,
        "typedec":typedec,
        "dot":dot,
        "TFI":TFI,
        "IFT":IFT,
        "IFF":IFF,
        "FFI":FFI,
        "DUB":DUB,
        "LS":LS,
        "RS":RS,
        "FWD":FWD,
        "BAK":BAK,
        "PTFI":PTFI,
        "PIFT":PIFT,
        "PIFF":PIFF,
        "PFFI":PFFI,
        "PDUB":PDUB,
        "PLS":PLS,
        "PRS":PRS,
        "PFWD":PFWD,
        "PBAK":PBAK,
        "SPACE":SPACE,
        "pipeq":pipeq,
        "arr":arr,
        "ident":ident,
        "assign":assign,
        "place":place,
        "expression":expression,
        "declaration":declaration,
        "statement":statement,
        "block":block,
        "parameterlist":parameterlist,
        "function":function,
        "mod":mod,
        }
    return d[n]


def symgen():
    ID = 0
    while 1:
        ID += 1
        yield "_id__%d__" % ID
SYM = symgen()

def maketree(pt):
    if type(pt) == list:        
        ren = []
        for node in pt:
            ren.append(maketree(node))
        return ren

    if type(pt) == unicode:
        return pt

    else:
        name = pt.__name__
        line = pt.__name__.line        
        return tbl(name)(name, line, maketree(pt.what))

class Node(object):
    def __init__(self, args):
        self.line = args[1]
        self.args = args[2:]

    def cls_name(self):
        return self.__class__.__name__

    def error(self, msg):
        print "slur: Error @ %s" % self.line
        print msg
        raise ValueError("ally: Error @ %s" % self.line)


'''
comment
module
rawstring
literal
symbol
typedec
dot
TFI
IFT
IFF
FFI
DUB
LS
RS
FWD
BAK
PTFI
PIFT
PIFF
PFFI
PDUB
PLS
PRS
PFWD
PBAK
SPACE
pipeq
arr
ident
assign
place
expression
declaration
statement
block
parameterlist
function
mod
'''

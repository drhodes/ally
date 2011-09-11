#! /usr/bin/env python
# -*- python -*-

import time
from pyparsing import (
    alphanums,
    Literal,
    Word,
    OneOrMore,
    Suppress,
    ZeroOrMore
    )

#-----------------------------------------------------------------------------
DoubleArrow = Literal(">>")
SingleArrow = Literal(">")
BothArrow = Literal("<>")
IdArrow = Literal("=>")

Arrow = DoubleArrow | SingleArrow | BothArrow | IdArrow

idstring = ("id:" + str(x) for x in xrange(0, int(1e7)))

class ArrowClass(object):
    def __init__(self, arr):        
        self.arr = arr[0]    

    def string(self):
        return str(self.arr)
                
    def gensymbol(self):
        return self.__class__.__name__ + ":anon:" + idstring.next()

    def gencode(self):        
        if self.arr == ">>":
            return " > %s > " % self.gensymbol() 
        if self.arr == ">":
            return " > " 
        if self.arr == "=>":
            return " > id > "
        if self.arr == "<>":
            return " <> "
    
    def __repr__(self):
        return self.gencode() #"<Arrow `" + self.arr + "` >"

Arrow.setParseAction(ArrowClass)
#-----------------------------------------------------------------------------

Equal = Literal("=")
Mac = Literal("mac")
Ident = Word("1234567890!@#$%^&*()_+-=?/|:." + alphanums)
LeftStache = Suppress("{")
RightStache = Suppress("}")
Let = Literal("let")
Semi = Suppress(";")
Return = Literal("return")

anychar = temp = map(chr, range(10, 150))
anychar.remove("{")
anychar.remove("}")
anychar = ''.join(anychar)

NoStaches = Word(anychar)

#-----------------------------------------------------------------------------
Macro = Mac + OneOrMore(Ident) + LeftStache + ZeroOrMore(NoStaches) + RightStache

class MacroClass(object):
    def __init__(self, mac):
        self.name = mac[1]
        self.vars = list(mac[2:-1])
        self.text = mac[-1]
        
    def __repr__(self):
        return self.text
                  
Macro.setParseAction(MacroClass)

#-----------------------------------------------------------------------------
LetStatement = Let + Ident + Equal + Ident + Semi


#-----------------------------------------------------------------------------
ArrowStatment = ZeroOrMore(Ident + Arrow) + Ident + Semi

class ArrowStatmentClass(object):
    def __init__(self, parse):
        self.parse = parse
        self.gen()

    def gen_place(self):
        return "place:" + idstring.next()

    def gen_func(self):
        return "func:" + idstring.next()
   
    def make_trips(self, els):
        accum = []
        els = list(els)
        while len(els) > 1:
            # take 3 
            cur = els[:3]

            fst = cur[0]
            arr = cur[1].string()
            lst = cur[2]

            if arr == ">":
                accum.append( (fst, ">", lst) )

            if arr == ">>":
                # get a anon place.
                tmp = self.gen_place()
                accum.append( (fst, ">", tmp) )
                accum.append( (tmp, ">", tmp) )

            if arr == "=>":
                tmp = self.gen_func()
                accum.append( (fst, ">", tmp) )
                accum.append( (tmp, ">", fst) )                

            if arr == "<>":
                # a cycle
                accum.append( (fst, ">", lst) )
                accum.append( (lst, ">", fst) )

            # drop 2
            els = els[2:]            
        return accum
                
    def gen(self):
        return self.make_trips(self.parse)

    def __repr__(self):
        return str(self.gen())


ArrowStatment.setParseAction(ArrowStatmentClass)
        



#-----------------------------------------------------------------------------
Function = Ident + OneOrMore(Ident) + LeftStache +\
    ZeroOrMore(LetStatement) + OneOrMore(ArrowStatment) + RightStache

Program = ZeroOrMore( Function | Macro )

#Program.ParseString




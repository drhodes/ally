#! /usr/bin/env python
import parser
from parser import result
import sys

from pass1 import (
    Node,
    parameterlist,
    )

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

class Pipe(Node):
    def __init__(self, *args, **kwargs):
        Node.__init__(self, ("Pipe Void",) + args)
        self.arrString = kwargs["arrstr"]

    def show(self):
        return self.arr_string()
    
    def arr_string(self):
        return self.arrString

class comment(Node):
    def __init____(self, *args):
        Node.__init__(self, args)
        
class module(Node):
    def __init__(self, *args):
        Node.__init__(self, args)
        
class rawstring(Node):
    def __init__(self, *args):
        Node.__init__(self, args)
    def show(self):
        return self.args[0][0]
        
class literal(Node):
    def __init__(self, *args):
        Node.__init__(self, args)
    def show(self):
        return self.args[0]

class symbol(Node):
    def __init__(self, *args):
        Node.__init__(self, args)
    def show(self):
        return self.args[0]
        
class typedec(Node):
    def __init__(self, *args):
        Node.__init__(self, args)
    def show(self):
        return self.args[0]

class dot(Node):
    def __init__(self, *args):
        Node.__init__(self, args)

class TFI(Pipe):
    def __init__(self, *args):
        Pipe.__init__(self, args, arrstr="<+" )

class IFT(Pipe):
    def __init__(self, *args):
        Pipe.__init__(self, args, arrstr="+>" )

class IFF(Pipe):
    def __init__(self, *args):
        Pipe.__init__(self, args, arrstr="->" )

class FFI(Pipe):
    def __init__(self, *args):
        Pipe.__init__(self, args, arrstr="<-" )

class DUB(Pipe):
    def __init__(self, *args):
        Pipe.__init__(self, args, arrstr="<>" )    

class LS(Pipe):
    def __init__(self, *args):
        Pipe.__init__(self, args, arrstr="<<" )

class RS(Pipe):
    def __init__(self, *args):
        Pipe.__init__(self, args, arrstr=">>" )

class FWD(Pipe):
    def __init__(self, *args):
        Pipe.__init__(self, args,arrstr= ">" )

class BAK(Pipe):
    def __init__(self, *args):
        Pipe.__init__(self, args,arrstr= "<" )


class SPACE(Pipe):
    def __init__(self, *args):
        Pipe.__init__(self, args, arrstr="<" )

class pipeq(Node):
    def __init__(self, *args):
        Node.__init__(self, args)
        self.symid = SYM.next()

    def show(self):
        temp = "tmp_%s"
        return temp % self.symid

class arr(Node):
    def __init__(self, *args):
        Node.__init__(self, args)

    def show(self):        
        return str(self.args[0][0].show())

class ident(Node):
    def __init__(self, *args):
        Node.__init__(self, args)
    def show(self):
        return self.args[0][0].show()
        
class assign(Node):
    def __init__(self, *args):
        Node.__init__(self, args)

    def gen_local(self):        
        temp = "var %s = %s;"
        a = self.args[0][0].show()
        b = self.args[0][1].show()
        return [temp % (a, b)]

    def show(self):
        temp = "%s"
        a = self.args[0][0].show()
        b = self.args[0][1].show()
        return temp % (a)

class place(Node):
    def __init__(self, *args):
        Node.__init__(self, args)        


    def show(self):
        return self.args[0][0].show()
              
class expression(Node):
    def __init__(self, *args):
        Node.__init__(self, args)

    def decompose_arrow(self, a, b, c):        
        stmts = []

        def knit(fst, arrstr, snd):
            return "%s %s %s; \n" % (fst.show(), arrstr, snd.show())
        
        # split arrows and flip them, to reduce work in the next pass.
        if b.show() == "<>":
            stmts.append( knit(a, ">", c) )
            stmts.append( knit(c, ">", a) )
        elif b.show() == "<<":
            stmts.append( knit(c, ">>", a))
        elif b.show() == "<+":
            stmts.append( knit(c, "+>", a))
        elif b.show() == "<-":
            stmts.append( knit(c, "->", a))
        elif b.show() == "<":
            stmts.append( knit(c, ">", a))                      
        else:                
            stmts.append( knit(a, b.show(), c))
        return stmts


    def show1(self, items):
        return items[0].show() + ";"

    def show(self):     
        showlist = []              
        items = list(self.args[0])
        if len(items) == 1:
            return self.show1(items)

        accum = []        
        while 1:
            if len(items) == 0:
                break

            if len(items) == 3:
                accum.append(items)
                break
            accum.append(items[:3])            
            items = items[2:]                
        
        stmts = []

        for a,b,c in accum:
            for stmt in self.decompose_arrow(a, b, c):                
                stmts.append(stmt)
        return ''.join(stmts)


class declaration(Node):
    def __init__(self, *args):
        Node.__init__(self, args)
    def show(self):
        temp = "%s %s = %s;"
        typedec = self.args[0][0].show()
        lhs = self.args[0][1].show()
        rhs = self.args[0][2].show()
        return temp % (typedec, lhs, rhs)            

class statement(Node):
    def __init__(self, *args):
        Node.__init__(self, args)
    def show(self):
        return self.args[0][0].show()

class block(Node):
    def __init__(self, *args):
        Node.__init__(self, args)
    def show(self):
        temp = []        
        for item in self.args[0]:
            temp.append(item.show())
        return "\n".join(temp)

class tupe(Node):
    def __init__(self, *args):
        Node.__init__(self, args)
    def show(self):
        temp = "(%s)" % ', '.join([x.show() for x in self.args[0]])
        return temp
        
class function(Node):
    def __init__(self, *args):
        Node.__init__(self, args)
    def show(self):
        temp = "def %s %s {\n%s\n}"
        name = self.args[0][0]
        params = self.args[0][1]
        block = self.args[0][2]
        return temp % (name.show(), params.show(), block.show())

# ------------------------------------------------------------------        
class mod(Node):
    def __init__(self, *args):
        Node.__init__(self, args)

    def show(self, quiet=False):
        name = self.args[0][0]
        output = ""
        output += ("module %s {\n" % name.show())
        for item in self.args[0][1:]:
            if quiet:
                item.show()
            else:
                output += (item.show()+"\n")
        output += "\n}\n"
        return output


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
        "SPACE":SPACE,
        "arr":arr,
        "ident":ident,
        "assign":assign,
        "place":place,
        "expression":expression,
        "declaration":declaration,
        "statement":statement,
        "tupe": tupe,
        "block":block,
        "parameterlist":parameterlist,
        "function":function,
        "mod":mod,
        }
    return d[n]

tree = result[0]

t = maketree(tree)
filename = "./temp/tmpfile.ally"

# second pass

tmpfile = open(filename, 'w')
tmpfile.write(t.show())



# second pass
# tmpfile = open(filename, 'w')

# import fileinput
# from pyPEG import parse
# from parser import simpleLanguage
# files = fileinput.FileInput(filename)

# result = parse( simpleLanguage(), 
#                 files,
#                 True,
#                 parser.comment,
#                 lineCount = True,
#                 )
# tree2 = maketree(result[0])


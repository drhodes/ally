#! /usr/bin/env python
import parser
from parser import result
from utility import *
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

def symgen():
    ID = 0
    while 1:
        ID += 1
        yield "_pipeid_%d_" % ID
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
        print "ally: Error @ %s" % self.line
        print msg        
        raise ValueError("ally: Error @ %s" % self.line)

    def line_comment(self):
        return "      /* :::: %s */" % self.line

class Pipe(Node):
    def __init__(self, *args, **kwargs):
        Node.__init__(self, ("Pipe Void",) + args)
        self.arrString = kwargs["arrstr"]

    def show(self, lastpipe=None):
        if not self.isPipedArrow():
            return self.arrString
        if lastpipe == None:
            return self.arrString
        else:
            temp = "%s %s "            
            return temp % (lastpipe, self.without_pipe())

    def isPipedArrow(self):
        return self.arr_string()[0] == "|"

    def without_pipe(self):
        s = self.arr_string()
        if s[0] == "|":
            return s[1:] 
        else:
            return s
    
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
    def show(self): return "."

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

class PTFI(Pipe):
    def __init__(self, *args):
        Pipe.__init__(self, args, arrstr="|<+" )

class PIFT(Pipe):
    def __init__(self, *args):
        Pipe.__init__(self, args, arrstr="|+>" )

class PIFF(Pipe):
    def __init__(self, *args):
        Pipe.__init__(self, args, arrstr="|->" )

class PFFI(Pipe):
    def __init__(self, *args):
        Pipe.__init__(self, args, arrstr="|<-" )

class PDUB(Pipe):
    def __init__(self, *args):
        Pipe.__init__(self, args, arrstr="|<>" )

class PLS(Pipe):
    def __init__(self, *args):
        Pipe.__init__(self, args, arrstr="|<<" )

class PRS(Pipe):
    def __init__(self, *args):
        Pipe.__init__(self, args, arrstr="|>>" )

class PFWD(Pipe):
    def __init__(self, *args):
        Pipe.__init__(self, args, arrstr="|>" )

class PBAK(Pipe):
    def __init__(self, *args):
        Pipe.__init__(self, args, arrstr="|<" )

class SPACE(Pipe):
    def __init__(self, *args):
        Pipe.__init__(self, args, arrstr="<" )

class pipeq(Node):
    def __init__(self, *args):
        Node.__init__(self, args)
        self.symid = SYM.next()

    def isPipeq(self): return True

    def show(self):
        temp = "_%s_"
        return temp % self.symid
        
class arr(Node):
    def __init__(self, *args):
        Node.__init__(self, args)

    def isPipeq(self):
        return False#return self.args[0][0].isPipeq()
    #return False
    def isPipedArrow(self):
        return self.args[0][0].isPipedArrow()

    def show(self, lastpipe):        
        return str(self.args[0][0].show(lastpipe))

class ident(Node):
    def __init__(self, *args):
        Node.__init__(self, args)
    def show(self):        
        temp = ''.join(x.show() for x in self.args[0])
        return temp
        
class assign(Node):
    def __init__(self, *args):
        Node.__init__(self, args)

    def isPipeq(self):
        return self.args[0][0].isPipeq()
    
    def gen_local(self):        
        temp = "var %s = %s;"
        a = self.args[0][0].show()
        b = self.args[0][1].show()
        return [temp % (a, b)]

    def show(self):
        temp = "%s"
        a = self.args[0][0].show()
        b = self.args[0][1].show()
        return b
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # This may be a source of confusion.
        # think if there needs to be a temporary place for pipeq's

        # i commented this when converting the pipe temp vars
        # back to the real deal
        return temp % (a)

class place(Node):
    def __init__(self, *args):
        Node.__init__(self, args)        

    def isPipeq(self):
        if self.args[0][0].cls_name() == "assign":
            return self.args[0][0].isPipeq()
        return False
    def gen_local(self):
        if self.isPipeq():
            return self.args[0][0].gen_local()

    def isPipedArrow(self):
        return False 

    def show(self, lastpipe=None):
        return self.args[0][0].show()
              
class expression(Node):
    def __init__(self, *args):
        Node.__init__(self, args)
        self.locals = []

    def gen_locals(self):
        for item in self.args[0]:
            if item.isPipeq():                
                self.locals.extend(item.gen_local())
        
    def show_locals(self):
        return "\n".join(self.locals) + "\n"

    def show(self):     
        self.gen_locals()
        showlist = []
        lastpipe = None        
        was_last_item_pipe = False
              
        items = list(self.args[0])
        accum = []

        for item in items:
            if item.isPipeq():
                lastpipe = item.show(lastpipe)
            if item.isPipedArrow():
                if lastpipe != None:
                    accum.append("; %s\n" % item.line_comment()) 
                    accum.append(lastpipe)
                    accum.append(item.args[0][0].without_pipe())                    

                else:
                    accum.append(item.show())                
            if not item.isPipedArrow():
                accum.append(item.show(lastpipe))


        exprs = " ".join(accum) + ";"
        return exprs
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # the above return statement short circuits this code.

        return self.show_locals() + exprs


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
        return self.args[0][0].show() + self.line_comment()

class block(Node):
    def __init__(self, *args):
        Node.__init__(self, args)
    def show(self):
        temp = []
        for item in self.args[0]:
            temp.append(item.show())
        return "\n".join(temp)

class parameterlist(Node):
    def __init__(self, *args):
        Node.__init__(self, args)
    def show(self):        
        pairs = pairify(self.args[0])
        items = []
        for a, b in pairs:
            items.append("%s %s" % (a.show(), b.show()))
        result = "(%s)" % ", ".join(items)
        return result

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
        temp = "def %s %s { %s \n%s\n}"
        name = self.args[0][0]
        params = self.args[0][1]
        block = self.args[0][2]
        return temp % (name.show(), 
                       params.show(), 
                       self.line_comment(),
                       block.show())
    
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
        "tupe":tupe,
        "function":function,
        "mod":mod,
        }
    return d[n]


t = maketree(tree)
filename = "./temp/tmpfile-pass-1.ally"
tmpfile = open(filename, 'w')
tmpfile.write(t.show())
tmpfile.close()

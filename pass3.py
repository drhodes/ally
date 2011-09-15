#! /usr/bin/env python
import parser
from parser import result
import sys

from pass1 import (
    Node,
    parameterlist,
    function,
    TFI,
    IFT,
    IFF,
    FFI,
    DUB,
    LS,
    RS,
    FWD,
    BAK,
    SPACE,
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
        val = self.args[0]
        '''
        if "." in val:
            return "float (%s)" % val
        else:
            return "int (%s)" % val
            '''
        return val

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

    def glue(self, a, b, c):
        return "%s %s %s;" % (a, b, c)    

    def distribute_both(self, a, b, c):        
        stmts = []
        a_vals = a.args[0][0].args[0]
        for aval in a_vals:
            stmts.extend(self.distribute_right(aval, b, c))
        return stmts

    def distribute_left(self, a, b, c):
        "(a, b) > c; ==> a>c; a>c;"
        a_vals = a.args[0][0].args[0]
        a_strs = [x.show() for x in a_vals]
        b_str = b.show()
        c_str = c.show()
        stmts = []
        for s in a_strs:
            stmts.append(self.glue(s, b_str, c_str) + self.line_comment())
        return stmts

    def distribute_right(self, a, b, c):
        "a > (b, c); ==> a>b; a>c;"
        a_str = a.show()
        b_str = b.show()
        c_vals = c.args[0][0].args[0]
        c_strs = [x.show() for x in c_vals]
        stmts = []
        for s in c_strs:
            stmts.append(self.glue(a_str, b_str, s) + self.line_comment())
        return stmts

    def distribute_tupe(self, a, b, c):
        if ( a.args[0][0].cls_name() == "tupe" and
             c.args[0][0].cls_name() == "tupe" ):
            return self.distribute_both(a, b, c)

        if ( a.args[0][0].cls_name() == "tupe" ):
            return self.distribute_left(a, b, c)

        if ( c.args[0][0].cls_name() == "tupe" ):
            return self.distribute_right(a, b, c)
        
        raise ValueError("Shouldn't be here")

    def show1(self, items):
        return items[0].show() + ";"

    def show(self):     
        if len(self.args[0]) == 1:
            return self.show1(self.args[0]) + self.line_comment()

        a,b,c = self.args[0]

        stmts = []

        if ( a.args[0][0].cls_name() == "tupe" or
             c.args[0][0].cls_name() == "tupe" ):
            stmts.extend(self.distribute_tupe(a, b, c))
        else:
            stmts.append(self.glue(a.show(),
                                   b.show(),
                                   c.show()) + self.line_comment())
        
        return "\n".join(stmts)

class declaration(Node):
    def __init__(self, *args):
        Node.__init__(self, args)
    def show(self):
        temp = "%s %s = %s;" + self.line_comment()
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


# ------------------------------------------------------------------        
class mod(Node):
    def __init__(self, *args):
        Node.__init__(self, args)

    def show(self, quiet=False):
        name = self.args[0][0]
        output = ""
        output += "module %s { %s\n" % (name.show(), self.line_comment())
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
filename = "./temp/tmpfile-pass-3.ally"
tmpfile = open(filename, 'w')
tmpfile.write(t.show())

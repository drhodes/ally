# >  arrow
# >> compose
# +> if_true
# -> if_false
from utility import lookupErr, error, has_function

def add(a, b): return a + b

class Parameter(object):
    def __init__(self, typedec, name, line):                
        self.typedec = typedec
        self.name = name
        self.line = line
    def __repr__(self):
        return "<Parameter %s: %s>" % (self.typedec, self.name)

class Value(object):
    def __init__(self, val):
        self.val = val


class Cond(object):
    def __init__(self, name, line):
        self.name = name
        self.line = line
        self.content = None

class Place(object):
    def __init__(self, name, line):
        self.name = name
        self.line = line
        self.flag = None
        self.kind = None
        self.content = None

    def __repr__(self):
        return "(%s)" % self.name

    def is_empty(self):
        return self.content == None

    def is_typed(self):
        return self.kind != None

    def is_function(self):
        return self.kind == "func"

    def is_value(self):
        return self.kind == "val"

class Arrow(object):
    def __init__(self, src, artype, tgt, line):
        self.src = src
        self.artype = artype
        self.tgt = tgt
        self.line = line

    def kind(self):
        return self.artype

    def targets_return(self):
        return self.tgt == "return"
        
    def __repr__(self):
        return "[Arrow: %s %s %s]" % (self.src, self.artype, self.tgt)

                 
class GraphMachine(object):
    def __init__(self, name, line):        
        self.name = name
        self.line = line
        self.arrows = []
        self.trans = {}
        self.places = {}

    def add_param(self, typedec, name, line):
        param = Parameter(typedec, name, line)
        msg = "Parameter name: `%s`, is already defined."

        if name in self.places:
            error(msg % name, line)
            
        self.places[name] = Place(name, line)
        self.places[name].kind = typedec

    def add_arrow(self, src, artype, tgt, line):
        arr = Arrow(src, artype, tgt, line)        
        self.arrows.append(arr)

    def add_declaration(self, typedec, name, val, line):
        if name in self.places:
            error("Declaration `%s` is already defined.", line)

        plc = Place(name, line)
        plc.content = val
        plc.kind = typedec
        self.places[name] = plc        

    def check_has_return(self):
        for a in self.arrows:            
            if a.tgt == "return":
                return True
        error("Function: `%s`, has no return" % self.name, self.line)

    def name_exists(self, name):
        if ( has_function(prelude, name) or
             name in self.places ):                    
            return True
        error("Name: `%s`, not found", name)
        
    def check_iff(self, arr):
        print arr

    def check_ift(self, arr):
        print arr

    def check_apply(self, arr):
        print arr
        
    def check_compose(self, arr):
        print arr

    def check_arrows(self):        
        for arr in self.arrows:            
            if arr.artype == "+>":
                self.check_ift(arr)
            if arr.artype == "->":
                self.check_iff(arr)
            if arr.artype == ">>":
                self.check_compose(arr)
            if arr.artype == ">":
                self.check_apply(arr)


                       
    def run(self):
        self.check_has_return()        
        self.check_arrows()
        print "Running!"





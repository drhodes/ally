# >  arrow
# >> compose
# +> if_true
# -> if_false
from utility import lookupErr

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


class Place(object):
    def __init__(self, name, line):
        self.name = name
        self.line = line
        self.flag = None
        self.kind = None
        self.content = None

    def __repr__(self):
        return "(%s)" % self.name

    def check_sane(self):
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
        if artype == ">":
            return "apply"
        if artype == ">>":
            return "compose"
        if artype == "+>":
            return "condition-true"
        if artype == "->":
            return "confition-false"

    def targets_return(self):
        return self.tgt == "return"
        
    def __repr__(self):
        return "[Arrow: %s %s %s]" % (self.src, self.artype, self.tgt)
                 
class GraphMachine(object):
    def __init__(self):        
        self.params = {}        
        self.arrows = []
        self.funcs = {}
        self.vars = {}
        self.places = {}

    def targets_return(self):
        for a in self.arrows:
            if a.targets_return():
                return a
        self.error("functions must return!")
        return None
            
    def error(self, msg, line):
        fn, ln, num = lookupErr( line)        
        tmp = "\n\n%s\n\nfile:    %s\nline:    %s\n\nline number:    %s"
        raise SyntaxError(tmp % ( msg.strip(),
                                  fn.strip(),
                                  ln.strip(),
                                  num.strip()))

    def add_param(self, typedec, name, line):
        param = Parameter(typedec, name, line)
        msg = "Parameter name: `%s`, is trying to shadow:"
        if name in self.params:
            other = self.params[name]         
            self.error(msg % name, line)
        self.params[name] = param

    def add_arrow(self, src, artype, tgt, line):
        arr = Arrow(src, artype, tgt, line)        
        self.places[src] = Place(src, line)
        self.places[tgt] = Place(tgt, line)
        self.arrows.append(arr)

    def add_declaration(self, typedec, name, val, line):
        if name in self.params:            
            self.error("Declaration is trying to shadow a parameter", line)
        if name in self.places:
            self.error("Declaration is trying to shadow a previous declaration", line)
        plc = Place(name, line)

        plc.content = val
        plc.kind = typedec
        self.places[name] = plc

    def add_compose(self, src, tgt):
        pass

    def add_cond_true(self, src, tgt):
        pass

    def add_cond_false(self, src, tgt):
        pass

    def typify(self):
        self.places["return"].kind = "val"

        for arr in self.arrows:
            if arr.targets_return():                               
                self.places[arr.src].kind = "func"

            # if arrow target is place 

            
        for arr in self.arrows:
            if self.places[arr.tgt].check_sane():
                if self.places[arr.src].check_sane():
                    continue
                else:
                    if self.places[arr.tgt].is_function():
                        self.places[arr.src].kind = "val" # this needs to change
                    else:
                        self.places[arr.src].kind = "func" # use polymorphism here.

        for p in self.places.values():
            if not p.check_sane():
                self.typify()
            
        for p in self.places.values():
            print p, p.kind

    def run(self):
        self.typify()
        print "Running!"












# XML to custom python object deserializer.
import sys
from lxml import etree

class Node(object):
    def __init__(self, vals, children):
        self.line = vals["line"]
        self.vals = vals
        self.children = children        
    def kind(self):
        return self.__class__.__name__
    def __repr__(self):
        return str((self.__class__.__name__, self.vals, self.children))
class comment(Node):
    def __init__(self, vals, children):
        Node.__init__(self, vals, children)
class module(Node):
    def __init__(self, vals, children):
        Node.__init__(self, vals, children)
class rawstring(Node):
    def __init__(self, vals, children):
        Node.__init__(self, vals, children)
class literal(Node):
    def __init__(self, vals, children):
        Node.__init__(self, vals, children)
class symbol(Node):
    def __init__(self, vals, children):
        Node.__init__(self, vals, children)
    def name(self):
        return self.vals["val"]        
class typedec(Node):
    def __init__(self, vals, children):
        Node.__init__(self, vals, children)
class dot(Node):
    def __init__(self, vals, children):
        Node.__init__(self, vals, children)
class pipe(Node):
    def __init__(self, vals, children):
        Node.__init__(self, vals, children)
class TFI(Node):
    def __init__(self, vals, children):
        Node.__init__(self, vals, children)
    def __repr__(self):
        return "<+"
class IFT(Node):
    def __init__(self, vals, children):
        Node.__init__(self, vals, children)
    def __repr__(self):
        return "+>"
class IFF(Node):
    def __init__(self, vals, children):
        Node.__init__(self, vals, children)
    def __repr__(self):
        return "->"
class FFI(Node):
    def __init__(self, vals, children):
        Node.__init__(self, vals, children)
    def __repr__(self):
        return "<-"
class DUB(Node):
    def __init__(self, vals, children):
        Node.__init__(self, vals, children)
    def __repr__(self):
        return "<>"
class LS(Node):
    def __init__(self, vals, children):
        Node.__init__(self, vals, children)
    def __repr__(self):
        return "<<"
class RS(Node):
    def __init__(self, vals, children):
        Node.__init__(self, vals, children)
    def __repr__(self):
        return ">>"
class FWD(Node):
    def __init__(self, vals, children):
        Node.__init__(self, vals, children)
    def __repr__(self):
        return ">"
class BAK(Node):
    def __init__(self, vals, children):
        Node.__init__(self, vals, children)
    def __repr__(self):
        return "<"

class PTFI(Node):
    def __init__(self, vals, children):
        Node.__init__(self, vals, children)
    def __repr__(self):
        return "|<+"
class PIFT(Node):
    def __init__(self, vals, children):
        Node.__init__(self, vals, children)
    def __repr__(self):
        return "|+>"
class PIFF(Node):
    def __init__(self, vals, children):
        Node.__init__(self, vals, children)
    def __repr__(self):
        return "|->"
class PFFI(Node):
    def __init__(self, vals, children):
        Node.__init__(self, vals, children)
    def __repr__(self):
        return "|<-"
class PDUB(Node):
    def __init__(self, vals, children):
        Node.__init__(self, vals, children)
    def __repr__(self):
        return "|<>"
class PLS(Node):
    def __init__(self, vals, children):
        Node.__init__(self, vals, children)
    def __repr__(self):
        return "|<<"
class PRS(Node):
    def __init__(self, vals, children):
        Node.__init__(self, vals, children)
    def __repr__(self):
        return "|>>"
class PFWD(Node):
    def __init__(self, vals, children):
        Node.__init__(self, vals, children)
    def __repr__(self):
        return "|>"
class PBAK(Node):
    def __init__(self, vals, children):
        Node.__init__(self, vals, children)
    def __repr__(self):
        return "|<"
class arrow(Node):
    def __init__(self, vals, children):
        Node.__init__(self, vals, children)
class pipeq(Node):
    def __init__(self, vals, children):
        Node.__init__(self, vals, children)
    def __repr__(self):
        return "|="
class arr(Node):
    def __init__(self, vals, children):
        Node.__init__(self, vals, children)
class ident(Node):
    def __init__(self, vals, children):
        Node.__init__(self, vals, children)
        #print children[0].name()
    def __repr__(self):
        return self.children[0].name()
class assign(Node):
    def __init__(self, vals, children):
        Node.__init__(self, vals, children)
    def __repr__(self):
        return "|=";
class place(Node):
    def __init__(self, vals, children):
        Node.__init__(self, vals, children)
class expression(Node):
    def __init__(self, vals, children):        
        Node.__init__(self, vals, children)
        self.trips = []
        for c in children:
            print c.kind(), c.children[0]
        print "------------------------------------------------------------------"
            
class declaration(Node):
    def __init__(self, vals, children):
        Node.__init__(self, vals, children)
class statement(Node):
    def __init__(self, vals, children):
        Node.__init__(self, vals, children)
class block(Node):
    def __init__(self, vals, children):
        Node.__init__(self, vals, children)
        self.stmts = children
class emptyparam(Node):
    def __init__(self, vals, children):
        Node.__init__(self, vals, children)
class parameterlist(Node):
    def __init__(self, vals, children):
        Node.__init__(self, vals, children)
class function(Node):
    def __init__(self, vals, children):
        Node.__init__(self, vals, children)
        self.locals = {}        
        self.name = children[0].name()        
        self.params = children[1]
        self.block = children[2]        
    def declarations(self):
        decs = []        
class mod(Node):
    def __init__(self, vals, children):
        Node.__init__(self, vals, children)

# -----------------------------------------------------------------------------
class Sog(object):
    def __init__(self, objs, infile):
        self.objs = objs
        self.infile = infile
        self.xml_root = None
        self.obj_root = None
        self.setup()

    def setup(self):
        self.xml_root = etree.fromstring(open(self.infile).read())
        self.obj_root = self.process(self.xml_root)
        
    def process(self, node):
        klass = self.objs[node.tag]
        #print klass
        values = dict(node.items())
        children = []

        for n in node.getchildren():                        
            children.append(self.process(n))

        return klass(values, children)
        
table = {\
    "comment": comment,
    "module": module,
    "rawstring": rawstring,
    "literal": literal,
    "symbol": symbol,
    "typedec": typedec,
    "dot": dot,
    "pipe": pipe,
    "TFI": TFI,
    "IFT": IFT,
    "IFF": IFF,
    "FFI": FFI,
    "DUB": DUB,
    "LS": LS,
    "RS": RS,
    "FWD": FWD,
    "BAK": BAK,
    "PTFI": PTFI,
    "PIFT": PIFT,
    "PIFF": PIFF,
    "PFFI": PFFI,
    "PDUB": PDUB,
    "PLS": PLS,
    "PRS": PRS,
    "PFWD": PFWD,
    "PBAK": PBAK,
    "pipeq": pipeq,
    "arr": arr,
    "arrow": arrow,
    "ident": ident,
    "assign": assign,
    "place": place,
    "expression": expression,
    "declaration": declaration,
    "statement": statement,
    "block": block,
    "emptyparam": emptyparam,
    "parameterlist": parameterlist,
    "function": function,
    "mod": mod,
    }

if __name__ == "__main__":
    s =  Sog(table, sys.argv[1])
    mod = s.obj_root
    #print mod
    

program = '''
12 + 34 * 5
'''

class Operator(object):
    def __init__(self, name, prec):
        self.name = name
        self.prec = prec
        self.left = None
        self.right = None

class Primitive(object):
    def __init__(self, s):        
        self.val = s
        self.prec = -1

def tokenize(rules, program):
    result = []
    for s in program.strip().split():
        if s in rules:
            result.append(rules[s])
        else:
            result.append(Primitive(s))
    return result

def highest_prec(tokens):
    pairs = list(reversed(sorted((t.prec, t) for t in tokens)))
    return pairs[0][1]


def parse(tokens):
    hp = highest_prec(tokens)
    hpi = tokens.index(hp)
    trip = ( tokens[hpi-1:hpi+2] )
    

    for t in tokens:
        print t
    


def main():
    rules = {'+': Operator("add", 0),
             '*': Operator("mult", 5)
             }

    toks = tokenize(rules, program)
    parse(toks)
    
main()

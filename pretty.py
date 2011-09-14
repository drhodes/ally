
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

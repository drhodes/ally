
# >  arrow
# >> compose
# +> if_true
# -> if_false

class GraphFunction(object):
    def __init__(self):
        self.trans = {}
        self.vars = {}

    def add_arrow(self, src, tgt):
        self.trans[src] = tgt
    
    def add_compose(self, src, tgt):
        

    def add_cond_true(self, src, tgt):
        pass

    def add_cond_false(self, src, tgt):
        pass
